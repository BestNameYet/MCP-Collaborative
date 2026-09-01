from __future__ import annotations

import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]


class WindowsLauncherTests(unittest.TestCase):
    def test_server_launcher_is_private_stdio_and_uses_durable_database(self) -> None:
        script = (PLUGIN_ROOT / "scripts" / "run-server.cmd").read_text(encoding="utf-8")
        self.assertIn("COLLAB_TTT_DB", script)
        self.assertIn("LOCALAPPDATA", script)
        self.assertIn("collab-tic-tac-toe-mcp.exe", script)
        self.assertNotIn("http://", script)
        self.assertNotIn("https://", script)

    def test_tunnel_launcher_uses_official_stdio_profile_without_secrets(self) -> None:
        script = (PLUGIN_ROOT / "scripts" / "start-tunnel.ps1").read_text(encoding="utf-8")
        self.assertIn("sample_mcp_stdio_local", script)
        self.assertIn("--mcp-command", script)
        self.assertIn("doctor --profile", script)
        self.assertIn("CONTROL_PLANE_API_KEY", script)
        self.assertNotIn("sk-", script)

    def test_setup_installs_plugin_into_isolated_environment(self) -> None:
        script = (PLUGIN_ROOT / "scripts" / "setup-windows.ps1").read_text(encoding="utf-8")
        self.assertIn("sys.version_info >= (3, 11)", script)
        self.assertIn("-3 -m venv", script)
        self.assertIn("-m pip install $PluginRoot", script)


if __name__ == "__main__":
    unittest.main()
