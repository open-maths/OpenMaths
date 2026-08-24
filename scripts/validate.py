#!/usr/bin/env python3
"""OpenMaths repository validator.

Checks structural validity of the research record: schemas, id/directory
consistency, parent DAG integrity, required writeup sections, and (in CI,
with --base) PR scope. It deliberately judges form, never mathematics.

Usage:
    python scripts/validate.py [--base <git-sha>]

Exit code 0 = valid, 1 = violations found (all are printed).
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"
SCHEMA_DIR = ROOT / "schema"
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ATTEMPT_ID_RE = re.compile(r"^20\d{2}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*$")

WRITEUP_REQUIRED_HEADINGS = ["## Claim", "## Novelty", "## Verification"]
PROBLEM_REQUIRED_HEADINGS = ["## Statement", "## Do not claim", "## Verification requirements"]
CODE_REQUIRED_TYPES = {"counterexample", "computational-evidence"}


class StrDateLoader(yaml.SafeLoader):
    """SafeLoader that keeps YAML timestamps as plain strings (schemas expect strings)."""


StrDateLoader.add_constructor(
    "tag:yaml.org,2002:timestamp",
    lambda loader, node: loader.construct_scalar(node),
)

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load_yaml(path: Path):
    try:
        with path.open() as fh:
            return yaml.load(fh, Loader=StrDateLoader)
    except yaml.YAMLError as exc:
        err(f"{path.relative_to(ROOT)}: YAML parse error: {exc}")
        return None


def load_schema(name: str) -> Draft202012Validator:
    import json

    with (SCHEMA_DIR / name).open() as fh:
        return Draft202012Validator(json.load(fh))


def schema_check(validator: Draft202012Validator, data, path: Path) -> None:
    for violation in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in violation.path) or "<root>"
        err(f"{path.relative_to(ROOT)}: [{where}] {violation.message}")


def check_headings(path: Path, required: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for heading in required:
        if not re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE):
            err(f"{path.relative_to(ROOT)}: missing required section heading '{heading}'")


def validate_problem(problem_dir: Path, problem_schema, attempt_schema) -> None:
    slug = problem_dir.name
    if not SLUG_RE.match(slug):
        err(f"problems/{slug}: directory name is not a valid slug")

    problem_md = problem_dir / "PROBLEM.md"
    problem_yaml = problem_dir / "problem.yaml"
    if not problem_md.is_file():
        err(f"problems/{slug}: missing PROBLEM.md")
    else:
        check_headings(problem_md, PROBLEM_REQUIRED_HEADINGS)
    if not problem_yaml.is_file():
        err(f"problems/{slug}: missing problem.yaml")
        return

    meta = load_yaml(problem_yaml)
    if meta is None:
        return
    schema_check(problem_schema, meta, problem_yaml)
    if isinstance(meta, dict) and meta.get("id") != slug:
        err(f"problems/{slug}/problem.yaml: id '{meta.get('id')}' != directory name '{slug}'")

    attempts_dir = problem_dir / "attempts"
    attempts: dict[str, dict] = {}
    if attempts_dir.is_dir():
        for attempt_dir in sorted(p for p in attempts_dir.iterdir() if p.is_dir()):
            attempt = validate_attempt(attempt_dir, slug, attempt_schema)
            if attempt is not None:
                attempts[attempt["id"]] = attempt

    check_dag(slug, attempts)


def validate_attempt(attempt_dir: Path, problem_slug: str, attempt_schema):
    rel = attempt_dir.relative_to(ROOT)
    aid = attempt_dir.name
    if not ATTEMPT_ID_RE.match(aid):
        err(f"{rel}: directory name is not a valid attempt id (YYYY-MM-DD-slug-suffix)")

    attempt_yaml = attempt_dir / "attempt.yaml"
    writeup = attempt_dir / "WRITEUP.md"
    if not attempt_yaml.is_file():
        err(f"{rel}: missing attempt.yaml")
        return None
    if not writeup.is_file():
        err(f"{rel}: missing WRITEUP.md")
    else:
        check_headings(writeup, WRITEUP_REQUIRED_HEADINGS)

    meta = load_yaml(attempt_yaml)
    if meta is None or not isinstance(meta, dict):
        return None
    schema_check(attempt_schema, meta, attempt_yaml)

    if meta.get("id") != aid:
        err(f"{rel}/attempt.yaml: id '{meta.get('id')}' != directory name '{aid}'")
    if meta.get("problem") != problem_slug:
        err(f"{rel}/attempt.yaml: problem '{meta.get('problem')}' != containing problem '{problem_slug}'")

    if meta.get("type") in CODE_REQUIRED_TYPES:
        code_dir = attempt_dir / "code"
        if not code_dir.is_dir() or not any(code_dir.iterdir()):
            err(f"{rel}: type '{meta.get('type')}' requires a non-empty code/ directory")

    lean_dir = attempt_dir / "lean"
    if meta.get("type") == "formalization" and not (lean_dir.is_dir() and any(lean_dir.iterdir())):
        err(f"{rel}: type 'formalization' requires a non-empty lean/ directory")

    return meta


def check_dag(problem_slug: str, attempts: dict[str, dict]) -> None:
    for aid, meta in attempts.items():
        for parent in meta.get("parents") or []:
            if parent == aid:
                err(f"problems/{problem_slug}/attempts/{aid}: lists itself as a parent")
            elif parent not in attempts:
                err(f"problems/{problem_slug}/attempts/{aid}: parent '{parent}' does not exist in this problem")
        refutes = meta.get("refutes")
        if refutes and refutes not in attempts:
            err(f"problems/{problem_slug}/attempts/{aid}: refutes '{refutes}' which does not exist in this problem")

    # Cycle detection over the parent relation.
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {aid: WHITE for aid in attempts}

    def visit(aid: str, stack: list[str]) -> None:
        color[aid] = GRAY
        for parent in attempts[aid].get("parents") or []:
            if parent not in attempts:
                continue
            if color[parent] == GRAY:
                err(f"problems/{problem_slug}: parent cycle involving {' -> '.join(stack + [aid, parent])}")
            elif color[parent] == WHITE:
                visit(parent, stack + [aid])
        color[aid] = BLACK

    for aid in attempts:
        if color[aid] == WHITE:
            visit(aid, [])


def check_global_uniqueness() -> None:
    seen: dict[str, str] = {}
    for attempt_yaml in PROBLEMS_DIR.glob("*/attempts/*/attempt.yaml"):
        if attempt_yaml.parts[-4] == "_template":
            continue
        aid = attempt_yaml.parent.name
        if aid in seen:
            err(f"attempt id '{aid}' used in both '{seen[aid]}' and '{attempt_yaml.parent.relative_to(ROOT)}'")
        else:
            seen[aid] = str(attempt_yaml.parent.relative_to(ROOT))


def check_scope(base: str) -> None:
    """PR scope: existing attempts are append-only except their attempt.yaml (steward metadata edits)."""
    try:
        diff = subprocess.run(
            ["git", "diff", "--name-status", f"{base}...HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except subprocess.CalledProcessError as exc:
        err(f"scope check failed to run git diff against base '{base}': {exc.stderr.strip()}")
        return

    attempt_file_re = re.compile(r"^problems/[^/]+/attempts/[^/]+/(.+)$")
    for line in diff.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0], parts[-1]
        m = attempt_file_re.match(path)
        if not m:
            continue
        inner = m.group(1)
        if status.startswith(("M", "D")) and inner != "attempt.yaml":
            err(
                f"{path}: modifies/deletes content of an existing attempt (status {status}). "
                "Attempts are append-only; corrections go in a new attempt. "
                "Only attempt.yaml may be edited, by stewards, for status changes."
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="git sha of the PR base; enables the scope check")
    args = parser.parse_args()

    if not PROBLEMS_DIR.is_dir():
        print("FATAL: problems/ directory not found", file=sys.stderr)
        return 1

    problem_schema = load_schema("problem.schema.json")
    attempt_schema = load_schema("attempt.schema.json")

    n_problems = 0
    for problem_dir in sorted(p for p in PROBLEMS_DIR.iterdir() if p.is_dir()):
        if problem_dir.name.startswith("_"):
            continue
        n_problems += 1
        validate_problem(problem_dir, problem_schema, attempt_schema)

    check_global_uniqueness()

    if args.base:
        check_scope(args.base)

    if errors:
        print(f"INVALID — {len(errors)} violation(s):\n", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1

    n_attempts = sum(
        1
        for p in PROBLEMS_DIR.glob("*/attempts/*/attempt.yaml")
        if p.parts[-4] != "_template"
    )
    print(f"OK — {n_problems} problem(s), {n_attempts} attempt(s), 0 violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
