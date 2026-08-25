import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
VALID_ATTEMPT = {
    "id": "2026-08-24-schema-test-a1b2",
    "problem": "test-problem",
    "type": "partial-result",
    "parents": [],
    "context": "informed",
    "contributor": {"kind": "human"},
    "claim": {
        "summary": "Every object satisfying hypothesis H also satisfies conclusion C.",
        "status": "exploration",
    },
    "verification": {
        "computational": "not-applicable",
        "adversarial_review": "pending",
        "human_review": "pending",
        "formal": "not-applicable",
    },
    "created": "2026-08-24",
}


class AttemptSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads((ROOT / "schema" / "attempt.schema.json").read_text())
        cls.validator = Draft202012Validator(schema)

    def test_non_refutation_cannot_set_refutes(self):
        attempt = copy.deepcopy(VALID_ATTEMPT)
        attempt["refutes"] = "2026-08-24-parent-a1b2"
        self.assertFalse(self.validator.is_valid(attempt))

    def test_refutation_requires_refutes(self):
        attempt = copy.deepcopy(VALID_ATTEMPT)
        attempt["type"] = "refutation"
        self.assertFalse(self.validator.is_valid(attempt))

    def test_refutation_with_target_is_valid(self):
        attempt = copy.deepcopy(VALID_ATTEMPT)
        attempt["type"] = "refutation"
        attempt["refutes"] = "2026-08-24-parent-a1b2"
        self.assertTrue(self.validator.is_valid(attempt))


if __name__ == "__main__":
    unittest.main()
