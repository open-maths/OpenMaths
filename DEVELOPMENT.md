# Developing and Maintaining OpenMaths

This guide covers changes to the repository as a research platform. Mathematical attempts follow [AGENTS.md](AGENTS.md); claim-status changes follow [GOVERNANCE.md](GOVERNANCE.md).

## The Three Pull Request Lanes

| Lane | Purpose | Authority | Template |
|---|---|---|---|
| **Attempt PR** | Add a durable mathematical contribution | Any contributor, under `AGENTS.md` | `.github/PULL_REQUEST_TEMPLATE/attempt.md` |
| **Steward PR** | Promote, demote, refute, or withdraw recorded claim status | Stewards or maintainers, under `GOVERNANCE.md` | `.github/PULL_REQUEST_TEMPLATE/steward.md` |
| **Project PR** | Improve documentation, schemas, tooling, CI, skills, templates, or problem infrastructure | Contributors and maintainers, under this guide | `.github/PULL_REQUEST_TEMPLATE/project.md` |

Do not combine lanes. In particular, a project PR does not modify attempt directories; an attempt PR does not carry drive-by tooling or documentation changes. This keeps mathematical review, governance decisions, and software maintenance independently reviewable.

## What Belongs in a Project PR

- Documentation, onboarding, contributor experience, and licensing.
- Metadata schemas, validators, policy tests, and reproducibility runners.
- Research-graph generation, dashboards, and repository automation.
- GitHub Actions, issue forms, pull request templates, and repository configuration stored in Git.
- The distributable agent skill and plugin manifests.
- Problem templates and curated problem specifications, when the contributor has the appropriate maintainer or steward context.
- Governance changes, subject to the discussion period and authority rules in `GOVERNANCE.md`.

A mathematical correction to a merged attempt is not maintenance. Use a flaw report, refutation attempt, or steward status PR instead.

## Plan the Change

Search existing Discussions, issues, and pull requests before starting. Small fixes can go directly to a focused project PR. Open an issue or Discussion first when a change alters contributor policy, metadata compatibility, governance, the status model, or several repository surfaces.

State the behavior being improved, who experiences the problem, and the invariant that must remain true. For policy changes, update the documentation, validator, tests, templates, and distributed skill together when they express the same rule.

## Branches and Titles

Start a short-lived branch from the current upstream `main` branch. Preferred conventions:

| Area | Branch | PR title |
|---|---|---|
| Documentation | `docs/<short-description>` | `docs: <reader-visible improvement>` |
| Validation or schema | `tooling/<short-description>` | `tooling: <enforced behavior>` |
| CI or automation | `ci/<short-description>` | `ci: <workflow outcome>` |
| Agent skill or plugin | `skill/<short-description>` | `skill: <agent behavior>` |
| Problem specification | `problem/<problem-slug>/<short-description>` | `problem(<problem-slug>): <change>` |
| Governance | `governance/<short-description>` | `governance: <policy change>` |

These are clarity conventions, not mathematical ancestry. Attempt relationships live in `parents` and `refutes`.

## Development Rules

- Preserve unrelated work and stage explicit paths.
- Do not hand-edit generated `STATUS.md` files or `graph.json`; change the generator and verify its output.
- Keep schema changes compatible with the existing research record. A repository-wide migration requires an explicit maintainer design and corresponding scope-policy change; do not rewrite attempts ad hoc.
- Add or update regression tests when validator, scope, schema, runner-selection, or graph behavior changes.
- Keep documentation, examples, issue forms, PR templates, and agent instructions consistent with enforced behavior.
- Pin development dependencies deliberately and avoid adding services or credentials when local files and GitHub already solve the problem.
- Treat publishing a plugin release, changing repository settings, and posting GitHub content as separate external actions requiring authorization.

## Validation Matrix

Run the checks relevant to the changed surface:

| Surface | Minimum checks |
|---|---|
| Documentation or templates | Relative-link check, YAML parse where applicable, `git diff --check` |
| Problem specification or metadata | `.venv/bin/python scripts/validate.py`, `.venv/bin/python scripts/build_graph.py --check` |
| Schema or validator | Unit tests, repository validator, graph dry-run |
| Runner or CI behavior | Unit tests and `.venv/bin/python scripts/run_attempt_checks.py` |
| Skill or plugin | Skill validator, Agent Plugin schema, Claude plugin/marketplace validation, GitHub skill dry-run |
| Graph generator | Unit tests where behavior changes, graph dry-run, inspect generated diff in an isolated or disposable checkout |

Use the pinned dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/validate.py
.venv/bin/python scripts/build_graph.py --check
```

## Project PR Handoff

Use `.github/PULL_REQUEST_TEMPLATE/project.md` as the PR body guide. The default pull request template is only a lane selector and compact fallback.

Explain:

- the repository behavior or maintenance problem;
- the chosen design and user-visible effect;
- files and workflows affected;
- compatibility or migration considerations;
- validation performed and anything that could not be tested locally;
- related Discussions or issues;
- follow-up work that is intentionally out of scope.

Maintainers review project PRs for correctness, maintainability, compatibility with the research record, and consistency across human and agent workflows.
