from __future__ import annotations

import asyncio
import os
import sys
import tempfile
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from collaborative_ttt.mcp_server import mcp


class McpSurfaceTests(unittest.TestCase):
    def test_exact_tool_surface(self):
        tools = asyncio.run(mcp.list_tools())
        names = {tool.name for tool in tools}
        self.assertEqual(
            {"create_game", "get_actor_environment", "submit_move", "verify_replay"},
            names,
        )
        for tool in tools:
            self.assertTrue(tool.description)
            self.assertIsInstance(tool.inputSchema, dict)

    def test_real_stdio_initialize_and_tools_list(self):
        async def exchange():
            with tempfile.TemporaryDirectory() as temporary:
                environment = os.environ.copy()
                environment["COLLAB_TTT_DB"] = str(Path(temporary) / "games.sqlite3")
                parameters = StdioServerParameters(
                    command=sys.executable,
                    args=["-m", "collaborative_ttt.mcp_server"],
                    env=environment,
                )
                async with stdio_client(parameters) as (read, write):
                    async with ClientSession(read, write) as session:
                        initialized = await session.initialize()
                        listed = await session.list_tools()
                        return initialized.serverInfo.name, {tool.name for tool in listed.tools}

        server_name, names = asyncio.run(exchange())
        self.assertEqual("collaborative-tic-tac-toe", server_name)
        self.assertEqual(
            {"create_game", "get_actor_environment", "submit_move", "verify_replay"},
            names,
        )


if __name__ == "__main__":
    unittest.main()
