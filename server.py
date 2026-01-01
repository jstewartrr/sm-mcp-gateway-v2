"""
SM MCP Gateway V2 - Sovereign Mind Master Gateway
Version: 2.0.0
Architecture: Modular backend system with unified SSE endpoint

This is the V2 refactored gateway with clean separation of concerns.
30-day parallel run before decommissioning V1.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Optional

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("sm-mcp-gateway-v2")

# Version info
VERSION = "2.0.0"
BUILD_DATE = "2026-01-01"
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

# Import all backend modules
from backends.snowflake_backend import SnowflakeBackend
from backends.asana_backend import AsanaBackend
from backends.drive_backend import GoogleDriveBackend
from backends.m365_backend import M365Backend
from backends.hivemind_backend import HiveMindBackend
from backends.stubs import (
    DropboxBackend, DealCloudBackend, GitHubBackend, AzureBackend,
    MakeBackend, VertexBackend, GeminiBackend, ElevenLabsBackend,
    SimliBackend, FigmaBackend, VectorBackend, TailscaleBackend, NotebookBackend
)

# Initialize all backends
BACKENDS = {}

def init_backends():
    """Initialize all backend modules"""
    global BACKENDS
    
    backend_classes = [
        ("sm", SnowflakeBackend),
        ("asana", AsanaBackend),
        ("drive", GoogleDriveBackend),
        ("m365", M365Backend),
        ("dropbox", DropboxBackend),
        ("dc", DealCloudBackend),
        ("github", GitHubBackend),
        ("azure", AzureBackend),
        ("make", MakeBackend),
        ("vertex", VertexBackend),
        ("gemini", GeminiBackend),
        ("voice", ElevenLabsBackend),
        ("avatar", SimliBackend),
        ("figma", FigmaBackend),
        ("vector", VectorBackend),
        ("ts", TailscaleBackend),
        ("notebook", NotebookBackend),
        ("hivemind", HiveMindBackend),
    ]
    
    for prefix, backend_class in backend_classes:
        try:
            BACKENDS[prefix] = backend_class()
            logger.info(f"Initialized backend: {prefix}")
        except Exception as e:
            logger.error(f"Failed to initialize {prefix}: {e}")
            BACKENDS[prefix] = None

def get_all_tools():
    """Aggregate tools from all backends"""
    all_tools = []
    
    # Add gateway meta-tools
    all_tools.append({
        "name": "gateway_status",
        "description": "[GATEWAY] Get the status of all MCP backends and health information",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    })
    
    # Collect tools from each backend
    for prefix, backend in BACKENDS.items():
        if backend is None:
            continue
        try:
            backend_tools = backend.get_tools()
            for tool in backend_tools:
                # Prefix tool names with backend identifier
                tool["name"] = f"{prefix}_{tool['name']}"
                all_tools.append(tool)
        except Exception as e:
            logger.error(f"Error getting tools from {prefix}: {e}")
    
    return all_tools

async def handle_tool_call(name: str, arguments: dict) -> Any:
    """Route tool call to appropriate backend"""
    
    # Handle gateway meta-tools
    if name == "gateway_status":
        return await get_gateway_status()
    
    # Parse backend prefix from tool name
    parts = name.split("_", 1)
    if len(parts) < 2:
        return {"error": f"Invalid tool name format: {name}"}
    
    prefix = parts[0]
    tool_name = parts[1]
    
    if prefix not in BACKENDS:
        return {"error": f"Unknown backend: {prefix}"}
    
    backend = BACKENDS[prefix]
    if backend is None:
        return {"error": f"Backend {prefix} is not initialized"}
    
    try:
        result = await backend.call_tool(tool_name, arguments)
        return result
    except Exception as e:
        logger.error(f"Error calling {name}: {e}")
        return {"error": str(e)}

async def get_gateway_status():
    """Get comprehensive gateway status"""
    status = {
        "gateway": {
            "version": VERSION,
            "build_date": BUILD_DATE,
            "environment": ENVIRONMENT,
            "timestamp": datetime.utcnow().isoformat()
        },
        "backends": {},
        "total_tools": 0
    }
    
    for prefix, backend in BACKENDS.items():
        if backend is None:
            status["backends"][prefix] = {"status": "FAILED", "tools": 0}
        else:
            try:
                tools = backend.get_tools()
                tool_count = len(tools)
                status["backends"][prefix] = {
                    "status": "HEALTHY",
                    "tools": tool_count
                }
                status["total_tools"] += tool_count
            except Exception as e:
                status["backends"][prefix] = {
                    "status": "ERROR",
                    "error": str(e),
                    "tools": 0
                }
    
    return status

# SSE Protocol handlers
async def handle_sse_message(request_data: dict) -> dict:
    """Handle incoming JSON-RPC message"""
    method = request_data.get("method")
    params = request_data.get("params", {})
    msg_id = request_data.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "SM MCP Gateway V2",
                    "version": VERSION
                },
                "capabilities": {
                    "tools": {}
                }
            }
        }
    
    elif method == "tools/list":
        tools = get_all_tools()
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": tools
            }
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        result = await handle_tool_call(tool_name, arguments)
        
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, default=str)
                    }
                ]
            }
        }
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }

# HTTP Endpoints
async def health_check(request):
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "version": VERSION,
        "timestamp": datetime.utcnow().isoformat()
    })

async def sse_endpoint(request):
    """SSE endpoint for MCP protocol"""
    
    async def event_generator():
        # Send endpoint message
        endpoint_msg = {
            "jsonrpc": "2.0",
            "method": "endpoint",
            "params": {
                "endpoint": "/mcp"
            }
        }
        yield f"data: {json.dumps(endpoint_msg)}\n\n"
        
        # Keep connection alive
        while True:
            await asyncio.sleep(30)
            yield f": keepalive\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

async def mcp_endpoint(request):
    """Main MCP JSON-RPC endpoint"""
    try:
        body = await request.json()
        response = await handle_sse_message(body)
        return JSONResponse(response)
    except Exception as e:
        logger.error(f"MCP endpoint error: {e}")
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }, status_code=500)

async def tools_list(request):
    """Direct tools list endpoint"""
    tools = get_all_tools()
    return JSONResponse({
        "tools": tools,
        "total_tools": len(tools)
    })

async def status_endpoint(request):
    """Gateway status endpoint"""
    status = await get_gateway_status()
    return JSONResponse(status)

# Create Starlette app
app = Starlette(
    debug=ENVIRONMENT != "production",
    routes=[
        Route("/", health_check),
        Route("/health", health_check),
        Route("/sse", sse_endpoint),
        Route("/mcp", mcp_endpoint, methods=["POST"]),
        Route("/tools", tools_list),
        Route("/status", status_endpoint),
    ],
    on_startup=[init_backends]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
