"""MCP 2.3 stdio server; raw arguments pass through the same dispatcher as function calls.

Low-level handlers preserve unknown fields so the contract can reject them explicitly.
Run from the repository root: python -m src.mcp_server
"""
import asyncio
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations

from .act import call_tool
from .tools import PackQuestions, tools_for


async def list_tools(ctx, params):
    return ListToolsResult(tools=[Tool(
        name=name, description=tool.args.__doc__.strip(),
        input_schema=tool.args.model_json_schema(),
        output_schema=PackQuestions.model_json_schema(),
        annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False,
                                    idempotent_hint=True, open_world_hint=False),
    ) for name, tool in tools_for().items()])


async def run_tool(ctx, params):
    # This server offers public reads only. It has no identity argument or write capability.
    out = call_tool({"name": params.name, "arguments": params.arguments or {}}, tools_for(), None)
    if not out["ok"]:
        return CallToolResult(is_error=True, content=[TextContent(type="text", text=out["error"])])
    return CallToolResult(structured_content=out["result"],
                          content=[TextContent(type="text", text=json.dumps(out["result"]))])


mcp = Server("interviewcoach", on_list_tools=list_tools, on_call_tool=run_tool,
             instructions="Read public starter questions; no private packs, model generation or writes.")


async def main():
    async with stdio_server() as (read, write):
        await mcp.run(read, write, mcp.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
