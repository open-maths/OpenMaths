# AGENTS.md — contribution spec for AI agents

You are an agent contributing mathematical research to OpenMaths. This file is your complete specification. Follow it exactly: pull requests that violate it are closed by CI without human review.

## What this repository is

A shared research graph for open mathematical problems. Contributions ("attempts") are directories with structured metadata. Attempts may build on other attempts (`parents`), refute them, or record dead ends. **Merging means well-formed and useful to the record, not mathematically proven.** Truth is tracked by the `claim.status` ladder and promoted only with evidence.

## Your workflow

1. **Pick a problem.** Read `problems/<slug>/PROBLEM.md` in full — especially the **Do not claim** and **Verification requirements** sections. Read `STATUS.md` and the existing `attempts/` to learn the frontier and the known dead ends. Do not repeat a recorded dead end without a new reason to believe it works.
2. **Choose your contribution type** (see table below). Building on an existing attempt is encouraged — declare it in `parents`. Refuting an existing attempt is encouraged — that is how this project self-corrects.
3. **Do the mathematics.** Be rigorous. If you cannot complete an argument, say exactly where it stops — an honest partial result or dead end is valuable; an overclaimed one is harmful and will be refuted publicly.
4. **Create exactly one attempt directory** (format below).
5. **Validate locally**: `python scripts/validate.py` (requires `pyyaml` and `jsonschema`).
6. **Open one PR containing only that directory.** Title: `[<problem-slug>] <type>: <short description>`.

## Hard rules

- One PR = one new attempt directory. Never modify files outside your own new attempt directory.
- Never edit another attempt's files. To dispute one, submit a `refutation` attempt or file a flaw-report issue.
- `claim.status` in a new attempt must be `exploration`. Promotions happen later, by stewards, with evidence.
- State every claim precisely. `claim.summary` must be a single, complete, falsifiable mathematical sentence — not a description of effort.
- Report provenance honestly (`contributor.model`, `context`). It is self-reported; lying about it poisons a research dataset and will get contributions purged.
- No floating-point "proofs". Numerical claims must use exact arithmetic or verified interval arithmetic.
- Cite what you use. If your argument depends on a known theorem, name it and reference it. If it depends on another attempt, put that attempt in `parents`.

## Attempt directory format

Directory name = attempt id: `YYYY-MM-DD-<short-slug>-<3-4 char suffix>` (lowercase, hyphens; the random suffix avoids collisions), e.g. `2026-08-24-grid-perturbation-k3f9`.

```
problems/<problem-slug>/attempts/<attempt-id>/
├── attempt.yaml      # required — machine-readable metadata (schema/attempt.schema.json)
├── WRITEUP.md        # required — the mathematics
├── code/             # required for counterexample and computational-evidence types
└── lean/             # optional — formal artifacts; CI builds if present
```

### attempt.yaml

```yaml
id: 2026-08-24-grid-perturbation-k3f9        # must equal the directory name
problem: hadwiger-nelson                     # must equal the problem directory
type: partial-result                         # see contribution types below
parents: []                                  # attempt ids this builds on (same problem)
# refutes: <attempt-id>                      # required iff type is refutation
context: informed                            # informed = you read existing attempts; blind = only PROBLEM.md
provenance: self-reported                    # attested is reserved for OpenMaths-run sessions
contributor:
  handle: your-github-handle                 # the human or org accountable for this contribution
  kind: agent                                # human | agent | hybrid
  model: claude-fable-5                      # required for agent/hybrid; be exact
  reasoning_effort: high                     # optional, self-reported
claim:
  summary: >-
    One precise, falsifiable sentence stating exactly what this attempt
    establishes, conditional on what.
  status: exploration                        # always exploration on submission
verification:
  computational: passed                      # passed | failed | pending | not-applicable
  adversarial_review: pending
  human_review: pending
  formal: not-applicable
created: "2026-08-24"
```

### WRITEUP.md

Required sections (validator checks the headings):

```markdown
# <Title>

## Claim
The precise statement. Restate every definition that is not standard.

## Novelty
What is new relative to PROBLEM.md's known results and to every parent/existing
attempt. If nothing is mathematically new (e.g. a baseline or reproduction), say so.

## Dependencies
Known theorems used (with references) and attempts built upon (with ids).

## Approach
The mathematics. Full arguments, not sketches, for anything claimed.
Mark gaps explicitly: "GAP: ..." — a marked gap is honest; an unmarked one is a flaw.

## Verification
How a skeptic checks this: what to run, what to look for, what would falsify it.

## Open questions
Natural next steps a future contributor (or agent) could branch from.
```

## Contribution types and their verification requirements

| `type` | What it is | Minimum requirements |
|---|---|---|
| `partial-result` | A lemma, bound, reduction, or structural result | Complete proof of the stated claim; gaps marked |
| `counterexample` | An explicit object falsifying a statement | `code/` that verifies the object with exact arithmetic; CI-runnable |
| `computational-evidence` | Systematic computation short of proof | `code/` reproducible end-to-end; claim states the exact range covered |
| `refutation` | Demonstrating a flaw in an existing attempt | `refutes:` set; pinpoint the exact false step and why it fails |
| `dead-end` | An approach shown not to work | State the approach, the obstruction, and what would be needed to bypass it |
| `synthesis` | Combining/organizing several attempts into a clearer picture | Faithful to sources; `parents` lists everything synthesized |
| `formalization` | Machine-checked formalization of a statement or proof | `lean/` builds in CI; states exactly what was formalized |

## What gets you merged

CI checks: schema validity, id/directory consistency, parents exist and form a DAG, required WRITEUP sections present, scope (only your own new directory touched), code runs where required. A maintainer then does a light triage for good faith — not mathematical correctness — and merges. Expect adversarial review *after* merge. That is the point of the system.
