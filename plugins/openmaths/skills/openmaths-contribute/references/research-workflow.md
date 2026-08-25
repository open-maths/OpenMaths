# OpenMaths Repository Reference

Use this reference when repository structure or the attempt format matters. It is a map, not a required research sequence.

## Files and Folders

| Path | Purpose |
|---|---|
| `problems/<slug>/PROBLEM.md` | Mathematical statement, known results, warnings, and verification requirements. |
| `problems/<slug>/problem.yaml` | Problem metadata. |
| `problems/<slug>/STATUS.md` | Generated index of recorded attempts and statuses. |
| `problems/<slug>/attempts/<id>/` | Immutable mathematical contribution. |
| `graph.json` | Generated machine-readable index of problems, attempts, parents, and refutations. |
| `schema/` | Metadata contracts enforced by CI. |
| `scripts/validate.py` | Repository and contribution-scope validator. |
| `scripts/run_attempt_checks.py` | Runs attempt verification entrypoints. |
| `AGENTS.md` | Authoritative attempt submission rules. |
| `GOVERNANCE.md` | Claim-status and steward rules. |

Only `PROBLEM.md` is required to begin mathematical work. `STATUS.md` and `graph.json` are convenient indexes. Read an attempt's `attempt.yaml`, `WRITEUP.md`, and artifacts when using, extending, reproducing, reviewing, or refuting it. Search broader history only to the extent needed for the claim being made.

Git history records file revisions. Mathematical ancestry is expressed by `parents` and `refutes` in attempt metadata.

## Contribution Types

| Type | Use |
|---|---|
| `partial-result` | Proved lemma, reduction, bound, or structural result. |
| `counterexample` | Explicit falsifying object with exact verification. |
| `computational-evidence` | Reproducible finite computation short of proof. |
| `refutation` | A precise flaw in an existing attempt. |
| `dead-end` | A rigorous obstruction to an approach. |
| `synthesis` | Faithful organization of several attempts. |
| `formalization` | Machine-checked statement or proof. |

Choose the type from what the work establishes. It is acceptable to do exploratory work without creating an attempt.

## Attempt Essentials

The directory id has the form `YYYY-MM-DD-<short-slug>-<suffix>`. Its required files and metadata are specified in `AGENTS.md` and `schema/attempt.schema.json`.

When relevant:

- list in `parents` only attempts the result actually uses;
- set `refutes` for a refutation;
- use `context: blind` when only the problem description was read, otherwise `informed`;
- state the limits of any novelty search;
- distinguish executable checks from prose arguments;
- keep generated `STATUS.md` and `graph.json` out of the attempt PR.

Validate with:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
(cd problems/<problem-slug>/attempts/<attempt-id>/code && bash run.sh)
# or use lean/run.sh for a formalization
```
