"""M365 Backend Stub"""
from typing import Any, Dict, List

class M365Backend:
    def __init__(self):
        self.name = "m365"
    
    def get_tools(self) -> List[Dict]:
        return [
            {"name": "read_emails", "description": "[M365] Read emails from inbox", "inputSchema": {"type": "object", "properties": {"top": {"type": "integer"}, "unread_only": {"type": "boolean"}}, "required": []}},
            {"name": "get_email", "description": "[M365] Get full email by ID", "inputSchema": {"type": "object", "properties": {"message_id": {"type": "string"}}, "required": ["message_id"]}},
            {"name": "send_email", "description": "[M365] Send email", "inputSchema": {"type": "object", "properties": {"to": {"type": "array"}, "subject": {"type": "string"}, "body": {"type": "string"}}, "required": ["to", "subject", "body"]}},
            {"name": "reply_email", "description": "[M365] Reply to email", "inputSchema": {"type": "object", "properties": {"message_id": {"type": "string"}, "body": {"type": "string"}}, "required": ["message_id", "body"]}},
            {"name": "search_emails", "description": "[M365] Search emails", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
            {"name": "list_calendar_events", "description": "[M365] List calendar events", "inputSchema": {"type": "object", "properties": {"start_date": {"type": "string"}, "end_date": {"type": "string"}}, "required": []}},
            {"name": "create_event", "description": "[M365] Create calendar event", "inputSchema": {"type": "object", "properties": {"subject": {"type": "string"}, "start": {"type": "string"}, "end": {"type": "string"}}, "required": ["subject", "start", "end"]}},
            {"name": "get_availability", "description": "[M365] Check free/busy", "inputSchema": {"type": "object", "properties": {"emails": {"type": "array"}, "start": {"type": "string"}, "end": {"type": "string"}}, "required": ["emails", "start", "end"]}},
            {"name": "list_users", "description": "[M365] List org users", "inputSchema": {"type": "object", "properties": {}, "required": []}},
            {"name": "get_user", "description": "[M365] Get user profile", "inputSchema": {"type": "object", "properties": {"user": {"type": "string"}}, "required": ["user"]}}
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        return {"status": "stub", "tool": tool_name}
