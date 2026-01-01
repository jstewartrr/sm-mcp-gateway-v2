"""
HiveMind Backend
Shared memory system for cross-AI continuity
Reads/writes to SOVEREIGN_MIND.RAW.HIVE_MIND
"""

import os
import json
import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class HiveMindBackend:
    """HiveMind shared memory backend"""
    
    def __init__(self):
        self.name = "hivemind"
        # Uses Snowflake connection from snowflake_backend
        self.snowflake = None
    
    def set_snowflake(self, snowflake_backend):
        """Set reference to snowflake backend"""
        self.snowflake = snowflake_backend
    
    def get_tools(self) -> List[Dict]:
        return [
            {
                "name": "read",
                "description": "[GATEWAY] Read recent entries from the Sovereign Mind Hive Mind",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "default": 10, "maximum": 50},
                        "workstream": {"type": "string"},
                        "category": {"type": "string"},
                        "source": {"type": "string"}
                    },
                    "required": []
                }
            },
            {
                "name": "write",
                "description": "[GATEWAY] Write an entry to the Sovereign Mind Hive Mind shared memory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string", "description": "Source identifier"},
                        "category": {"type": "string", "description": "Category: CONTEXT, DECISION, ACTION_ITEM, etc"},
                        "workstream": {"type": "string", "description": "Workstream or project name", "default": "GENERAL"},
                        "summary": {"type": "string", "description": "Clear summary", "maxLength": 2000},
                        "details": {"type": "object", "description": "JSON details object"},
                        "priority": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"], "default": "MEDIUM"},
                        "tags": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["source", "category", "summary"]
                }
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        if tool_name == "read":
            return await self._read(arguments)
        elif tool_name == "write":
            return await self._write(arguments)
        return {"error": f"Unknown tool: {tool_name}"}
    
    async def _read(self, args: Dict) -> Dict:
        """Read from Hive Mind"""
        limit = min(args.get("limit", 10), 50)
        
        conditions = ["1=1"]
        if args.get("workstream"):
            conditions.append(f"WORKSTREAM = '{args['workstream']}'")
        if args.get("category"):
            conditions.append(f"CATEGORY = '{args['category']}'")
        if args.get("source"):
            conditions.append(f"SOURCE = '{args['source']}'")
        
        where_clause = " AND ".join(conditions)
        
        sql = f"""
        SELECT ID, CREATED_AT, SOURCE, CATEGORY, WORKSTREAM, SUMMARY, PRIORITY, STATUS
        FROM SOVEREIGN_MIND.RAW.HIVE_MIND
        WHERE {where_clause}
        ORDER BY CREATED_AT DESC
        LIMIT {limit}
        """
        
        # This would use the snowflake backend
        return {"sql": sql, "note": "Execute via snowflake backend"}
    
    async def _write(self, args: Dict) -> Dict:
        """Write to Hive Mind"""
        source = args.get("source", "UNKNOWN")
        category = args.get("category", "GENERAL")
        workstream = args.get("workstream", "GENERAL")
        summary = args.get("summary", "").replace("'", "''")
        details = json.dumps(args.get("details", {})).replace("'", "''")
        priority = args.get("priority", "MEDIUM")
        tags = args.get("tags", [])
        tags_sql = f"ARRAY_CONSTRUCT({','.join([repr(t) for t in tags])})" if tags else "NULL"
        
        sql = f"""
        INSERT INTO SOVEREIGN_MIND.RAW.HIVE_MIND 
        (SOURCE, CATEGORY, WORKSTREAM, SUMMARY, DETAILS, PRIORITY, TAGS)
        VALUES (
            '{source}',
            '{category}',
            '{workstream}',
            '{summary}',
            PARSE_JSON('{details}'),
            '{priority}',
            {tags_sql}
        )
        """
        
        return {"sql": sql, "note": "Execute via snowflake backend"}
