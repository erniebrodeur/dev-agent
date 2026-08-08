from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = ROOT / "plugins" / "dev-agent"
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
POLICY_PATH = PLUGIN_ROOT / "AGENTS.md"
ACTIVATE_ROOT = PLUGIN_ROOT / "skills" / "activate"


class PluginLayoutTests(unittest.TestCase):
    def test_manifest_identity_matches_plugin_directory(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text())

        self.assertEqual(PLUGIN_ROOT.name, manifest["name"])
        self.assertEqual("0.1.0", manifest["version"])
        self.assertEqual("./skills/", manifest["skills"])
        self.assertNotIn("apps", manifest)
        self.assertNotIn("mcpServers", manifest)

    def test_activate_is_explicit_and_loads_canonical_policy(self) -> None:
        skill = (ACTIVATE_ROOT / "SKILL.md").read_text()
        metadata = (ACTIVATE_ROOT / "agents" / "openai.yaml").read_text()

        self.assertTrue(POLICY_PATH.is_file())
        self.assertIn("`../../AGENTS.md`", skill)
        self.assertIn("current task", skill)
        self.assertIn("allow_implicit_invocation: false", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_marketplace_points_to_plugin(self) -> None:
        marketplace = json.loads(MARKETPLACE_PATH.read_text())
        entries = [entry for entry in marketplace["plugins"] if entry["name"] == "dev-agent"]

        self.assertEqual(1, len(entries))
        self.assertEqual(
            {"source": "local", "path": "./plugins/dev-agent"},
            entries[0]["source"],
        )
        self.assertEqual("AVAILABLE", entries[0]["policy"]["installation"])
        self.assertEqual("ON_INSTALL", entries[0]["policy"]["authentication"])

    def test_package_is_deterministic_and_contains_only_plugin_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.zip"
            second = Path(directory) / "second.zip"

            subprocess.run([ROOT / "scripts" / "package-plugin", first], check=True)
            subprocess.run([ROOT / "scripts" / "package-plugin", second], check=True)

            self.assertEqual(
                hashlib.sha256(first.read_bytes()).digest(),
                hashlib.sha256(second.read_bytes()).digest(),
            )
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(
                    [
                        ".codex-plugin/plugin.json",
                        "AGENTS.md",
                        "skills/activate/SKILL.md",
                        "skills/activate/agents/openai.yaml",
                    ],
                    archive.namelist(),
                )


if __name__ == "__main__":
    unittest.main()
