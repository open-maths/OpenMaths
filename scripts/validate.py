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
import json
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

WRITEUP_REQUIRED_HEADINGS = [
    "## Claim",
    "## Novelty",
    "## Dependencies",
    "## Approach",
    "## Verification",
    "## Open questions",
]
PROBLEM_REQUIRED_HEADINGS = ["## Statement", "## Do not claim", "## Verification requirements"]
CODE_REQUIRED_TYPES = {"counterexample", "computational-evidence"}
ATTEMPT_PATH_RE = re.compile(r"^(problems/[^/]+/attempts/[^/]+)/(.*)$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLUGIN_NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?$")


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
    with (SCHEMA_DIR / name).open() as fh:
        return Draft202012Validator(json.load(fh))


def load_json(path: Path):
    try:
        with path.open() as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        err(f"{path.relative_to(ROOT)}: JSON parse error: {exc}")
        return None


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
        elif not (code_dir / "run.sh").is_file():
            err(f"{rel}: type '{meta.get('type')}' requires code/run.sh")

    lean_dir = attempt_dir / "lean"
    if meta.get("type") == "formalization" and not (lean_dir.is_dir() and any(lean_dir.iterdir())):
        err(f"{rel}: type 'formalization' requires a non-empty lean/ directory")
    elif meta.get("type") == "formalization" and not (lean_dir / "run.sh").is_file():
        err(f"{rel}: type 'formalization' requires lean/run.sh")

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


def skill_paths() -> list[Path]:
    paths = set(ROOT.glob("skills/*/SKILL.md"))
    paths.update(ROOT.glob("plugins/*/skills/*/SKILL.md"))
    return sorted(paths)


def validate_skills() -> None:
    for skill_md in skill_paths():
        rel = skill_md.relative_to(ROOT)
        text = skill_md.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---(?:\n|$)", text, flags=re.DOTALL)
        if not match:
            err(f"{rel}: missing or invalid YAML frontmatter")
            continue
        try:
            meta = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            err(f"{rel}: YAML frontmatter parse error: {exc}")
            continue
        if not isinstance(meta, dict):
            err(f"{rel}: frontmatter must be an object")
            continue
        name = meta.get("name")
        description = meta.get("description")
        if name != skill_md.parent.name:
            err(f"{rel}: name '{name}' != directory name '{skill_md.parent.name}'")
        if not isinstance(name, str) or not SKILL_NAME_RE.fullmatch(name):
            err(f"{rel}: name must use lowercase letters, digits, and single hyphens")
        if not isinstance(description, str) or not description.strip():
            err(f"{rel}: description must be a non-empty string")
        if "[TODO:" in text:
            err(f"{rel}: unfinished TODO placeholder")


def validate_plugin_distribution() -> None:
    portable_plugins: dict[Path, dict] = {}
    expected_schema = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    for manifest in sorted(ROOT.glob("plugins/*/plugin.json")):
        data = load_json(manifest)
        if not isinstance(data, dict):
            continue
        portable_plugins[manifest.parent] = data
        rel = manifest.relative_to(ROOT)
        if data.get("$schema") != expected_schema:
            err(f"{rel}: $schema must be '{expected_schema}'")
        name = data.get("name")
        if (
            not isinstance(name, str)
            or not PLUGIN_NAME_RE.fullmatch(name)
            or "--" in name
            or ".." in name
        ):
            err(f"{rel}: invalid plugin name '{name}'")
        if not isinstance(data.get("description"), str) or not data["description"].strip():
            err(f"{rel}: description must be a non-empty string")

        claude_manifest = manifest.parent / ".claude-plugin" / "plugin.json"
        if claude_manifest.is_file():
            claude = load_json(claude_manifest)
            if isinstance(claude, dict):
                for field in ("name", "version"):
                    if claude.get(field) != data.get(field):
                        err(
                            f"{claude_manifest.relative_to(ROOT)}: {field} must match "
                            f"{rel}"
                        )

    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    if not marketplace_path.is_file():
        return
    marketplace = load_json(marketplace_path)
    if not isinstance(marketplace, dict):
        return
    if not isinstance(marketplace.get("name"), str) or not marketplace["name"].strip():
        err(f"{marketplace_path.relative_to(ROOT)}: name must be a non-empty string")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or not entries:
        err(f"{marketplace_path.relative_to(ROOT)}: plugins must be a non-empty array")
        return
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not isinstance(entry.get("source"), str):
            err(f"{marketplace_path.relative_to(ROOT)}: plugins/{index} needs a string source")
            continue
        source = entry["source"]
        if not source.startswith("./"):
            continue
        plugin_dir = (ROOT / source[2:]).resolve()
        try:
            plugin_dir.relative_to(ROOT)
        except ValueError:
            err(f"{marketplace_path.relative_to(ROOT)}: plugins/{index} escapes the repository")
            continue
        portable = portable_plugins.get(plugin_dir)
        if portable is None:
            err(f"{marketplace_path.relative_to(ROOT)}: plugins/{index} source has no plugin.json")
        elif entry.get("name") != portable.get("name"):
            err(f"{marketplace_path.relative_to(ROOT)}: plugins/{index} name must match plugin.json")


def check_scope(base: str) -> None:
    """Classify and enforce attempt, steward, and project PR scope."""
    try:
        diff = subprocess.run(
            ["git", "diff", "--name-status", "--find-renames", f"{base}...HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except subprocess.CalledProcessError as exc:
        err(f"scope check failed to run git diff against base '{base}': {exc.stderr.strip()}")
        return

    changes: list[tuple[str, list[str]]] = []
    for line in diff.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        changes.append((parts[0], parts[1:]))

    attempt_changes: list[tuple[str, str, str, str]] = []
    for status, paths in changes:
        for path in paths:
            match = ATTEMPT_PATH_RE.match(path)
            if match:
                attempt_changes.append((status, path, match.group(1), match.group(2)))
    if not attempt_changes:
        return

    def existed_at_base(root: str) -> bool:
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{base}:{root}/attempt.yaml"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    roots = {root for _, _, root, _ in attempt_changes}
    new_roots = {root for root in roots if not existed_at_base(root)}

    if new_roots:
        if len(new_roots) != 1:
            err(f"PR adds {len(new_roots)} attempt directories; an attempt PR may add one")
            return
        new_root = next(iter(new_roots))
        for status, paths in changes:
            for path in paths:
                if not path.startswith(new_root + "/"):
                    err(f"{path}: attempt PRs may change only '{new_root}/'")
            if not status.startswith("A"):
                err(f"{', '.join(paths)}: new attempt files must be added, not status {status}")
        meta = load_yaml(ROOT / new_root / "attempt.yaml")
        if isinstance(meta, dict) and (meta.get("claim") or {}).get("status") != "exploration":
            err(f"{new_root}/attempt.yaml: new attempts must use claim.status 'exploration'")
        return

    changed_paths = [path for _, paths in changes for path in paths]
    if len(changed_paths) != len(attempt_changes):
        for path in changed_paths:
            if not ATTEMPT_PATH_RE.match(path):
                err(f"{path}: status-update PRs may change only existing attempt.yaml files")
    for status, path, _, inner in attempt_changes:
        if status != "M" or inner != "attempt.yaml":
            err(
                f"{path}: existing attempts are append-only; steward updates may only modify "
                "attempt.yaml"
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
    validate_skills()
    validate_plugin_distribution()

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
