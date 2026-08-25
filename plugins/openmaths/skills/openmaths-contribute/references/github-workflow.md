# OpenMaths Git and GitHub Reference

Use this reference only when Git or GitHub is part of the task. Remote writes require user authorization.

## Inspect

```bash
git status --short --branch
git remote -v
gh repo view open-maths/OpenMaths
```

Clone only when local files or validators are needed:

```bash
gh repo clone open-maths/OpenMaths
cd OpenMaths
```

Useful read-only commands:

```bash
gh issue list --repo open-maths/OpenMaths --state all
gh issue view <number> --repo open-maths/OpenMaths --comments
gh pr list --repo open-maths/OpenMaths --state all
gh pr view <number> --repo open-maths/OpenMaths --comments
gh pr diff <number> --repo open-maths/OpenMaths
gh pr checks <number> --repo open-maths/OpenMaths
```

GitHub CLI has no high-level Discussion command. Use `gh api graphql` or the web UI when Discussion context is needed.

## Collaboration Surfaces

| Surface | Role |
|---|---|
| Discussion | Informal ideas, questions, and coordination. |
| Issue | Focused subproblem, flaw report, problem proposal, or steward application. |
| Attempt PR | New mathematical record governed by `AGENTS.md`. |
| Steward PR | Evidence-backed claim-status change governed by `GOVERNANCE.md`. |

## Branch and Publish

Preferred attempt branch and PR title:

```text
attempt/<problem-slug>/<short-description>
[<problem-slug>] <type>: <claim-focused description>
```

Create a branch from the current upstream default without disturbing unrelated local work. Stage only the new attempt directory:

```bash
git add -- problems/<problem-slug>/attempts/<attempt-id>
git diff --cached
```

When publication is authorized, use `.github/PULL_REQUEST_TEMPLATE/attempt.md` and target the repository's current default branch. Do not include generated dashboards or unrelated changes. Do not merge or change claim status unless separately authorized.
