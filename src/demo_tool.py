"""One safe call through the real MCP client; no model or key needed."""
import asyncio
import json

from mcp import Client
from .mcp_server import mcp


async def main():
    async with Client(mcp) as client:
        result = await client.call_tool("get_pack_questions", {"pack_id": "frontend", "limit": 2})
    print(json.dumps(result.structured_content, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
