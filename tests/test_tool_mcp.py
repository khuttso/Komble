import asyncio
import os
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters
import pytest

from src.act import call_tool
from src.mcp_server import mcp
from src.tools import TOOLS
from tests.test_tool_golden import CASES


def test_both_doors_publish_identical_contracts():
    async def check():
        async with Client(mcp) as client:
            listed = {tool.name: tool for tool in (await client.list_tools()).tools}
            assert set(listed) == set(TOOLS)
            for name, tool in TOOLS.items():
                assert listed[name].input_schema == tool.schema(name)["function"]["parameters"]
                assert listed[name].input_schema["additionalProperties"] is False
                assert listed[name].annotations.read_only_hint
                assert listed[name].annotations.destructive_hint is False
    asyncio.run(check())


@pytest.mark.parametrize("owner,case", CASES, ids=[f"{owner}:{case['id']}" for owner, case in CASES])
def test_all_golden_cases_through_real_mcp_client(owner, case):
    async def check():
        async with Client(mcp) as client:
            mcp_result = await client.call_tool(case["tool"], case["arguments"])
        direct = call_tool({"name": case["tool"], "arguments": case["arguments"]})
        assert mcp_result.is_error == (not direct["ok"])
        if direct["ok"]:
            assert mcp_result.structured_content == direct["result"]
        else:
            assert mcp_result.content[0].text == direct["error"]
    asyncio.run(check())


def test_mcp_unknown_tool_has_safe_error():
    async def check():
        async with Client(mcp) as client:
            result = await client.call_tool("private-secret", {})
        assert result.is_error
        assert "private-secret" not in result.content[0].text
        assert "offered list" in result.content[0].text
    asyncio.run(check())


def test_stdio_transport_lists_and_calls_tool():
    async def check():
        params = StdioServerParameters(command=sys.executable, args=["-m", "src.mcp_server"],
            cwd=str(Path(__file__).resolve().parents[1]),
            env={"INTERVIEWCOACH_TOOL_LOG": os.environ["INTERVIEWCOACH_TOOL_LOG"]})
        async with Client(params) as client:
            assert (await client.list_tools()).tools[0].name == "get_pack_questions"
            good = await client.call_tool("get_pack_questions", {"pack_id": "frontend", "limit": 1})
            assert not good.is_error and good.structured_content["returned"] == 1
            bad = await client.call_tool("get_pack_questions", {"pack_id": "frontend", "user_id": "other"})
            assert bad.is_error and "identity" in bad.content[0].text
    asyncio.run(check())
