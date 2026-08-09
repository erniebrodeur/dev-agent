from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "submission" / "test-cases.json"
EXPECTED_IDS = (
    "activate-recover",
    "plan-json-list",
    "implement-check-script",
    "diagnose-invalid-json",
    "prepare-json-commit",
    "run-existing-check",
    "explain-bootstrap",
    "recommend-security-check",
)


class SubmissionCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(CASES_PATH.read_text())
        cls.cases = cls.document["cases"]

    def test_submission_has_five_positive_and_three_negative_cases(self) -> None:
        self.assertEqual(1, self.document["schema_version"])
        self.assertEqual(EXPECTED_IDS, tuple(case["id"] for case in self.cases))
        self.assertEqual(
            {"positive": 5, "negative": 3},
            {
                kind: sum(case["kind"] == kind for case in self.cases)
                for kind in ("positive", "negative")
            },
        )

    def test_cases_define_submission_and_fixture_contracts(self) -> None:
        prompts = []

        for case in self.cases:
            with self.subTest(case=case["id"]):
                prompts.append(case["prompt"])
                self.assertTrue(case["prompt"].strip())
                fixture = case["fixture"]
                self.assertTrue(fixture["repository_state"].strip())
                self.assertGreaterEqual(len(fixture["proof_points"]), 1)
                self.assertTrue(all(point.strip() for point in fixture["proof_points"]))

                if case["kind"] == "positive":
                    self.assertTrue(case["expected_workflow"].strip())
                    self.assertTrue(case["result_shape"].strip())
                else:
                    self.assertTrue(case["safe_fallback"].strip())
                    self.assertTrue(case["rationale"].strip())

        self.assertEqual(len(prompts), len(set(prompts)))

    def test_bootstrap_case_is_informational(self) -> None:
        bootstrap = next(
            case for case in self.cases if case["id"] == "explain-bootstrap"
        )

        self.assertEqual(
            "How would I make Pilot's policy and skills part of this repository "
            "for future tasks?",
            bootstrap["prompt"],
        )
        self.assertIn("Do not invoke the skill or modify files", bootstrap["safe_fallback"])


if __name__ == "__main__":
    unittest.main()
