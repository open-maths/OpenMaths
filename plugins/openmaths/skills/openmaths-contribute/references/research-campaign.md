# Autonomous Research Campaigns

Use this reference when an agent should work on one OpenMaths problem for many turns with little supervision. The goal is durable, verifiable mathematical progress—not merely a long transcript or an impressive-sounding claim.

## Define the Campaign Contract

Before sustained work, record:

- the problem slug and the precise region of the frontier in scope;
- a time, turn, token, or cost budget when the user provides one;
- acceptable outcomes: a proved lemma or reduction, exact counterexample, bounded reproducible computation, refutation, rigorous obstruction or dead end, faithful synthesis, or a clearly improved research map;
- the evidence required for each kind of outcome;
- constraints on tools, files, network access, and external actions;
- stopping conditions for success, exhausted budget, repeated non-progress, or a blocker that needs human input.

Do not use “solve the open problem” or “find something groundbreaking” as the only completion condition. Pair ambition with falsifiable intermediate outcomes and a budget. A result is significant because it advances the recorded frontier and survives verification, not because the agent labels it significant.

## Keep a Durable Research Notebook

Copy [../assets/campaign-notebook.md](../assets/campaign-notebook.md) to `.openmaths-work/<problem-slug>/CAMPAIGN.md`. The `.openmaths-work/` directory is gitignored and may hold scripts, logs, candidate proofs, and exact computational output that are not ready for the research record.

Update the notebook after every meaningful cycle and before context compaction, delegation, pause, or handoff. Keep it concise enough for another agent to resume without replaying the transcript. Distinguish:

- established repository facts, with file or URL provenance;
- conjectures and candidate lemmas;
- verified deductions and their checks;
- failed approaches and the exact obstruction;
- the current best result and the next experiment.

Never put secrets in the notebook. Do not treat ignored scratch files as evidence that another contributor can reproduce; move necessary material into an attempt only when packaging a contribution.

## Run the Research Loop

1. **Map the frontier.** Read the full problem contract, status index, relevant attempt chains, artifacts, literature, and current community context. Build a short list of genuinely open, testable subproblems.
2. **Choose one target.** Prefer the smallest statement whose resolution would eliminate uncertainty or unlock a parent direction. State what would prove it and what would falsify it.
3. **Construct.** Try one coherent proof, computation, counterexample search, reduction, or formalization. Keep derivations explicit and scripts deterministic.
4. **Attack.** Switch roles and try to break the candidate: test boundary cases, negate quantifiers, inspect hidden assumptions, compare with known results, and search for simpler counterexamples. When the harness supports independent agents, give a critic only the claim and dependencies, then reconcile its objections in the primary notebook.
5. **Verify.** Re-derive delicate steps, run exact or interval-safe computations, preserve commands and outputs, and separate machine-checked facts from prose arguments. Check novelty against the frontier again.
6. **Checkpoint and replan.** Record what changed, what failed, and which direction now has the highest expected research value. Continue unless a stopping condition is met.

Avoid spending many cycles paraphrasing the same idea. After repeated failure with no new information, change the subproblem, strengthen the falsification method, seek a synthesis, or document the obstruction.

## Evaluate Progress Without Overclaiming

At each checkpoint ask:

| Gate | Question |
|---|---|
| Correctness | Does every part of the candidate claim follow, and are all gaps explicit? |
| Novelty | Is it new relative to the problem statement, parent attempts, siblings, discussions, and cited literature? |
| Relevance | Does it settle a useful subproblem, remove a live direction, or improve verification? |
| Reproducibility | Can another contributor check the argument or rerun the computation from recorded inputs? |
| Scope | Can the durable outcome be stated as one precise attempt claim? |

A promising route that fails these gates remains in the notebook. A rigorous negative result can pass them and be more valuable than a broad speculative positive claim.

## Use Harness Controls Deliberately

- In current Codex and Claude Code versions, `/goal` is the primary control for continuous work toward a completion condition. Put the outcome, constraints, verification, budget, checkpoint path, and stop rules in the goal. See the [Codex](https://learn.chatgpt.com/docs/long-running-work) and [Claude Code](https://code.claude.com/docs/en/goal) goal guides for current controls.
- Claude Code's `/loop` reruns a prompt on a schedule. Use it to revisit a long computation, poll external work, or periodically resume a checkpointed campaign. It is not a substitute for the reasoning loop above; see the [scheduled-task guide](https://code.claude.com/docs/en/scheduled-tasks).
- In harnesses without these commands, give the same campaign contract as the initial prompt and require the agent to continue from the notebook until a stop condition holds.
- Use an isolated worktree for concurrent campaigns or whenever the current checkout has unrelated edits. Never allow two agents to write the same notebook or attempt directory concurrently.
- Long-running mode does not expand permissions. A goal may read, reason, write ignored scratch files, and run safe local checks within the user's scope; commits and remote GitHub actions still require authorization.

## Package or Hand Off the Outcome

At the end, report:

1. the strongest exact statement supported;
2. its relationship to the existing frontier and why it may be novel;
3. proof, computation, and adversarial checks completed;
4. gaps, assumptions, and plausible failure modes;
5. dead ends and reusable obstructions discovered;
6. ranked next steps;
7. whether the result is ready for an attempt, needs another independent review, or should remain scratch work.

If it is ready, reread `AGENTS.md` and create the attempt from the verified outcome. Do not copy the whole campaign notebook into the attempt: write a self-contained claim, proof, novelty account, dependencies, verification procedure, and open questions.
