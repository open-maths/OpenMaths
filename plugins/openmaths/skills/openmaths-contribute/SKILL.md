---
name: openmaths-contribute
description: Participate in mathematical collaboration in the open-maths/OpenMaths research repository. Use when exploring its problems, running a long autonomous research campaign, reading research Discussions, issues, attempts, or pull requests, doing or reviewing mathematics, proposing subproblems, preparing attempts, or using Git and GitHub CLI for those workflows; do not use for unrelated mathematics, generic GitHub work, or repository development and maintenance.
license: Apache-2.0
---

# Collaborate on OpenMaths Research

Help the user understand and improve a shared mathematical research graph. Repository files hold the durable research record; GitHub hosts coordination and review. Treat newer repository instructions as authoritative over this packaged skill.

## Establish Project Context

- Reuse an appropriate checkout when one exists. Inspect its branch, remotes, and worktree before changing anything; preserve unrelated work.
- If no checkout exists, clone `open-maths/OpenMaths`. A fork, branch push, issue, discussion reply, or pull request changes external state and requires user authorization.
- Read `README.md` for orientation and `CONTRIBUTING.md` for mathematical contribution paths. Read `AGENTS.md` completely before preparing an attempt and `GOVERNANCE.md` before reviewing status evidence or proposing a promotion.
- Read [references/research-workflow.md](references/research-workflow.md) when exploring a problem, doing mathematics, preparing an attempt, reproducing work, or reviewing a claim.
- Read [references/research-campaign.md](references/research-campaign.md) before starting or resuming a multi-turn autonomous research campaign.
- Read [references/github-workflow.md](references/github-workflow.md) when inspecting community activity or working with Discussions, issues, branches, commits, forks, or pull requests.

## Understand the Three Layers

- **Research record:** `PROBLEM.md`, attempts, metadata, verification artifacts, and the generated graph. This is the mathematical source of truth.
- **Coordination:** Discussions hold early questions and strategy; issues hold focused proposals, subproblems, flaw reports, and steward applications.
- **Change review:** branches and pull requests propose changes. Git branch topology does not define mathematical ancestry—attempt `parents` and `refutes` do.

## Choose a Contribution Path

| Goal | Use | Read next |
|---|---|---|
| Understand the frontier or choose research | Repository files plus community context | `research-workflow.md`, then relevant parts of `github-workflow.md` |
| Work autonomously on one problem for many turns | Research campaign with a durable local notebook | `research-campaign.md`, then the other references as needed |
| Ask an open question or coordinate a direction | Discussion | `github-workflow.md` |
| Track a focused subproblem, flaw, problem proposal, or steward application | Issue form | `github-workflow.md` |
| Record a mathematical result, reproduction, refutation, synthesis, or dead end | Attempt PR | Both references and `AGENTS.md` |
| Change the status of a recorded claim | Steward PR | `GOVERNANCE.md` and `github-workflow.md` |
| Review unmerged work | Pull request | Both references |
| Challenge a merged claim | Flaw issue or refutation attempt | Both references |

## Explore a Problem

Start with the problem specification, especially what counts as progress, known results, traps, useful subproblems, and verification requirements. Use `STATUS.md` and `graph.json` as indexes, then read the underlying attempt metadata, writeups, and artifacts. Search relevant Discussions, issues, and pull requests for community context that has not entered the durable record.

Let the user choose among materially different problems or research directions. If asked to recommend one, compare concrete open subproblems, required expertise, available verification, existing dead ends, and likely novelty.

## Run an Autonomous Research Campaign

Use a persistent harness goal when the user wants the agent to keep working without step-by-step prompting. Agree on or infer a bounded target, budget, acceptable outcomes, verification standard, and stopping conditions. Keep resumable scratch notes under `.openmaths-work/<problem-slug>/`; this ignored workspace is not an attempt and must not leak into a PR.

Run a research loop that alternates construction and adversarial attack. Preserve failed approaches and exact obstructions, compare every surviving result with the recorded frontier, and checkpoint before context compaction or a change of direction. Do not manufacture an attempt merely because the run is ending. Package only the strongest durable outcome, and keep publication as a separate user-authorized action.

## Start a New Mathematical Attempt

Follow `AGENTS.md` for format and PR scope. Base the contribution type on what was actually established—not what the approach hoped to prove. State a falsifiable claim, cite dependencies and parent attempts, mark gaps, report provenance honestly, and use exact or verified arithmetic where required.

Prefer extending, reproducing, synthesizing, or refuting recorded work when that advances the frontier more clearly than beginning from scratch. Do not edit a merged attempt to repair it; create a new node that makes the relationship explicit.

## Read or Join a Discussion

Read the opening post and the full relevant thread before summarizing or responding. Trace mathematical claims back to repository artifacts or external references. Treat promising discussion content as leads, not established results. Use a specific title such as `[problem-slug] <research question or proposed direction>` when starting a research discussion.

Move durable mathematical outcomes into the appropriate repository form: an attempt for research work or a focused issue for an actionable question or flaw. Post or reply only when the user asks.

## Review or Challenge Existing Work

Identify whether the target is an open PR, a merged attempt, or an informal claim; each has a different record and response path. Check the precise claim against `PROBLEM.md`, declared dependencies, parent attempts, code or formal artifacts, and the stated verification method. Separate a reproducibility failure, a proof gap, a false claim, and a novelty problem.

Review an open contribution on its PR. For a merged attempt, use a flaw-report issue for a concise diagnosis or a refutation attempt for a durable mathematical result. Never equate passing CI or being merged with mathematical correctness.

## Validate and Hand Off

Run the checks appropriate to the mathematical work. For an attempt, run the repository validator and its own verification entrypoint. For review or reproduction, rerun the relevant artifacts and state which parts of the argument remain outside executable verification.

Before any authorized publication, inspect the final diff and staged paths. Report the contribution path, mathematical claim or review outcome, evidence run, unresolved gaps, affected files, and any external actions still requiring approval.
