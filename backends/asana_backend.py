"""
Asana Backend
Project management tools for Asana workspace
"""

import os
import logging
from typing import Any, Dict, List
import httpx

logger = logging.getLogger(__name__)

ASANA_BASE = "https://app.asana.com/api/1.0"


class AsanaBackend:
    """Asana project management backend"""
    
    def __init__(self):
        self.name = "asana"
        self.token = os.getenv("ASANA_TOKEN")
        self.workspace_gid = os.getenv("ASANA_WORKSPACE_GID", "373563495855656")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def get_tools(self) -> List[Dict]:
        return [
            {
                "name": "get_user",
                "description": "[ASANA] Get information about a user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "default": "me"}
                    },
                    "required": []
                }
            },
            {
                "name": "get_my_tasks",
                "description": "[ASANA] Get tasks assigned to the authenticated user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "default": 50},
                        "completed": {"type": "boolean", "default": False}
                    },
                    "required": []
                }
            },
            {
                "name": "list_projects",
                "description": "[ASANA] List all projects in the workspace",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "default": 50},
                        "archived": {"type": "boolean", "default": False}
                    },
                    "required": []
                }
            },
            {
                "name": "get_project",
                "description": "[ASANA] Get details of a specific project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string"}
                    },
                    "required": ["project_id"]
                }
            },
            {
                "name": "create_project",
                "description": "[ASANA] Create a new project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "notes": {"type": "string"},
                        "team": {"type": "string"},
                        "due_date": {"type": "string"},
                        "public": {"type": "boolean", "default": False}
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "list_tasks",
                "description": "[ASANA] List tasks with optional filters",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string"},
                        "assignee": {"type": "string"},
                        "section": {"type": "string"},
                        "completed": {"type": "boolean"},
                        "limit": {"type": "integer", "default": 50}
                    },
                    "required": []
                }
            },
            {
                "name": "get_task",
                "description": "[ASANA] Get detailed information about a task",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "create_task",
                "description": "[ASANA] Create a new task",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "notes": {"type": "string"},
                        "project_id": {"type": "string"},
                        "section_id": {"type": "string"},
                        "assignee": {"type": "string"},
                        "due_date": {"type": "string"},
                        "due_at": {"type": "string"},
                        "parent": {"type": "string"},
                        "tags": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "update_task",
                "description": "[ASANA] Update an existing task",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "name": {"type": "string"},
                        "notes": {"type": "string"},
                        "assignee": {"type": "string"},
                        "due_date": {"type": "string"},
                        "due_at": {"type": "string"},
                        "completed": {"type": "boolean"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "complete_task",
                "description": "[ASANA] Mark a task as complete",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "delete_task",
                "description": "[ASANA] Delete a task permanently",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "add_task_to_project",
                "description": "[ASANA] Add an existing task to a project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "project_id": {"type": "string"},
                        "section_id": {"type": "string"}
                    },
                    "required": ["task_id", "project_id"]
                }
            },
            {
                "name": "list_sections",
                "description": "[ASANA] List sections in a project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string"}
                    },
                    "required": ["project_id"]
                }
            },
            {
                "name": "create_section",
                "description": "[ASANA] Create a new section in a project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string"},
                        "name": {"type": "string"}
                    },
                    "required": ["project_id", "name"]
                }
            },
            {
                "name": "move_task_to_section",
                "description": "[ASANA] Move a task to a different section",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "section_id": {"type": "string"}
                    },
                    "required": ["task_id", "section_id"]
                }
            },
            {
                "name": "get_subtasks",
                "description": "[ASANA] Get subtasks of a parent task",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "add_comment",
                "description": "[ASANA] Add a comment to a task",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "text": {"type": "string"}
                    },
                    "required": ["task_id", "text"]
                }
            },
            {
                "name": "get_task_comments",
                "description": "[ASANA] Get comments on a task",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "search_tasks",
                "description": "[ASANA] Search for tasks in the workspace",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "assignee": {"type": "string"},
                        "projects": {"type": "string"},
                        "completed": {"type": "boolean"},
                        "due_on": {"type": "string"},
                        "due_before": {"type": "string"},
                        "due_after": {"type": "string"},
                        "is_subtask": {"type": "boolean"},
                        "limit": {"type": "integer", "default": 25}
                    },
                    "required": []
                }
            },
            {
                "name": "list_teams",
                "description": "[ASANA] List all teams in the workspace",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "default": 100}
                    },
                    "required": []
                }
            },
            {
                "name": "list_workspace_users",
                "description": "[ASANA] List all users in the workspace",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "default": 100}
                    },
                    "required": []
                }
            },
            {
                "name": "list_tags",
                "description": "[ASANA] List all tags in the workspace",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "default": 100}
                    },
                    "required": []
                }
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Route tool call to appropriate handler"""
        handlers = {
            "get_user": self._get_user,
            "get_my_tasks": self._get_my_tasks,
            "list_projects": self._list_projects,
            "get_project": self._get_project,
            "create_project": self._create_project,
            "list_tasks": self._list_tasks,
            "get_task": self._get_task,
            "create_task": self._create_task,
            "update_task": self._update_task,
            "complete_task": self._complete_task,
            "delete_task": self._delete_task,
            "add_task_to_project": self._add_task_to_project,
            "list_sections": self._list_sections,
            "create_section": self._create_section,
            "move_task_to_section": self._move_task_to_section,
            "get_subtasks": self._get_subtasks,
            "add_comment": self._add_comment,
            "get_task_comments": self._get_task_comments,
            "search_tasks": self._search_tasks,
            "list_teams": self._list_teams,
            "list_workspace_users": self._list_workspace_users,
            "list_tags": self._list_tags
        }
        
        handler = handlers.get(tool_name)
        if not handler:
            return {"error": f"Unknown tool: {tool_name}"}
        
        return await handler(arguments)
    
    async def _api_get(self, endpoint: str, params: Dict = None) -> Dict:
        """Make GET request to Asana API"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{ASANA_BASE}{endpoint}",
                headers=self.headers,
                params=params,
                timeout=30
            )
            resp.raise_for_status()
            return resp.json()
    
    async def _api_post(self, endpoint: str, data: Dict) -> Dict:
        """Make POST request to Asana API"""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{ASANA_BASE}{endpoint}",
                headers=self.headers,
                json={"data": data},
                timeout=30
            )
            resp.raise_for_status()
            return resp.json()
    
    async def _api_put(self, endpoint: str, data: Dict) -> Dict:
        """Make PUT request to Asana API"""
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                f"{ASANA_BASE}{endpoint}",
                headers=self.headers,
                json={"data": data},
                timeout=30
            )
            resp.raise_for_status()
            return resp.json()
    
    async def _api_delete(self, endpoint: str) -> Dict:
        """Make DELETE request to Asana API"""
        async with httpx.AsyncClient() as client:
            resp = await client.delete(
                f"{ASANA_BASE}{endpoint}",
                headers=self.headers,
                timeout=30
            )
            resp.raise_for_status()
            return {"success": True}
    
    # Tool implementations
    async def _get_user(self, args: Dict) -> Dict:
        user_id = args.get("user_id", "me")
        result = await self._api_get(f"/users/{user_id}")
        return {"success": True, "user": result.get("data")}
    
    async def _get_my_tasks(self, args: Dict) -> Dict:
        params = {
            "workspace": self.workspace_gid,
            "assignee": "me",
            "limit": args.get("limit", 50),
            "opt_fields": "name,due_on,completed,notes"
        }
        if not args.get("completed", False):
            params["completed_since"] = "now"
        result = await self._api_get("/tasks", params)
        return {"success": True, "tasks": result.get("data", [])}
    
    async def _list_projects(self, args: Dict) -> Dict:
        params = {
            "workspace": self.workspace_gid,
            "limit": args.get("limit", 50),
            "archived": args.get("archived", False),
            "opt_fields": "name,notes,due_date,owner,public"
        }
        result = await self._api_get("/projects", params)
        return {"success": True, "projects": result.get("data", [])}
    
    async def _get_project(self, args: Dict) -> Dict:
        project_id = args["project_id"]
        result = await self._api_get(f"/projects/{project_id}")
        return {"success": True, "project": result.get("data")}
    
    async def _create_project(self, args: Dict) -> Dict:
        data = {"workspace": self.workspace_gid, "name": args["name"]}
        if args.get("notes"):
            data["notes"] = args["notes"]
        if args.get("team"):
            data["team"] = args["team"]
        if args.get("due_date"):
            data["due_date"] = args["due_date"]
        if "public" in args:
            data["public"] = args["public"]
        result = await self._api_post("/projects", data)
        return {"success": True, "project": result.get("data")}
    
    async def _list_tasks(self, args: Dict) -> Dict:
        params = {"opt_fields": "name,due_on,due_at,completed,assignee,notes,projects,tags"}
        params["limit"] = args.get("limit", 50)
        
        if args.get("project_id"):
            params["project"] = args["project_id"]
        if args.get("assignee"):
            params["assignee"] = args["assignee"]
            params["workspace"] = self.workspace_gid
        if args.get("section"):
            params["section"] = args["section"]
        if "completed" in args:
            if not args["completed"]:
                params["completed_since"] = "now"
        
        result = await self._api_get("/tasks", params)
        return {"success": True, "count": len(result.get("data", [])), "tasks": result.get("data", [])}
    
    async def _get_task(self, args: Dict) -> Dict:
        result = await self._api_get(f"/tasks/{args['task_id']}")
        return {"success": True, "task": result.get("data")}
    
    async def _create_task(self, args: Dict) -> Dict:
        data = {"name": args["name"]}
        
        if args.get("notes"):
            data["notes"] = args["notes"]
        if args.get("assignee"):
            data["assignee"] = args["assignee"]
        if args.get("due_date"):
            data["due_on"] = args["due_date"]
        if args.get("due_at"):
            data["due_at"] = args["due_at"]
        if args.get("parent"):
            data["parent"] = args["parent"]
        
        if args.get("project_id"):
            data["projects"] = [args["project_id"]]
        if args.get("section_id"):
            data["memberships"] = [{"project": args.get("project_id"), "section": args["section_id"]}]
        
        result = await self._api_post("/tasks", data)
        return {"success": True, "task": result.get("data")}
    
    async def _update_task(self, args: Dict) -> Dict:
        task_id = args.pop("task_id")
        data = {}
        
        if args.get("name"):
            data["name"] = args["name"]
        if args.get("notes"):
            data["notes"] = args["notes"]
        if args.get("assignee"):
            data["assignee"] = args["assignee"]
        if args.get("due_date"):
            data["due_on"] = args["due_date"]
        if args.get("due_at"):
            data["due_at"] = args["due_at"]
        if "completed" in args:
            data["completed"] = args["completed"]
        
        result = await self._api_put(f"/tasks/{task_id}", data)
        return {"success": True, "task": result.get("data")}
    
    async def _complete_task(self, args: Dict) -> Dict:
        result = await self._api_put(f"/tasks/{args['task_id']}", {"completed": True})
        return {"success": True, "task": result.get("data")}
    
    async def _delete_task(self, args: Dict) -> Dict:
        await self._api_delete(f"/tasks/{args['task_id']}")
        return {"success": True, "deleted": args['task_id']}
    
    async def _add_task_to_project(self, args: Dict) -> Dict:
        data = {"project": args["project_id"]}
        if args.get("section_id"):
            data["section"] = args["section_id"]
        await self._api_post(f"/tasks/{args['task_id']}/addProject", data)
        return {"success": True}
    
    async def _list_sections(self, args: Dict) -> Dict:
        result = await self._api_get(f"/projects/{args['project_id']}/sections")
        return {"success": True, "sections": result.get("data", [])}
    
    async def _create_section(self, args: Dict) -> Dict:
        data = {"name": args["name"]}
        result = await self._api_post(f"/projects/{args['project_id']}/sections", data)
        return {"success": True, "section": result.get("data")}
    
    async def _move_task_to_section(self, args: Dict) -> Dict:
        data = {"task": args["task_id"]}
        await self._api_post(f"/sections/{args['section_id']}/addTask", data)
        return {"success": True}
    
    async def _get_subtasks(self, args: Dict) -> Dict:
        result = await self._api_get(f"/tasks/{args['task_id']}/subtasks")
        return {"success": True, "subtasks": result.get("data", [])}
    
    async def _add_comment(self, args: Dict) -> Dict:
        data = {"text": args["text"]}
        result = await self._api_post(f"/tasks/{args['task_id']}/stories", data)
        return {"success": True, "comment": result.get("data")}
    
    async def _get_task_comments(self, args: Dict) -> Dict:
        result = await self._api_get(f"/tasks/{args['task_id']}/stories")
        comments = [s for s in result.get("data", []) if s.get("type") == "comment"]
        return {"success": True, "comments": comments}
    
    async def _search_tasks(self, args: Dict) -> Dict:
        params = {"opt_fields": "name,due_on,completed,assignee,projects"}
        
        if args.get("text"):
            params["text"] = args["text"]
        if args.get("assignee"):
            params["assignee.any"] = args["assignee"]
        if args.get("projects"):
            params["projects.any"] = args["projects"]
        if "completed" in args:
            params["completed"] = args["completed"]
        if args.get("due_on"):
            params["due_on"] = args["due_on"]
        if args.get("due_before"):
            params["due_on.before"] = args["due_before"]
        if args.get("due_after"):
            params["due_on.after"] = args["due_after"]
        if "is_subtask" in args:
            params["is_subtask"] = args["is_subtask"]
        
        result = await self._api_get(f"/workspaces/{self.workspace_gid}/tasks/search", params)
        return {"success": True, "tasks": result.get("data", [])}
    
    async def _list_teams(self, args: Dict) -> Dict:
        params = {"limit": args.get("limit", 100)}
        result = await self._api_get(f"/workspaces/{self.workspace_gid}/teams", params)
        return {"success": True, "teams": result.get("data", [])}
    
    async def _list_workspace_users(self, args: Dict) -> Dict:
        params = {"limit": args.get("limit", 100)}
        result = await self._api_get(f"/workspaces/{self.workspace_gid}/users", params)
        return {"success": True, "users": result.get("data", [])}
    
    async def _list_tags(self, args: Dict) -> Dict:
        params = {"limit": args.get("limit", 100)}
        result = await self._api_get(f"/workspaces/{self.workspace_gid}/tags", params)
        return {"success": True, "tags": result.get("data", [])}
