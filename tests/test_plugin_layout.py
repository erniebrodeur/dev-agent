from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = ROOT / "plugins" / "pilot"
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
POLICY_PATH = PLUGIN_ROOT / "AGENTS.md"
ACTIVATE_ROOT = PLUGIN_ROOT / "skills" / "activate"
COMMIT_ROOT = PLUGIN_ROOT / "skills" / "commit"
BOOTSTRAP_REPO_WITH_AGENT_ROOT = (
    PLUGIN_ROOT / "skills" / "bootstrap-repo-with-agent"
)
GIT_STATUS_ROOT = PLUGIN_ROOT / "skills" / "git-status"
HELP_ROOT = PLUGIN_ROOT / "skills" / "help"
RECOVER_CONTEXT_ROOT = PLUGIN_ROOT / "skills" / "recover-project-context"
PLANNING_ROOT = PLUGIN_ROOT / "skills" / "planning"
NEXT_SLICE_ROOT = PLUGIN_ROOT / "skills" / "next-slice"
TROUBLESHOOT_ROOT = PLUGIN_ROOT / "skills" / "troubleshoot"
SECURITY_CHECK_ROOT = PLUGIN_ROOT / "skills" / "security-check"
UTILITY_BUILDER_ROOT = PLUGIN_ROOT / "skills" / "utility-builder"
PACKAGE_SCRIPT = ROOT / "scripts" / "package-plugin"


def skill_description(skill_root: Path) -> str:
    frontmatter = (skill_root / "SKILL.md").read_text().split("---\n", 2)[1]
    return next(
        line.removeprefix("description: ")
        for line in frontmatter.splitlines()
        if line.startswith("description: ")
    )


class PluginLayoutTests(unittest.TestCase):
    def test_manifest_identity_matches_plugin_directory(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text())

        self.assertEqual(PLUGIN_ROOT.name, manifest["name"])
        self.assertEqual("1.0.1", manifest["version"])
        self.assertEqual("./skills/", manifest["skills"])
        self.assertNotIn("apps", manifest)
        self.assertNotIn("mcpServers", manifest)
        self.assertEqual("GPL-3.0-only", manifest["license"])
        self.assertEqual("Ernie Brodeur", manifest["author"]["name"])
        self.assertEqual("ebrodeur@ujami.net", manifest["author"]["email"])
        self.assertEqual(
            "https://erniebrodeur.github.io/pilot/",
            manifest["homepage"],
        )
        self.assertEqual(
            "https://github.com/erniebrodeur/pilot",
            manifest["repository"],
        )
        interface = manifest["interface"]
        self.assertEqual("Ernie Brodeur", interface["developerName"])
        self.assertEqual("Developer Tools", interface["category"])
        self.assertEqual(["Interactive", "Write"], interface["capabilities"])
        self.assertEqual(3, len(interface["defaultPrompt"]))
        for field in ("composerIcon", "logo"):
            self.assertTrue((PLUGIN_ROOT / interface[field]).is_file())

    def test_activate_matches_activation_requests_and_loads_canonical_policy(self) -> None:
        skill = (ACTIVATE_ROOT / "SKILL.md").read_text()
        metadata = (ACTIVATE_ROOT / "agents" / "openai.yaml").read_text()

        self.assertTrue(POLICY_PATH.is_file())
        self.assertIn("`../../AGENTS.md`", skill)
        self.assertIn("`../../../AGENTS.md`", skill)
        self.assertIn("repository-owned copy", skill)
        self.assertIn("`../recover-project-context/SKILL.md`", skill)
        self.assertIn("Activation is incomplete until", skill)
        self.assertIn("Do not report Pilot as active", skill)
        self.assertIn("mandatory and blocking", skill)
        self.assertIn("Do not defer project-context recovery", skill)
        self.assertIn("asks to activate Pilot", skill)
        self.assertIn("selects the Pilot plugin", skill)
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
        self.assertIn("Pilot convention", skill)
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

        self.assertIn("choosing or defining future software work", skill)
        self.assertIn("`../recover-project-context/SKILL.md`", skill)
        self.assertIn("CURRENT_WORK.md", skill)
        self.assertIn("provisional", skill)
        self.assertIn("settled", skill)
        self.assertIn("correction", skill)
        self.assertIn("explicit approval", skill)
        self.assertIn("Do not implement", skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_skill_descriptions_define_distinct_routing_owners(self) -> None:
        descriptions = {
            "planning": skill_description(PLANNING_ROOT).lower(),
            "recover": skill_description(RECOVER_CONTEXT_ROOT).lower(),
            "next-slice": skill_description(NEXT_SLICE_ROOT).lower(),
            "troubleshoot": skill_description(TROUBLESHOOT_ROOT).lower(),
            "commit": skill_description(COMMIT_ROOT).lower(),
            "bootstrap-repo-with-agent": skill_description(
                BOOTSTRAP_REPO_WITH_AGENT_ROOT
            ).lower(),
            "utility-builder": skill_description(UTILITY_BUILDER_ROOT).lower(),
        }
        contracts = [
            (
                "Where are we, what's left, and what is already planned next?",
                "recover",
                (
                    "already-established current state",
                    "what remains in an existing plan",
                    "planned next work",
                ),
            ),
            (
                "What future work should we define next?",
                "planning",
                ("choosing or defining future software work", "unsettled idea"),
            ),
            (
                "Implement the approved corrective slice.",
                "next-slice",
                ("approved corrective slice",),
            ),
            (
                "Implement the approved slice that creates our deploy script.",
                "next-slice",
                ("approved slice that creates or changes a repository utility",),
            ),
            (
                "This behavior fails and has no approved correction.",
                "troubleshoot",
                ("undiagnosed concrete failure", "no correction is already approved"),
            ),
            (
                "Prepare or stage these changes for a commit.",
                "commit",
                ("prepare or stage changes", "create a local commit"),
            ),
            (
                "$bootstrap-repo-with-agent: install Pilot policy in this project's AGENTS.md.",
                "bootstrap-repo-with-agent",
                (
                    "use only when the user explicitly invokes "
                    "`$bootstrap-repo-with-agent`",
                ),
            ),
            (
                "Create a reusable deployment script.",
                "utility-builder",
                ("create or change a repository-owned script", "repeatable, deterministic"),
            ),
        ]

        for prompt, owner, required_fragments in contracts:
            with self.subTest(prompt=prompt, owner=owner):
                for fragment in required_fragments:
                    self.assertIn(fragment, descriptions[owner])

        self.assertIn("already-established project state", descriptions["planning"])
        self.assertNotIn("or next work", descriptions["planning"])
        self.assertNotIn("no approved implementation slice", descriptions["planning"])
        self.assertIn("choose or design new future work", descriptions["recover"])
        self.assertIn("do not use to implement", descriptions["recover"])
        self.assertIn("do not use to diagnose a new failure", descriptions["next-slice"])
        self.assertIn(
            "during an active approved slice, `next-slice` owns",
            descriptions["troubleshoot"],
        )
        self.assertIn("possible commit message is read-only", descriptions["commit"])
        self.assertNotIn("proposes a commit message", descriptions["commit"])
        self.assertIn(
            "do not use merely to run an existing script",
            descriptions["utility-builder"],
        )
        self.assertIn(
            "or to build, test, deploy, release",
            descriptions["utility-builder"],
        )
        self.assertIn(
            "do not use to implement an approved implementation slice",
            descriptions["utility-builder"],
        )
        self.assertIn("`next-slice` owns that work", descriptions["utility-builder"])
        self.assertIn(
            "do not use for a natural-language request",
            descriptions["bootstrap-repo-with-agent"],
        )

        bootstrap_metadata = (
            BOOTSTRAP_REPO_WITH_AGENT_ROOT / "agents" / "openai.yaml"
        ).read_text()
        self.assertIn("allow_implicit_invocation: false", bootstrap_metadata)

    def test_portable_policy_defines_an_implementation_slice(self) -> None:
        policy = POLICY_PATH.read_text()

        self.assertIn("An implementation slice is", policy)
        self.assertIn("smallest coherent, independently reviewable unit", policy)
        self.assertIn("outcome, scope, constraints or invariants, non-goals", policy)
        self.assertIn("authorization boundary", policy)
        self.assertIn("Approval authorizes implementation of that slice only", policy)

    def test_policy_requires_evidence_before_fix_claims(self) -> None:
        policy = POLICY_PATH.read_text()
        authorization = policy.split("## Authorization\n", 1)[1].split(
            "\n## Questions and assumptions", 1
        )[0]
        proof = policy.split("## Proof\n", 1)[1].split("\n## Project memory", 1)[0]

        self.assertIn(
            "A request to fix a concrete failure authorizes diagnosis, not an unknown correction",
            authorization,
        )
        self.assertIn("Success depends on the problem", proof)
        self.assertIn("user accepts the result", proof)
        self.assertIn("current, relevant evidence", proof)
        self.assertIn("An edit or code inspection proves only that code changed", proof)
        self.assertIn("A passing test proves only", proof)
        self.assertIn("final relevant code, build, service, and environment", proof)
        self.assertIn("do not claim it is fixed", proof)
        self.assertIn("provide the concrete observed result", proof)
        self.assertNotIn("security check", proof.lower())

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
        self.assertIn("Success depends on the problem", skill)
        self.assertIn("final relevant code, build, service, and environment", skill)
        self.assertIn("implemented but unverified", skill)
        self.assertIn("provide the concrete observed result", skill)
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
        self.assertIn("authorizes diagnosis only", skill)
        self.assertIn("Do not report the failure as fixed or resolved", skill)
        self.assertNotIn("security checks", skill.lower())
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

    def test_bootstrap_repo_with_agent_requires_approved_bootstrap(self) -> None:
        skill = (BOOTSTRAP_REPO_WITH_AGENT_ROOT / "SKILL.md").read_text()
        metadata = (
            BOOTSTRAP_REPO_WITH_AGENT_ROOT / "agents" / "openai.yaml"
        ).read_text()

        self.assertIn("`../../AGENTS.md`", skill)
        self.assertIn("`.agents/skills/`", skill)
        self.assertIn("every Pilot skill except `bootstrap-repo-with-agent`", skill)
        self.assertIn("Before modifying anything", skill)
        self.assertIn("Ask whether this is the intended result", skill)
        self.assertIn("stop until the user explicitly confirms", skill)
        self.assertIn("semantic merge", skill)
        self.assertIn("complete proposed `AGENTS.md`", skill)
        self.assertIn("full skill inventory", skill)
        self.assertIn("Wait for explicit approval", skill)
        self.assertIn("will not automatically synchronize", skill)
        self.assertIn("Do not copy `bootstrap-repo-with-agent`", skill)
        self.assertIn("allow_implicit_invocation: false", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_utility_builder_owns_deterministic_repository_scripts(self) -> None:
        skill = (UTILITY_BUILDER_ROOT / "SKILL.md").read_text()
        metadata = (UTILITY_BUILDER_ROOT / "agents" / "openai.yaml").read_text()

        self.assertIn("repeatable and deterministic", skill)
        self.assertIn("token and context use", skill)
        self.assertIn("Ask whether the user wants the script built", skill)
        self.assertIn("Wait for explicit approval", skill)
        self.assertIn("Bash is always an acceptable implementation choice", skill)
        self.assertIn("repository's existing language and toolchain", skill)
        self.assertIn("`scripts/`", skill)
        self.assertIn("`cmd/`", skill)
        self.assertIn("complete authoritative procedure", skill)
        self.assertIn("test bundle", skill)
        self.assertIn("Use an existing repository script", skill)
        self.assertIn("does not authorize executing", skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("[TODO:", skill)

    def test_help_shows_canonical_guidance_only_in_pilot_context(self) -> None:
        skill = (HELP_ROOT / "SKILL.md").read_text()
        metadata = (HELP_ROOT / "agents" / "openai.yaml").read_text()
        guide = (HELP_ROOT / "references" / "help.md").read_text()

        self.assertIn("explicitly asks for Pilot help", skill)
        self.assertIn("Pilot is already active", skill)
        self.assertIn("Do not claim generic help requests", skill)
        self.assertIn("reproduce the guide verbatim", skill.lower())
        self.assertIn("Do not create or infer persistent activation state", skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertIn("Start here", guide)
        self.assertIn("Authorization boundaries", guide)
        self.assertIn("does not call a problem fixed", guide)
        self.assertIn("`$bootstrap-repo-with-agent`", guide)
        self.assertNotIn("unqualified", skill.lower())
        self.assertNotIn("unqualified", guide.lower())
        self.assertNotIn("[TODO:", skill)

    def test_marketplace_points_to_plugin(self) -> None:
        marketplace = json.loads(MARKETPLACE_PATH.read_text())
        entries = [entry for entry in marketplace["plugins"] if entry["name"] == "pilot"]

        self.assertEqual(1, len(entries))
        self.assertEqual(
            {"source": "local", "path": "./plugins/pilot"},
            entries[0]["source"],
        )
        self.assertEqual("AVAILABLE", entries[0]["policy"]["installation"])
        self.assertEqual("ON_INSTALL", entries[0]["policy"]["authentication"])

    def test_package_contains_exact_plugin_files_and_normalized_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "pilot.zip"
            object_directory = Path(directory) / "objects"
            object_directory.mkdir()
            environment = os.environ | {
                "GIT_INDEX_FILE": str(Path(directory) / "package-index"),
                "GIT_OBJECT_DIRECTORY": str(object_directory),
                "GIT_ALTERNATE_OBJECT_DIRECTORIES": str(ROOT / ".git" / "objects"),
            }

            subprocess.run(
                ["git", "read-tree", "HEAD"],
                cwd=ROOT,
                env=environment,
                check=True,
            )
            subprocess.run(
                ["git", "add", "plugins/pilot"],
                cwd=ROOT,
                env=environment,
                check=True,
            )
            subprocess.run(
                [PACKAGE_SCRIPT, archive_path],
                env=environment,
                check=True,
            )

            with zipfile.ZipFile(archive_path) as archive:
                expected_files = [
                    ".codex-plugin/plugin.json",
                    "AGENTS.md",
                    "assets/pilot-living-interface-logo.svg",
                    "skills/activate/SKILL.md",
                    "skills/activate/agents/openai.yaml",
                    "skills/bootstrap-repo-with-agent/SKILL.md",
                    "skills/bootstrap-repo-with-agent/agents/openai.yaml",
                    "skills/commit/SKILL.md",
                    "skills/commit/agents/openai.yaml",
                    "skills/git-status/SKILL.md",
                    "skills/git-status/agents/openai.yaml",
                    "skills/help/SKILL.md",
                    "skills/help/agents/openai.yaml",
                    "skills/help/references/help.md",
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
                    "skills/utility-builder/SKILL.md",
                    "skills/utility-builder/agents/openai.yaml",
                ]
                self.assertEqual(expected_files, archive.namelist())

                for name in expected_files:
                    with self.subTest(name=name):
                        info = archive.getinfo(name)
                        self.assertEqual((1980, 1, 1, 0, 0, 0), info.date_time)
                        self.assertEqual(3, info.create_system)
                        self.assertEqual(0o100644, info.external_attr >> 16)
                        self.assertEqual(
                            (PLUGIN_ROOT / name).read_bytes(),
                            archive.read(name),
                        )

    def test_package_excludes_ignored_files_and_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            script = repository / "scripts" / "package-plugin"
            plugin = repository / "plugins" / "pilot"
            manifest = plugin / ".codex-plugin" / "plugin.json"
            policy = plugin / "AGENTS.md"
            ignored = plugin / "private.secret"

            script.parent.mkdir(parents=True)
            manifest.parent.mkdir(parents=True)
            shutil.copy2(PACKAGE_SCRIPT, script)
            manifest.write_text("{}\n")
            policy.write_text("# Policy\n")
            ignored.write_text("not package content\n")
            (repository / ".gitignore").write_text("*.secret\n")

            subprocess.run(["git", "-C", repository, "init", "-q"], check=True)
            subprocess.run(
                ["git", "-C", repository, "add", ".gitignore", "scripts", "plugins"],
                check=True,
            )

            archive_path = repository / "dist" / "pilot.zip"
            subprocess.run([script, archive_path], check=True)

            with zipfile.ZipFile(archive_path) as archive:
                self.assertEqual(
                    [".codex-plugin/plugin.json", "AGENTS.md"],
                    archive.namelist(),
                )

            symlink = plugin / "policy-link"
            symlink.symlink_to("AGENTS.md")
            subprocess.run(["git", "-C", repository, "add", symlink], check=True)

            result = subprocess.run(
                [script, repository / "dist" / "with-symlink.zip"],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("symlink", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
