#!/usr/bin/env python3
"""
Openbiometrics – field biometrics CLI.

Adult-only gate (21+):
  All sessions require explicit operator attestation and a signed consent file.
  The program exits before initialising any camera or loading any image if
  either requirement is missing or invalid.

  This tool does NOT infer age (or any other demographic) from images, face
  landmarks, height, body shape, or any other biometric signal.
"""

import argparse
import json
import sys
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Consent-file validation
# ---------------------------------------------------------------------------

REQUIRED_CONSENT_FIELDS = ("consent", "adult_attestation", "signed_at", "participant_id")


def _load_consent_file(path: str) -> dict:
    """Load and parse the consent JSON file.  Raises SystemExit on any error."""
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        _refuse(f"Consent file not found: {path}")
    except json.JSONDecodeError as exc:
        _refuse(f"Consent file is not valid JSON ({path}): {exc}")
    if not isinstance(data, dict):
        _refuse(f"Consent file must contain a JSON object, got {type(data).__name__}")
    return data


def _validate_consent(data: dict) -> None:
    """Validate all required fields.  Raises SystemExit on any violation."""
    for field in REQUIRED_CONSENT_FIELDS:
        if field not in data:
            _refuse(f"Consent file is missing required field: '{field}'")

    if data["consent"] is not True:
        _refuse("Consent file field 'consent' must be true.")

    if data["adult_attestation"] is not True:
        _refuse("Consent file field 'adult_attestation' must be true.")

    signed_at = data["signed_at"]
    if not isinstance(signed_at, str) or not signed_at.strip():
        _refuse("Consent file field 'signed_at' must be a non-empty ISO-8601 string.")
    # Basic ISO-8601 sanity check
    try:
        datetime.fromisoformat(signed_at.replace("Z", "+00:00"))
    except ValueError:
        _refuse(
            f"Consent file field 'signed_at' is not a valid ISO-8601 datetime: {signed_at!r}"
        )

    participant_id = data["participant_id"]
    if not isinstance(participant_id, str) or not participant_id.strip():
        _refuse("Consent file field 'participant_id' must be a non-empty string.")


# ---------------------------------------------------------------------------
# Attest-21 flag validation
# ---------------------------------------------------------------------------

_AFFIRMATIVE = {"yes", "true"}


def _check_attest_21(value: str) -> None:
    """Raise SystemExit if --attest-21 is not an affirmative value."""
    if value.lower().strip() not in _AFFIRMATIVE:
        _refuse(
            "--attest-21 must be 'yes' or 'true'. "
            "Pass --attest-21 yes to attest that the participant is 21 or older."
        )


# ---------------------------------------------------------------------------
# Fast-fail helper
# ---------------------------------------------------------------------------

def _refuse(reason: str) -> None:
    print(
        "REFUSED: This tool requires explicit consent + 21+ attestation. "
        "No data was captured.\n"
        f"Reason: {reason}",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# Gate function (called before any camera / image I/O)
# ---------------------------------------------------------------------------

def run_adult_gate(attest_21: str, consent_file: str) -> None:
    """Validate attestation and consent file.  Must be called before any I/O."""
    _check_attest_21(attest_21)
    data = _load_consent_file(consent_file)
    _validate_consent(data)
    # All checks passed
    print(
        f"Consent verified for participant '{data['participant_id']}' "
        f"(signed_at={data['signed_at']}). Proceeding."
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openbiometrics",
        description=(
            "Openbiometrics field biometrics tool.\n\n"
            "Adult-only (21+): explicit operator attestation and a signed consent\n"
            "file are required before any camera or image processing begins.\n"
            "This tool does NOT infer age from biometrics."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--attest-21",
        required=True,
        metavar="yes|true",
        help=(
            "Operator attestation that the participant is 21 or older. "
            "Must be 'yes' or 'true' (case-insensitive). Required."
        ),
    )
    parser.add_argument(
        "--consent-file",
        required=True,
        metavar="PATH",
        help=(
            "Path to a JSON consent file signed by the participant. "
            "Required fields: consent (true), adult_attestation (true), "
            "signed_at (ISO-8601), participant_id (string). Required."
        ),
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    run_adult_gate(args.attest_21, args.consent_file)
    # TODO: initialise camera / run biometric pipeline here
    return 0


if __name__ == "__main__":
    sys.exit(main())
