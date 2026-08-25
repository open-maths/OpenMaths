# Research and Repository Workflow

Use this reference to navigate the research graph, choose a useful contribution, prepare mathematical work, or review an existing claim.

## Repository Map

| Path | Role | How to use it |
|---|---|---|
| `README.md` | Project orientation | Learn the model, available problems, installation, and trust ladder. |
| `AGENTS.md` | Attempt submission rules | Read in full before creating or publishing an attempt. |
| `CONTRIBUTING.md` | Contribution paths | Decide between discussion, issue, attempt, review, or stewardship. |
| `GOVERNANCE.md` | Trust and authority | Interpret statuses, evidence requirements, and steward actions. |
| `problems/<slug>/PROBLEM.md` | Curated mathematical specification | Treat its statement, known results, traps, subproblems, and verification requirements as the problem contract. |
| `problems/<slug>/problem.yaml` | Problem metadata | Read status, area, tags, references, and current stewards. |
| `problems/<slug>/STATUS.md` | Generated frontier index | Use it to locate attempts and see the status summary; do not edit it. |
| `problems/<slug>/attempts/<id>/` | Durable research node | Read metadata, writeup, and evidence together. |
| `graph.json` | Generated machine index | Query attempt types, statuses, parents, refutations, and claims across problems. |
| `schema/` | Machine-enforced metadata contracts | Consult when constructing or changing YAML metadata. |
| `scripts/` | Validation and graph tooling | Run locally; distinguish structural checks from mathematical verification. |
| `.github/` | Collaboration and automation | Read issue forms, PR template, and CI behavior. |

The files record mathematics; Git records revisions; `parents` and `refutes` record mathematical relationships. Do not infer research ancestry from commit or branch history.

## Read the Research Frontier

1. Read the chosen `PROBLEM.md` completely. Extract the exact statement, recognized progress, strongest baseline, explicit non-results, useful subproblems, and verification standard.
2. Read `STATUS.md` as an index. Use `graph.json` and `attempt.yaml` files to identify parent chains, refutations, dead ends, syntheses, and claims near the proposed direction.
3. Read the relevant `WRITEUP.md` files and their code or formal artifacts. Metadata summarizes a claim; it does not replace the argument.
4. Search repository text for the central objects, lemmas, residue classes, constructions, or algorithms. This catches related work whose title or type is not obvious.
5. Inspect relevant Discussions, issues, and open or closed PRs for unmerged ideas, objections, and coordination. Treat them as context until incorporated into the research record.
6. Verify external references before relying on them. Cite the theorem or result actually used, not a nearby survey claim.

Useful local queries:

```bash
rg -n "<term|lemma|construction>" problems graph.json
find problems/<problem-slug>/attempts -name attempt.yaml -print
python3 scripts/build_graph.py --check
```

## Choose the Right Mathematical Contribution

Select the type from the result in hand:

- Use `partial-result` for a proved lemma, reduction, bound, or structural statement—not an unfinished route toward one.
- Use `computational-evidence` for a reproducible finite range or systematic experiment whose claim states its exact coverage.
- Use `counterexample` for an explicit falsifying object with exact verification.
- Use `refutation` when a precise step in a recorded attempt fails; set `refutes` and cite that attempt.
- Use `dead-end` when the contribution is a rigorous obstruction explaining why an approach cannot work as tried.
- Use `synthesis` to organize recorded attempts faithfully; include every synthesized attempt in `parents`.
- Use `formalization` for a machine-checked artifact whose build entrypoint runs in CI.

If the work is still a question, strategy, or proposed direction, use a Discussion or focused issue instead of manufacturing an attempt claim.

## Start a New Mathematical Attempt

Read `AGENTS.md` for the required directory and fields. Then:

1. Choose a descriptive attempt id with the current date and a collision-resistant suffix.
2. Set `parents` to attempts whose results or methods the work actually uses. For a refutation, also set `refutes` to the challenged attempt.
3. Write `claim.summary` after the mathematics is complete enough to know what was established. Make it a single falsifiable sentence with conditions and finite ranges included.
4. In `Novelty`, compare against `PROBLEM.md`, parent attempts, relevant siblings, and known literature. Say plainly when the value is reproduction or infrastructure rather than a new theorem.
5. In `Approach`, prove everything needed for the claim and label every unresolved step `GAP:`. Narrow the claim if a gap blocks it.
6. Make verification adversarial: say what would falsify the claim, include exact checks, and make runners reproducible from their own directory.
7. Keep metadata honest. `claim.status` starts at `exploration`; verification fields describe checks actually performed, not expected future success.

For a suffix when one is needed:

```bash
python3 -c 'import secrets; print(secrets.token_hex(2))'
```

## Reproduce, Extend, or Refute Work

- **Reproduce:** derive or verify the claim independently; explain what was independent and what artifacts were reused.
- **Extend:** declare the source attempt in `parents`, state the additional conclusion precisely, and avoid re-claiming the parent's result as novelty.
- **Refute:** identify the exact statement or proof step, show why it fails, and explain whether the main claim survives. Prefer a concrete counterexample to a vague objection.
- **Repair:** preserve the flawed attempt and create a child attempt containing the corrected claim and proof. A repair does not erase the historical flaw.

## Verify the Result

Install the pinned development dependencies in an isolated environment, then run structural validation:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

Run the attempt's own entrypoint from its artifact directory:

```bash
(cd problems/<problem-slug>/attempts/<attempt-id>/code && bash run.sh)
# or
(cd problems/<problem-slug>/attempts/<attempt-id>/lean && bash run.sh)
```

A passing validator proves repository structure. A passing runner proves only the checks encoded by that runner. Neither establishes an unencoded mathematical argument.

## Hand Off Clearly

Report:

- the selected problem and contribution path;
- the exact claim, type, parents, and novelty;
- known gaps, assumptions, and external dependencies;
- verification commands and results;
- the changed paths and current branch;
- relevant Discussions, issues, or PRs;
- any proposed external action still awaiting authorization.
