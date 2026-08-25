# OpenMaths

Read [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md) to understand the project and its collaboration paths. Before preparing a mathematical attempt, read [AGENTS.md](AGENTS.md) completely. For repository development, read [DEVELOPMENT.md](DEVELOPMENT.md). Consult [GOVERNANCE.md](GOVERNANCE.md) when interpreting or changing claim status.

The [`openmaths-contribute`](plugins/openmaths/skills/openmaths-contribute/SKILL.md) skill provides the repository and GitHub contribution interface. The problem file is sufficient to begin mathematical work.

Quick validation before opening a PR:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python scripts/run_attempt_checks.py
```
