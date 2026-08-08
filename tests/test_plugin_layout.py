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
COMMIT_ROOT = PLUGIN_ROOT / "skills" / "commit"
COPY_AGENTS_ROOT = PLUGIN_ROOT / "skills" / "copy-agents"
GIT_STATUS_ROOT = PLUGIN_ROOT / "skills" / "git-status"
RECOVER_CONTEXT_ROOT = PLUGIN_ROOT / "skills" / "recover-project-context"
PLANNING_ROOT = PLUGIN_ROOT / "skills" / "planning"
NEXT_SLICE_ROOT = PLUGIN_ROOT / "skills" / "next-slice"
TROUBLESHOOT_ROOT = PLUGIN_ROOT / "skills" / "troubleshoot"
SECURITY_CHECK_ROOT = PLUGIN_ROOT / "skills" / "security-check"


class PluginLayoutTests(unittest.TestCase):
    def test_manifest_identity_matches_plugin_directory(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text())

        self.assertEqual(PLUGIN_ROOT.name, manifest["name"])
        self.assertRegex(
            manifest["version"],
            r"^0\.1\.0\+codex\.[a-z0-9-]+$",
        )
        self.assertEqual("./skills/", manifest["skills"])
        self.assertNotIn("apps", manifest)
        self.assertNotIn("mcpServers", manifest)
        self.assertIn(
            "Two-phase local commit preparation and approval",
            manifest["interface"]["capabilities"],
        )
        self.assertIn(
            "Reusable read-only Git status reporting",
            manifest["interface"]["capabilities"],
        )

    def test_activate_matches_activation_requests_and_loads_canonical_policy(self) -> None:
        skill = (ACTIVATE_ROOT / "SKILL.md").read_text()
        metadata = (ACTIVATE_ROOT / "agents" / "openai.yaml").read_text()

        self.assertTrue(POLICY_PATH.is_file())
        self.assertIn("`../../AGENTS.md`", skill)
        self.assertIn("`../recover-project-context/SKILL.md`", skill)
        self.assertIn("Activation is incomplete until", skill)
        self.assertIn("Do not report Dev Agent as active", skill)
        self.assertIn("mandatory and blocking", skill)
        self.assertIn("Do not defer project-context recovery", skill)
        self.assertIn("asks to activate Dev Agent", skill)
        self.assertIn("selects the Dev Agent plugin", skill)
        self.assertIn("context recovery is complete", metadata)
        self.assertIn("current task", skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_recover_context_is_implicit_and_verifies_project_state(self) -> None:
        skill = (RECOVER_CONTEXT_ROOT / "SKILL.md").read_text()
        metadata = (RECOVER_CONTEXT_ROOT / "agents" / "openai.yaml").read_text()

        self.assertIn("CURRENT_WORK.md", skill)
        self.assertIn("surface-scan", skill)
        self.assertIn("deep-scan", skill)
        self.assertIn("Dev Agent convention", skill)
        self.assertIn("project scratch pad", skill)
        self.assertIn("not a standard development artifact", skill)
        self.assertIn("Ask whether the user wants", skill)
        self.assertIn("tracked or ignored", skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_portable_policy_supports_current_work_creation(self) -> None:
        policy = POLICY_PATH.read_text()

        self.assertIn("Be willing to create `CURRENT_WORK.md`", policy)
        self.assertIn("tracked or ignored", policy)
        self.assertIn("wait for approval before writing", policy)

    def test_planning_is_an_implicit_conversational_loop(self) -> None:
        skill = (PLANNING_ROOT / "SKILL.md").read_text()
        metadata = (PLANNING_ROOT / "agents" / "openai.yaml").read_text()

        self.assertIn("no approved implementation slice", skill)
        self.assertIn("`../recover-project-context/SKILL.md`", skill)
        self.assertIn("CURRENT_WORK.md", skill)
        self.assertIn("provisional", skill)
        self.assertIn("settled", skill)
        self.assertIn("correction", skill)
        self.assertIn("explicit approval", skill)
        self.assertIn("Do not implement", skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_portable_policy_defines_an_implementation_slice(self) -> None:
        policy = POLICY_PATH.read_text()

        self.assertIn("An implementation slice is", policy)
        self.assertIn("smallest coherent, independently reviewable unit", policy)
        self.assertIn("outcome, scope, constraints or invariants, non-goals", policy)
        self.assertIn("authorization boundary", policy)
        self.assertIn("Approval authorizes implementation of that slice only", policy)

    def test_next_slice_implements_one_approved_slice(self) -> None:
        skill = (NEXT_SLICE_ROOT / "SKILL.md").read_text()
        metadata = (NEXT_SLICE_ROOT / "agents" / "openai.yaml").read_text()

        self.assertIn("exactly one approved implementation slice", skill)
        self.assertIn("`../recover-project-context/SKILL.md`", skill)
        self.assertIn("outcome, scope, constraints or invariants, non-goals", skill)
        self.assertIn("concise task title", skill)
        self.assertIn("before editing", skill)
        self.assertIn("does not block implementation", skill)
        self.assertIn("minor, conventional, and reversible", skill)
        self.assertIn("Return to planning", skill)
        self.assertIn("CURRENT_WORK.md", skill)
        self.assertIn("Do not begin another slice", skill)
        self.assertIn("Committing, pushing", skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_commit_prepares_then_waits_for_approval(self) -> None:
        skill = (COMMIT_ROOT / "SKILL.md").read_text()
        metadata = (COMMIT_ROOT / "agents" / "openai.yaml").read_text()

        self.assertIn("authorizes preparation only", skill)
        self.assertIn("stage only the intended", skill)
        self.assertIn("complete staged diff", skill)
        self.assertIn("exact staged scope and proposed message", skill)
        self.assertIn("Wait for explicit approval", skill)
        self.assertIn("material drift", skill)
        self.assertIn("Do not push", skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_git_status_reports_reusable_read_only_state(self) -> None:
        skill = (GIT_STATUS_ROOT / "SKILL.md").read_text()
        metadata = (GIT_STATUS_ROOT / "agents" / "openai.yaml").read_text()
        commit_skill = (COMMIT_ROOT / "SKILL.md").read_text()

        self.assertIn("read-only", skill)
        self.assertIn("active branch", skill)
        self.assertIn("detached HEAD", skill)
        self.assertIn("unborn branch", skill)
        self.assertIn("merge or rebase", skill)
        self.assertIn("upstream", skill)
        self.assertIn("local tracking refs", skill)
        self.assertIn("staged, unstaged, and untracked", skill)
        self.assertIn("Do not fetch", skill)
        self.assertIn("Do not reproduce", skill)
        self.assertIn("`../git-status/SKILL.md`", commit_skill)
        self.assertIn("mandatory first step", commit_skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_troubleshoot_diagnoses_and_waits_before_correction(self) -> None:
        skill = (TROUBLESHOOT_ROOT / "SKILL.md").read_text()
        metadata = (TROUBLESHOOT_ROOT / "agents" / "openai.yaml").read_text()

        self.assertIn("diagnosis-only", skill)
        self.assertIn("`../recover-project-context/SKILL.md`", skill)
        self.assertIn("intended behavior", skill)
        self.assertIn("observed behavior", skill)
        self.assertIn("facts from inference", skill)
        self.assertIn("credible hypotheses", skill)
        self.assertIn("falsify", skill)
        self.assertIn("recent change", skill)
        self.assertIn("confidence and remaining uncertainty", skill)
        self.assertIn("Do not edit implementation files", skill)
        self.assertIn("corrective slice", skill)
        self.assertIn("wait for explicit approval", skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_security_check_is_user_authorized_and_semgrep_required(self) -> None:
        skill = (SECURITY_CHECK_ROOT / "SKILL.md").read_text()
        metadata = (SECURITY_CHECK_ROOT / "agents" / "openai.yaml").read_text()

        self.assertIn("partial mode", skill)
        self.assertIn("only files changed by the relevant", skill)
        self.assertIn("comprehensive mode", skill)
        self.assertIn("without narrowing its scope", skill)
        self.assertIn("must not run one automatically", skill)
        self.assertIn("Semgrep is mandatory in both modes", skill)
        self.assertIn("in addition to Semgrep, not instead of it", skill)
        self.assertIn("report the check as incomplete", skill)
        self.assertIn("severity, and confidence", skill)
        self.assertIn("false positives", skill)
        self.assertIn("clean scan does not prove", skill)
        self.assertIn("corrective slice", skill)
        self.assertIn("Do not implement a correction", skill)
        self.assertIn('value: "semgrep"', metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_copy_agents_requires_an_approved_semantic_merge(self) -> None:
        skill = (COPY_AGENTS_ROOT / "SKILL.md").read_text()
        metadata = (COPY_AGENTS_ROOT / "agents" / "openai.yaml").read_text()

        self.assertIn("`../../AGENTS.md`", skill)
        self.assertIn("semantic merge", skill)
        self.assertIn("complete proposed `AGENTS.md`", skill)
        self.assertIn("Wait for explicit approval", skill)
        self.assertIn("will not automatically synchronize", skill)
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
                        "skills/commit/SKILL.md",
                        "skills/commit/agents/openai.yaml",
                        "skills/copy-agents/SKILL.md",
                        "skills/copy-agents/agents/openai.yaml",
                        "skills/git-status/SKILL.md",
                        "skills/git-status/agents/openai.yaml",
                        "skills/next-slice/SKILL.md",
                        "skills/next-slice/agents/openai.yaml",
                        "skills/planning/SKILL.md",
                        "skills/planning/agents/openai.yaml",
                        "skills/recover-project-context/SKILL.md",
                        "skills/recover-project-context/agents/openai.yaml",
                        "skills/security-check/SKILL.md",
                        "skills/security-check/agents/openai.yaml",
                        "skills/troubleshoot/SKILL.md",
                        "skills/troubleshoot/agents/openai.yaml",
                    ],
                    archive.namelist(),
                )


if __name__ == "__main__":
    unittest.main()
