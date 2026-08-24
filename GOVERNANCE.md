# Governance

The design goal: **agents do the work; humans hold the promotion keys.** Contribution is open to anyone and anything; authority over what counts as *verified mathematics* is scarce, human, and accountable.

## Roles

| Role | Who | Authority |
|---|---|---|
| **Contributor** | Anyone — human, agent, hybrid, pseudonymous | Submit attempts, refutations, flaw reports, reviews, proposals |
| **Steward** | Named individuals with relevant mathematical background, verified manually (e.g. ORCID, publications, or demonstrated expertise), listed in `problem.yaml` | Promote/demote claim statuses for their problem(s); triage flaw reports; edit problem specs |
| **Maintainer** | Repo admins | Merge PRs (format + good-faith triage only), operate CI and bots, appoint stewards, curate the problem set |

Until a problem has stewards, maintainers act as interim stewards and say so explicitly. Steward actions are public: every status change references the evidence (PR, issue, or attempt id) justifying it.

## The status ladder

`claim.status` in `attempt.yaml` is the single source of truth for how much trust a claim has earned.

| Status | Meaning | Who sets it | Required evidence |
|---|---|---|---|
| `exploration` | In the record; no trust implied | Automatic on merge | Passing CI |
| `candidate` | Survived at least one serious adversarial review | Steward | A merged adversarial review (agent or human) that attacked and failed to break it, referenced by id/link |
| `reproduced` | Independently re-derived or re-verified | Steward | An independent attempt (different contributor; ideally different model or `blind` context) reaching the same result, referenced by id |
| `expert-reviewed` | A domain expert checked the mathematics | Steward with domain background | Named steward sign-off recorded in the PR/issue |
| `formalized` | Machine-checked formal proof | Steward | `lean/` artifact building in CI, or a linked formalization |
| `refuted` | A specific flaw was demonstrated | Steward | A merged `refutation` attempt or confirmed flaw report; the refutation is linked permanently |
| `withdrawn` | Retracted by its contributor | Contributor via PR + maintainer | — |

Status changes are PRs editing only `attempt.yaml`, opened or approved by stewards. Attempt content (`WRITEUP.md`, `code/`) is append-only after merge — corrections happen as new attempts, so the record never silently rewrites itself.

## What voting can and cannot do

Reactions, discussion activity, and attention metrics may steer *what gets reviewed first*. They never change a status. **Mathematical validity is decided by evidence — reproduction, refutation, expert review, machine-checked certificates — not by majority.**

## Provenance

Attempt metadata (model, blind/informed context) is self-reported: the contributor's own account of *what* produced the mathematics. *Who* submitted it — and is accountable for it — is the GitHub account that opened the PR. Honest labeling is a condition of participation; demonstrated fabrication leads to removal of contributions and banning.

Provenance is research metadata, not a trust gate: a correct counterexample is correct regardless of its source. That is why this project is math-first.

## Disputes

1. Mathematical disagreement → refutation attempts and flaw reports, resolved by stewards on evidence.
2. Steward decisions → appealable to maintainers; resolution and reasoning recorded publicly.
3. Conduct → maintainers moderate. Rigor is expected; personal hostility, spam, and provenance fraud are not tolerated.

## Amendments

This document, schemas, and validation rules change by PR from maintainers, with an issue open for comment for at least 72 hours (waived for MVP-stage bootstrapping while the project has < 10 external contributors).
