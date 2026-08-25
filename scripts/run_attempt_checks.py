#!/usr/bin/env python3
"""Run verification entrypoints for changed attempts, or all attempts when no base is given."""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
ATTEMPT_PATH_RE = re.compile(r"^(problems/[^/]+/attempts/[^/]+)(?:/|$)")
RUNNER_PATHS = (Path("code/run.sh"), Path("lean/run.sh"))


def changed_attempt_roots(base: str) -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    roots = set()
    for path in result.stdout.splitlines():
        match = ATTEMPT_PATH_RE.match(path)
        if match:
            roots.add(Path(match.group(1)))
    return sorted(roots)


def runners(base: Optional[str]) -> list[Path]:
    if base:
        roots = changed_attempt_roots(base)
        candidates = [root / runner for root in roots for runner in RUNNER_PATHS]
    else:
        candidates = []
        for pattern in ("problems/*/attempts/*/code/run.sh", "problems/*/attempts/*/lean/run.sh"):
            candidates.extend(path.relative_to(ROOT) for path in ROOT.glob(pattern))
    return sorted(path for path in set(candidates) if (ROOT / path).is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="git SHA used to select changed attempts")
    parser.add_argument("--timeout", type=int, default=600, help="seconds allowed per runner")
    args = parser.parse_args()

    selected = runners(args.base)
    if not selected:
        scope = "changed" if args.base else "repository"
        print(f"OK — no attempt runners in {scope} scope")
        return 0

    for runner in selected:
        print(f"RUN — {runner}", flush=True)
        try:
            completed = subprocess.run(
                ["bash", runner.name],
                cwd=ROOT / runner.parent,
                timeout=args.timeout,
            )
        except subprocess.TimeoutExpired:
            print(f"FAILED — {runner} exceeded {args.timeout}s", file=sys.stderr)
            return 1
        if completed.returncode:
            print(f"FAILED — {runner} exited {completed.returncode}", file=sys.stderr)
            return completed.returncode

    print(f"OK — {len(selected)} attempt runner(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
