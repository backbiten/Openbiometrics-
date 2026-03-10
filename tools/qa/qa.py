#!/usr/bin/env python3
"""
tools/qa/qa.py — Openbiometrics QA/QC gate.

Runs linting, the test suite, and a repository integrity check.
Exits 0 on success, non-zero on any failure.

Usage:
    python tools/qa/qa.py [--strict]

Options:
    --strict    Treat lint warnings as errors (default: errors only).

This script is also the entry point used by the CI workflow.
"""

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Files that must always exist for the repo to be considered integral.
REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "openbiometrics.py",
    "consent.example.json",
    "tests/__init__.py",
    "tests/test_gate.py",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _header(title: str) -> None:
    bar = "=" * 60
    print(f"\n{bar}\n  {title}\n{bar}")


def _ok(msg: str) -> None:
    print(f"  [OK]  {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Step 1 – Lint
# ---------------------------------------------------------------------------

def run_lint(strict: bool) -> bool:
    """Run flake8.  Returns True on success."""
    _header("Step 1/3 — Lint (flake8)")

    # Configuration comes from .flake8 in the repo root.
    select = "E,F,W" if strict else "E,F"
    cmd = [
        sys.executable, "-m", "flake8",
        "--select", select,
        str(REPO_ROOT),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout)
    if result.stderr.strip():
        print(result.stderr, file=sys.stderr)

    if result.returncode == 0:
        _ok("Lint passed.")
        return True

    _fail("Lint failed — fix the issues above before proceeding.")
    return False


# ---------------------------------------------------------------------------
# Step 2 – Tests
# ---------------------------------------------------------------------------

def run_tests() -> bool:
    """Run pytest.  Returns True on success."""
    _header("Step 2/3 — Tests (pytest)")

    cmd = [sys.executable, "-m", "pytest", str(REPO_ROOT / "tests"), "-v"]
    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode == 0:
        _ok("All tests passed.")
        return True

    _fail("Test suite failed — fix failing tests before proceeding.")
    return False


# ---------------------------------------------------------------------------
# Step 3 – Integrity check
# ---------------------------------------------------------------------------

def run_integrity_check() -> bool:
    """Verify required files exist and are non-empty.  Returns True on success."""
    _header("Step 3/3 — Repository integrity check")

    passed = True
    for rel in REQUIRED_FILES:
        full = REPO_ROOT / rel
        if not full.exists():
            _fail(f"Required file missing: {rel}")
            passed = False
        elif full.stat().st_size == 0 and not rel.endswith("__init__.py"):
            _fail(f"Required file is empty: {rel}")
            passed = False
        else:
            digest = hashlib.sha256(full.read_bytes()).hexdigest()[:12]
            _ok(f"{rel}  (sha256:{digest}…)")

    if passed:
        _ok("Integrity check passed.")
    else:
        _fail("Integrity check failed — one or more required files are missing or empty.")
    return passed


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="qa",
        description="Openbiometrics QA/QC gate — lint, tests, integrity check.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Treat flake8 warnings (W) as failures in addition to errors.",
    )
    args = parser.parse_args(argv)

    results = {
        "lint": run_lint(args.strict),
        "tests": run_tests(),
        "integrity": run_integrity_check(),
    }

    _header("QA/QC Summary")
    all_passed = True
    for step, ok in results.items():
        status = "PASS" if ok else "FAIL"
        print(f"  {status}  {step}")
        if not ok:
            all_passed = False

    if all_passed:
        print("\nQA gate: PASSED\n")
        return 0

    print("\nQA gate: FAILED — see errors above.\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
