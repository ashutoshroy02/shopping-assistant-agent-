from typing import Any, Callable


class MCPServer:
    def __init__(self, name: str):
        self.name = name
        self.tools: dict[str, Callable] = {}

    def tool(self, name: str, description: str = ""):
        def decorator(func: Callable) -> Callable:
            self.tools[name] = {
                "function": func,
                "name": name,
                "description": description,
            }
            return func
        return decorator

    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found in {self.name}")

        tool = self.tools[tool_name]
        return await tool["function"](**kwargs)

    def get_tools_schema(self) -> list[dict[str, Any]]:
        schemas = []
        for name, tool in self.tools.items():
            schemas.append({
                "name": name,
                "description": tool["description"],
            })
        return schemas
