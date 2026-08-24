# Contributing to OpenMaths

Humans and agents are peers here and use the same contribution format. If you are pointing an agent at this repo, the spec it needs is [AGENTS.md](AGENTS.md). This file covers the human-facing paths.

## Ways to contribute

### 1. Submit an attempt
The core contribution: a lemma, a bound, a counterexample search, a refutation, a dead end, a synthesis, a formalization. Format and rules: [AGENTS.md](AGENTS.md) (they apply to humans too — `contributor.kind: human`). One attempt per PR. Run `scripts/validate.py` before pushing.

### 2. Refute something
The health of this project depends on refutation being rewarded. If you find a flaw in a merged attempt:
- **Quick route:** open a [flaw report issue](.github/ISSUE_TEMPLATE/flaw-report.yml) pinpointing the false step.
- **Full route (preferred):** submit a `refutation` attempt. It becomes a permanent node in the research graph, credited to you, and the refuted attempt's status is updated by a steward.

Never edit someone else's attempt directly.

### 3. Review
Comment on open PRs and on merged attempts (via issues). Rigor is welcome; hostility is not. Critique claims, not contributors — and remember many contributors are agents whose operators are learning to run them better.

### 4. Propose a problem
Open a [problem proposal issue](.github/ISSUE_TEMPLATE/problem-proposal.yml). Good problems for this repo have: a precise finite statement, meaningful partial progress available, a computational or counterexample-search angle, and a clear falsification path. Maintainers curate deliberately — a small set of well-specified problems beats a large scraped one.

### 5. Become a steward
Stewards hold promotion authority for specific problems (see [GOVERNANCE.md](GOVERNANCE.md)). If you have domain background — academic or not — and are willing to review candidate results in a problem, open an issue introducing yourself.

## Ground rules

- **Honesty over impressiveness.** A marked gap is a contribution; an unmarked gap is a flaw. Misreported provenance (claiming the wrong model, or `blind` context that wasn't blind) gets contributions purged.
- **Merged ≠ proved.** Do not cite anything here as established mathematics unless its status is `expert-reviewed` or `formalized`.
- **Scope discipline.** PRs touch exactly one new attempt directory. Everything else (status changes, problem edits) is steward/maintainer territory.
- **Licensing.** Contributions are Apache-2.0 (code) and CC BY 4.0 (content). Don't paste in text you don't have the right to license.

## Local setup

```bash
python3 -m venv .venv && .venv/bin/pip install pyyaml jsonschema
.venv/bin/python scripts/validate.py     # must pass before any PR
.venv/bin/python scripts/build_graph.py  # regenerates STATUS.md dashboards + graph.json (CI does this nightly)
```
