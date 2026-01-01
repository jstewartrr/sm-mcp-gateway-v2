"""
Snowflake Backend
Provides database query access to Sovereign Mind, Hurricane, and DealCloud databases
"""

import os
import json
import logging
from typing import Any, Dict, List

import snowflake.connector

logger = logging.getLogger(__name__)


class SnowflakeBackend:
    """Snowflake database backend"""
    
    def __init__(self):
        self.name = "snowflake"
        self.conn = None
        self._init_connection()
        
    def _init_connection(self):
        """Initialize Snowflake connection"""
        try:
            self.conn = snowflake.connector.connect(
                user=os.getenv("SNOWFLAKE_USER", "JOHN_CLAUDE"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                account=os.getenv("SNOWFLAKE_ACCOUNT", "uib44717"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
                database=os.getenv("SNOWFLAKE_DATABASE", "SOVEREIGN_MIND"),
                schema=os.getenv("SNOWFLAKE_SCHEMA", "RAW"),
                role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
            )
            logger.info("Snowflake connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {e}")
            self.conn = None
    
    def get_tools(self) -> List[Dict]:
        return [{
            "name": "query_snowflake",
            "description": "[SM] Execute SQL query on Snowflake as JOHN_CLAUDE",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "SQL query to execute"
                    }
                },
                "required": ["sql"]
            }
        }]
    
    async def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        if tool_name == "query_snowflake":
            return await self._query(arguments.get("sql", ""))
        return {"error": f"Unknown tool: {tool_name}"}
    
    async def _query(self, sql: str) -> Dict:
        """Execute SQL query"""
        if not self.conn:
            self._init_connection()
            if not self.conn:
                return {"success": False, "error": "No database connection"}
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            
            # Get column names
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            
            # Fetch results
            rows = cursor.fetchall()
            
            # Convert to list of dicts
            data = []
            for row in rows:
                row_dict = {}
                for i, col in enumerate(columns):
                    value = row[i]
                    # Handle special types
                    if hasattr(value, 'isoformat'):
                        value = value.isoformat()
                    row_dict[col] = value
                data.append(row_dict)
            
            cursor.close()
            
            return {
                "success": True,
                "data": data,
                "row_count": len(data)
            }
            
        except Exception as e:
            logger.error(f"Query error: {e}")
            return {"success": False, "error": str(e)}
