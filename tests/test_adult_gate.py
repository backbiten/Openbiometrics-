"""Tests for the adult attestation gate in openbiometrics.py."""

import subprocess
import sys

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SCRIPT = "openbiometrics.py"


def run_cli(*args: str) -> subprocess.CompletedProcess:
    """Run the openbiometrics CLI with the given arguments and capture output."""
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Tests: missing / non-affirmative --adult flag → must exit non-zero
# ---------------------------------------------------------------------------

class TestAdultGateDenied:
    """Program must refuse to run without an affirmative --adult flag."""

    def test_missing_adult_flag_exits_nonzero(self):
        result = run_cli()
        assert result.returncode != 0, (
            "Expected non-zero exit when --adult flag is missing"
        )

    def test_missing_adult_flag_prints_no_camera_output(self):
        """No camera / session output should appear when the gate is closed."""
        result = run_cli()
        assert "session starting" not in result.stdout.lower()

    def test_adult_no_exits_nonzero(self):
        result = run_cli("--adult", "no")
        assert result.returncode != 0

    def test_adult_no_shows_error_message(self):
        result = run_cli("--adult", "no")
        combined = result.stderr + result.stdout
        assert "adult attestation required" in combined.lower()

    def test_adult_false_exits_nonzero(self):
        result = run_cli("--adult", "false")
        assert result.returncode != 0

    def test_adult_empty_string_exits_nonzero(self):
        result = run_cli("--adult", "")
        assert result.returncode != 0

    def test_adult_numeric_exits_nonzero(self):
        result = run_cli("--adult", "18")
        assert result.returncode != 0

    def test_error_message_mentions_optin_research(self):
        result = run_cli("--adult", "no")
        combined = result.stderr + result.stdout
        assert "opt-in research" in combined.lower()

    def test_error_message_mentions_no_age_estimation(self):
        result = run_cli("--adult", "no")
        combined = result.stderr + result.stdout
        assert "does not estimate age" in combined.lower()


# ---------------------------------------------------------------------------
# Tests: affirmative --adult flag → must exit zero
# ---------------------------------------------------------------------------

class TestAdultGateAccepted:
    """Program must proceed normally when --adult is affirmative."""

    def test_adult_yes_exits_zero(self):
        result = run_cli("--adult", "yes")
        assert result.returncode == 0, (
            f"Expected exit 0 with --adult yes, got {result.returncode}\n"
            f"stderr: {result.stderr}"
        )

    def test_adult_YES_case_insensitive(self):
        result = run_cli("--adult", "YES")
        assert result.returncode == 0

    def test_adult_Yes_mixed_case(self):
        result = run_cli("--adult", "Yes")
        assert result.returncode == 0

    def test_adult_true_exits_zero(self):
        result = run_cli("--adult", "true")
        assert result.returncode == 0

    def test_adult_TRUE_case_insensitive(self):
        result = run_cli("--adult", "TRUE")
        assert result.returncode == 0

    def test_adult_yes_prints_attestation_accepted(self):
        result = run_cli("--adult", "yes")
        combined = result.stdout + result.stderr
        assert "adult attestation accepted" in combined.lower()

    def test_adult_yes_prints_optin_session(self):
        result = run_cli("--adult", "yes")
        assert "opt-in research session starting" in result.stdout.lower()


# ---------------------------------------------------------------------------
# Tests: unit-level helpers
# ---------------------------------------------------------------------------

class TestAdultFlagHelper:
    """Unit tests for the _adult_flag_is_affirmative helper."""

    def setup_method(self):
        import importlib.util
        import pathlib
        spec = importlib.util.spec_from_file_location(
            "openbiometrics",
            pathlib.Path(__file__).parent.parent / "openbiometrics.py",
        )
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def test_yes_is_affirmative(self):
        assert self.mod._adult_flag_is_affirmative("yes") is True

    def test_true_is_affirmative(self):
        assert self.mod._adult_flag_is_affirmative("true") is True

    def test_case_insensitive_YES(self):
        assert self.mod._adult_flag_is_affirmative("YES") is True

    def test_no_is_not_affirmative(self):
        assert self.mod._adult_flag_is_affirmative("no") is False

    def test_empty_is_not_affirmative(self):
        assert self.mod._adult_flag_is_affirmative("") is False

    def test_numeric_is_not_affirmative(self):
        assert self.mod._adult_flag_is_affirmative("18") is False
