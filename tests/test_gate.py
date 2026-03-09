"""
Tests for the adult-only gate (--attest-21 / --consent-file).

Run with:  python -m pytest tests/
"""

import json
import os
import sys
import tempfile
import pytest

# Ensure the package root is on the path when running from tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import openbiometrics as ob


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_json(tmp_path, data):
    """Write *data* as JSON to a temp file and return the path."""
    path = os.path.join(tmp_path, "consent.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    return path


VALID_CONSENT = {
    "consent": True,
    "adult_attestation": True,
    "signed_at": "2026-03-09T12:34:56Z",
    "participant_id": "anon-001",
}


# ---------------------------------------------------------------------------
# --attest-21 flag tests
# ---------------------------------------------------------------------------

class TestAttest21Flag:
    def test_missing_attest_21_flag(self, tmp_path):
        """Omitting --attest-21 entirely must exit non-zero."""
        path = _write_json(tmp_path, VALID_CONSENT)
        with pytest.raises(SystemExit) as exc:
            ob.main(["--consent-file", str(path)])
        assert exc.value.code != 0

    def test_attest_21_no_exits(self, tmp_path):
        """--attest-21 no must exit non-zero."""
        path = _write_json(tmp_path, VALID_CONSENT)
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "no", "--consent-file", str(path)])
        assert exc.value.code != 0

    def test_attest_21_false_exits(self, tmp_path):
        """--attest-21 false must exit non-zero."""
        path = _write_json(tmp_path, VALID_CONSENT)
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "false", "--consent-file", str(path)])
        assert exc.value.code != 0

    def test_attest_21_yes_passes(self, tmp_path):
        """--attest-21 yes with a valid consent file must succeed."""
        path = _write_json(tmp_path, VALID_CONSENT)
        result = ob.main(["--attest-21", "yes", "--consent-file", str(path)])
        assert result == 0

    def test_attest_21_yes_case_insensitive(self, tmp_path):
        """--attest-21 YES (upper-case) must also pass."""
        path = _write_json(tmp_path, VALID_CONSENT)
        result = ob.main(["--attest-21", "YES", "--consent-file", str(path)])
        assert result == 0

    def test_attest_21_true_passes(self, tmp_path):
        """--attest-21 true must succeed."""
        path = _write_json(tmp_path, VALID_CONSENT)
        result = ob.main(["--attest-21", "true", "--consent-file", str(path)])
        assert result == 0


# ---------------------------------------------------------------------------
# --consent-file flag tests
# ---------------------------------------------------------------------------

class TestConsentFileFlag:
    def test_missing_consent_file_flag(self):
        """Omitting --consent-file entirely must exit non-zero."""
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "yes"])
        assert exc.value.code != 0

    def test_consent_file_not_found(self, tmp_path):
        """A path that does not exist must exit non-zero."""
        missing = os.path.join(str(tmp_path), "nonexistent.json")
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "yes", "--consent-file", missing])
        assert exc.value.code != 0

    def test_invalid_json_exits(self, tmp_path):
        """A file with invalid JSON must exit non-zero."""
        bad = os.path.join(str(tmp_path), "bad.json")
        with open(bad, "w") as fh:
            fh.write("{not valid json")
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "yes", "--consent-file", bad])
        assert exc.value.code != 0

    def test_json_not_object_exits(self, tmp_path):
        """A JSON array (not object) must exit non-zero."""
        path = os.path.join(str(tmp_path), "consent.json")
        with open(path, "w") as fh:
            json.dump([1, 2, 3], fh)
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "yes", "--consent-file", path])
        assert exc.value.code != 0


# ---------------------------------------------------------------------------
# Consent field validation tests
# ---------------------------------------------------------------------------

class TestConsentFieldValidation:
    def _run(self, tmp_path, overrides):
        data = {**VALID_CONSENT, **overrides}
        path = _write_json(tmp_path, data)
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "yes", "--consent-file", str(path)])
        assert exc.value.code != 0

    def test_consent_false_exits(self, tmp_path):
        self._run(tmp_path, {"consent": False})

    def test_consent_missing_exits(self, tmp_path):
        data = {k: v for k, v in VALID_CONSENT.items() if k != "consent"}
        path = _write_json(tmp_path, data)
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "yes", "--consent-file", str(path)])
        assert exc.value.code != 0

    def test_adult_attestation_false_exits(self, tmp_path):
        self._run(tmp_path, {"adult_attestation": False})

    def test_adult_attestation_missing_exits(self, tmp_path):
        data = {k: v for k, v in VALID_CONSENT.items() if k != "adult_attestation"}
        path = _write_json(tmp_path, data)
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "yes", "--consent-file", str(path)])
        assert exc.value.code != 0

    def test_signed_at_missing_exits(self, tmp_path):
        data = {k: v for k, v in VALID_CONSENT.items() if k != "signed_at"}
        path = _write_json(tmp_path, data)
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "yes", "--consent-file", str(path)])
        assert exc.value.code != 0

    def test_signed_at_empty_exits(self, tmp_path):
        self._run(tmp_path, {"signed_at": ""})

    def test_signed_at_invalid_datetime_exits(self, tmp_path):
        self._run(tmp_path, {"signed_at": "not-a-date"})

    def test_participant_id_missing_exits(self, tmp_path):
        data = {k: v for k, v in VALID_CONSENT.items() if k != "participant_id"}
        path = _write_json(tmp_path, data)
        with pytest.raises(SystemExit) as exc:
            ob.main(["--attest-21", "yes", "--consent-file", str(path)])
        assert exc.value.code != 0

    def test_participant_id_empty_exits(self, tmp_path):
        self._run(tmp_path, {"participant_id": ""})

    def test_participant_id_whitespace_exits(self, tmp_path):
        self._run(tmp_path, {"participant_id": "   "})


# ---------------------------------------------------------------------------
# Happy-path: valid file + --attest-21 yes => proceeds (no camera init)
# ---------------------------------------------------------------------------

class TestHappyPath:
    def test_valid_consent_and_attest_succeeds(self, tmp_path, capsys):
        path = _write_json(tmp_path, VALID_CONSENT)
        result = ob.main(["--attest-21", "yes", "--consent-file", str(path)])
        assert result == 0
        out = capsys.readouterr().out
        assert "anon-001" in out

    def test_extra_fields_allowed(self, tmp_path):
        """Additional fields in the consent file must not cause failures."""
        data = {**VALID_CONSENT, "custom_field": "anything"}
        path = _write_json(tmp_path, data)
        result = ob.main(["--attest-21", "yes", "--consent-file", str(path)])
        assert result == 0

    def test_signed_at_without_z_suffix(self, tmp_path):
        """ISO-8601 without trailing Z (plain offset) must also be accepted."""
        data = {**VALID_CONSENT, "signed_at": "2026-03-09T12:34:56+00:00"}
        path = _write_json(tmp_path, data)
        result = ob.main(["--attest-21", "yes", "--consent-file", str(path)])
        assert result == 0


# ---------------------------------------------------------------------------
# run_adult_gate unit tests (internal API)
# ---------------------------------------------------------------------------

class TestRunAdultGate:
    def test_gate_refuses_bad_attest(self, tmp_path):
        path = _write_json(tmp_path, VALID_CONSENT)
        with pytest.raises(SystemExit) as exc:
            ob.run_adult_gate("no", str(path))
        assert exc.value.code != 0

    def test_gate_passes_valid(self, tmp_path):
        path = _write_json(tmp_path, VALID_CONSENT)
        # Should not raise
        ob.run_adult_gate("yes", str(path))
