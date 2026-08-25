# GitHub Collaboration Workflow

Use this reference for mathematical collaboration: repository discovery, research community context, attempt or steward branches, review, and publication. Repository development and maintenance are outside this skill. Commands that create or modify remote state require user authorization.

## Inspect Before Acting

Prefer an existing checkout. A read-only task does not require a new branch or fork.

```bash
git status --short --branch
git remote -v
gh auth status
gh repo view open-maths/OpenMaths --json defaultBranchRef,hasDiscussionsEnabled,url
```

If no checkout exists and local files or validators are needed:

```bash
gh repo clone open-maths/OpenMaths
cd OpenMaths
```

Treat the repository's current default branch as canonical. Do not assume a separate development branch. Inspect remote protection when it matters instead of relying on stale knowledge:

```bash
gh api repos/open-maths/OpenMaths/branches
gh api repos/open-maths/OpenMaths/branches/main/protection
```

## Read Discussions

Discussions are for early ideas, open questions, research strategy, and community coordination. They may explain why someone is pursuing a direction, but they are not part of the mathematical record until the result becomes an attempt or another repository artifact.

List recent discussions:

```bash
gh api graphql -f query='query {
  repository(owner: "open-maths", name: "OpenMaths") {
    discussions(first: 50, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes { number title category { name } updatedAt url }
    }
  }
}' --jq '.data.repository.discussions.nodes'
```

Read a discussion and its comments before summarizing it:

```bash
gh api graphql -F number=<number> -f query='query($number: Int!) {
  repository(owner: "open-maths", name: "OpenMaths") {
    discussion(number: $number) {
      number title body url category { name }
      comments(first: 100) { nodes { author { login } body createdAt url } }
    }
  }
}' --jq '.data.repository.discussion'
```

GitHub CLI has no high-level `gh discussion` command. For a new post or reply, prefer the GitHub web UI or a narrowly scoped GraphQL mutation after the user authorizes the external message. Use a problem slug in the title when the discussion concerns a repository problem.

## Read and Use Issues

Issues turn a focused question or action into trackable work. Search before opening a duplicate:

```bash
gh issue list --repo open-maths/OpenMaths --state all --limit 100
gh issue view <number> --repo open-maths/OpenMaths --comments
gh search issues "<keywords>" --repo open-maths/OpenMaths --match title,body,comments
```

Choose the repository form that matches the outcome:

| Need | Form |
|---|---|
| Specific flaw in a merged attempt | `flaw-report.yml` issue or a durable refutation attempt |
| Focused question within an existing problem | `subproblem.yml` issue |
| New curated open problem | `problem-proposal.yml` issue |
| Volunteer for promotion/review authority | `steward-application.yml` issue |
| Open-ended idea or strategy | Discussion |

When authorized, start from the maintained form rather than recreating its fields:

```bash
gh issue create --repo open-maths/OpenMaths --template flaw-report.yml
gh issue create --repo open-maths/OpenMaths --template subproblem.yml
gh issue create --repo open-maths/OpenMaths --template problem-proposal.yml
gh issue create --repo open-maths/OpenMaths --template steward-application.yml
```

## Choose the Pull Request Lane

Classify the change before creating a branch. The lanes have different review questions and must not be mixed:

| Lane | Source of rules | Body guide |
|---|---|---|
| Attempt PR | `AGENTS.md` | `.github/PULL_REQUEST_TEMPLATE/attempt.md` |
| Steward status PR | `GOVERNANCE.md` | `.github/PULL_REQUEST_TEMPLATE/steward.md` |

Keep attempt and steward work separate. If repository-development work is discovered while researching, record it for a separate project task instead of adding it to the mathematical branch.

## Read and Review Pull Requests

Pull requests are proposed changes and the place to review unmerged work. Read the description, comments, checks, and actual diff:

```bash
gh pr list --repo open-maths/OpenMaths --state all --limit 100
gh pr view <number> --repo open-maths/OpenMaths --comments
gh pr diff <number> --repo open-maths/OpenMaths
gh pr checks <number> --repo open-maths/OpenMaths
```

Review the relevant kind of change:

- **Attempt PR:** check the claim, novelty, dependencies, gaps, provenance, verification, and the attempt scope defined in `AGENTS.md`.
- **Steward PR:** check that status changes touch attempt metadata and cite the evidence required by `GOVERNANCE.md`.

Use `gh pr checkout` only when local execution is needed and switching branches will not disturb the user's worktree. A read-only `gh pr diff` is often sufficient.

## Name Branches and Changes Clearly

Create short-lived branches from the current upstream default branch. These are preferred names, not mathematical structure:

| Work | Branch | Title |
|---|---|---|
| Attempt | `attempt/<problem-slug>/<short-description>` | `[<problem-slug>] <type>: <claim-focused description>` |
| Steward status update | `steward/<problem-slug>/<attempt-id>` | `steward(<problem-slug>): <status change>` |

The attempt title is required by `AGENTS.md`; the steward title is a clarity convention.

```bash
git fetch <base-remote> main
git switch -c <branch-name> <base-remote>/main
```

Do not switch branches over unrelated local changes.

## Stage and Inspect Deliberately

Stage explicit paths. Avoid broad staging commands that can capture unrelated work:

```bash
git add -- <intended-path> [<intended-path> ...]
git diff --cached --name-status
git diff --cached
```

Compare the staged paths with the rules for the selected PR type. Do not include generated `STATUS.md` files or `graph.json`; automation maintains them.

## Publish When Authorized

Use an existing writable remote when appropriate. If direct push access is unavailable, create the contributor's fork only after publication is authorized:

```bash
gh repo fork --remote
git remote -v
```

Push to the confirmed writable remote:

```bash
git commit -m "<title>"
git push -u <publish-remote> HEAD
```

Use the matching lane template as a body guide. Complete a copy in a temporary file outside the checkout, then create the PR without editing the tracked template:

```bash
gh pr create \
  --repo open-maths/OpenMaths \
  --base main \
  --title "<lane-appropriate title>" \
  --body-file <completed-temporary-pr-body>
```

Do not merge or promote a claim unless the user explicitly asks and the repository role and evidence rules authorize it.
