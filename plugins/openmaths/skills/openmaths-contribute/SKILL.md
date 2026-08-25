---
name: openmaths-contribute
description: Work on mathematical problems and contribute results in the open-maths/OpenMaths repository. Use for understanding its problem format, locating research artifacts, preparing or reviewing attempts, and using Git or GitHub for OpenMaths collaboration; do not use for repository development or unrelated GitHub work.
license: Apache-2.0
---

# Work on OpenMaths

OpenMaths is a repository of mathematical problem descriptions and independently contributed attempts. Help the user work on the mathematics using whatever approach is appropriate. The repository defines how durable results are recorded; it does not prescribe a research method.

## Begin with the Problem

- Reuse a suitable checkout, or clone `open-maths/OpenMaths` if local files or verification are needed.
- Read the selected `problems/<slug>/PROBLEM.md` in full. That is sufficient to begin work.
- Use `STATUS.md`, existing attempts, `graph.json`, literature, Discussions, issues, or pull requests when they are relevant to the task. Do not load them by default.
- Read [references/research-workflow.md](references/research-workflow.md) when repository paths, attempt types, relationships, or validation details are needed.
- Read [references/github-workflow.md](references/github-workflow.md) only when GitHub context, branches, commits, issues, Discussions, or pull requests are involved.

## Collaborate Freely

Solving a problem independently is only one form of contribution. Depending on the work, help the user or agent:

- explore the mathematics without first surveying the whole repository;
- join or start a Discussion about an idea, question, or competing approach;
- use an issue for a focused subproblem, flaw report, or problem proposal;
- review, reproduce, extend, synthesize, or refute existing work; or
- preserve a durable result as an attempt.

Choose the surface that fits the contribution. Do not force early exploration into an attempt, and do not require a prescribed reading or research sequence.

## Share Useful Work Before Finishing

Do not leave a recordable mathematical result only in the chat. When the work produces a rigorous partial result, counterexample, reproducible computation, refutation, informative dead end, synthesis, or formalization, the default completion path is to create and validate an attempt. Inspect the final diff and, when GitHub publication is already authorized, commit, push, and open the attempt pull request before finishing the task.

If the work is useful but not attempt-ready, turn it into a concise proposed Discussion post or issue when that would advance collaboration. Do not manufacture a contribution from inconclusive scratch work.

Before creating an attempt, read `AGENTS.md`; it is authoritative. Preserve these essentials:

- An attempt PR contains one new attempt directory and nothing outside it.
- Never edit a merged attempt. Extend it through `parents`, or challenge it with a refutation attempt or flaw issue.
- New attempts start with `claim.status: exploration`.
- State a precise, falsifiable claim and mark every known gap.
- Report contributor provenance and research context honestly.
- Cite the theorems and attempts actually used.
- Use exact or verified interval arithmetic for numerical claims.
- Include reproducible code or formal artifacts when the contribution type requires them.

Run `python3 scripts/validate.py` and the attempt's `code/run.sh` or `lean/run.sh`, when present. These checks establish structure and encoded computations, not mathematical truth.

If GitHub publication is not authorized, leave the local attempt or proposed post ready and ask before changing remote state.

## Use GitHub

Repository files are the durable mathematical record. Discussions are informal collaboration; issues track focused questions or flaws; pull requests review proposed records and status changes. Use whichever surface helps the task.

Read-only inspection does not require publication permission. A fork, push, issue, Discussion post, review, or pull request changes external state; perform it only when the user authorizes it. Do not merge or promote a claim without explicit authority and the evidence required by `GOVERNANCE.md`.
