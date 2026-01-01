"""
Backend Base Class
All MCP backends inherit from this class
"""

from abc import ABC, abstractmethod
from typing import Any, List, Dict
import logging

logger = logging.getLogger(__name__)


class BackendBase(ABC):
    """Base class for all MCP backends"""
    
    def __init__(self, name: str):
        self.name = name
        self.initialized = False
        self._tools = []
        
    @abstractmethod
    def get_tools(self) -> List[Dict]:
        """Return list of tools provided by this backend"""
        pass
    
    @abstractmethod
    async def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Execute a tool call"""
        pass
    
    def _register_tool(self, name: str, description: str, parameters: Dict):
        """Helper to register a tool"""
        self._tools.append({
            "name": name,
            "description": description,
            "inputSchema": parameters
        })
