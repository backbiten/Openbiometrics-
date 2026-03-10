# QA/QC Guide

This document describes how to run the Openbiometrics QA/QC gate locally and
how the CI workflow uses it as a required status check.

---

## Overview

The QA gate is a single Python script that runs three checks in sequence:

| Step | What it checks |
|------|---------------|
| 1 — Lint | `flake8` style and error checks on all Python files |
| 2 — Tests | `pytest` unit-test suite in `tests/` |
| 3 — Integrity | All required repository files are present and non-empty |

**All three steps must pass** for the gate to succeed (exit code 0).

---

## Running locally

```bash
# Install dependencies (once)
pip install pytest flake8

# Run the QA gate
python tools/qa/qa.py
```

To treat flake8 warnings as failures (stricter mode):

```bash
python tools/qa/qa.py --strict
```

### Expected output on success

```
============================================================
  Step 1/3 — Lint (flake8)
============================================================
  [OK]  Lint passed.

============================================================
  Step 2/3 — Tests (pytest)
============================================================
  ... (pytest output) ...
  [OK]  All tests passed.

============================================================
  Step 3/3 — Repository integrity check
============================================================
  [OK]  README.md  (sha256:...)
  ...
  [OK]  Integrity check passed.

============================================================
  QA/QC Summary
============================================================
  PASS  lint
  PASS  tests
  PASS  integrity

QA gate: PASSED
```

---

## CI integration

The CI workflow (`.github/workflows/ci.yml`) runs automatically on every push
and pull request. It executes `python tools/qa/qa.py` and reports the result
as the **QA/QC Gate** status check.

To require this check before merging a pull request:

1. Go to **Settings → Branches** in the GitHub repository.
2. Add (or edit) a branch protection rule for `main`.
3. Enable **Require status checks to pass before merging**.
4. Search for and select **"QA/QC Gate"**.
5. Save the rule.

---

## What the integrity check covers

The integrity check verifies that these files exist and are non-empty:

- `README.md`
- `LICENSE`
- `openbiometrics.py`
- `consent.example.json`
- `tests/__init__.py`
- `tests/test_gate.py`

If you add new required files, update `REQUIRED_FILES` in `tools/qa/qa.py`.

---

## Role-based QA workflow

The QA gate supports a construction-industry-inspired role hierarchy:

| Role | Responsibility |
|------|---------------|
| **Project Manager / General Superintendent** | Approves releases; merges to `main` (GitHub branch protection) |
| **Superintendent / General Foreman** | Reviews PRs; required in `CODEOWNERS` for critical paths |
| **Foreman / Lead Hand** | Runs `python tools/qa/qa.py --strict`; reviews QA reports |
| **Journeyman / Apprentice / Laborer** | Runs `python tools/qa/qa.py` locally; reports issues; contributes patches |

GitHub enforces the upper levels through branch protection rules and
`CODEOWNERS`.  The QA script is the shared tool everyone uses, regardless of role.
