#!/usr/bin/env python3
"""
Openbiometrics – open-source field biometrics toolkit.

IMPORTANT – Adult-only / opt-in research tool
==============================================
This software is intended exclusively for opt-in research involving
consenting adults (18 +).  Use on or near minors is strictly prohibited.

The tool does NOT estimate, infer, or guess any participant's age from
camera data.  The operator is solely responsible for confirming that every
participant has provided informed, voluntary consent and is an adult.
"""

import argparse
import sys


# ---------------------------------------------------------------------------
# Adult attestation helpers
# ---------------------------------------------------------------------------

MINIMUM_AGE = 18

_AFFIRMATIVE = {"yes", "true"}


def _adult_flag_is_affirmative(value: str) -> bool:
    """Return True when *value* is an affirmative acknowledgement."""
    return value.strip().lower() in _AFFIRMATIVE


def require_adult_attestation(adult_flag: str) -> None:
    """Exit the process if operator has not attested that the participant is an adult.

    This check **must** run before any camera or biometric data is accessed.
    """
    if not _adult_flag_is_affirmative(adult_flag):
        print(
            "\n"
            "ERROR: Adult attestation required.\n"
            "\n"
            "  This tool is intended for opt-in research with consenting adults only.\n"
            f"  You must confirm that the participant is an adult ({MINIMUM_AGE}+) and has\n"
            "  given explicit, informed consent before capturing any data.\n"
            "\n"
            "  Re-run with:  --adult yes\n"
            "\n"
            "  The tool does NOT estimate age from camera data.\n"
            "  The operator is solely responsible for participant eligibility.\n",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        "[openbiometrics] Adult attestation accepted. "
        "Opt-in research session starting."
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openbiometrics",
        description=(
            "Openbiometrics – open-source field biometrics toolkit.\n\n"
            "Adult-only / opt-in research use only.\n"
            f"The operator must attest that the participant is an adult ({MINIMUM_AGE}+)\n"
            "and has provided explicit informed consent before any data is captured."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--adult",
        required=True,
        metavar="yes|true",
        help=(
            f"Operator attestation that the participant is an adult ({MINIMUM_AGE}+) and "
            "has given explicit informed consent. "
            "Acceptable values: 'yes' or 'true' (case-insensitive). "
            "If this flag is absent or not affirmative the program exits "
            "immediately without accessing any camera or biometric data."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # ------------------------------------------------------------------ #
    # Adult attestation gate – must happen BEFORE any camera / data work  #
    # ------------------------------------------------------------------ #
    require_adult_attestation(args.adult)

    # ------------------------------------------------------------------ #
    # Main application logic goes here.                                   #
    # Camera initialisation, biometric capture, etc. must only be placed  #
    # below this line, after the attestation gate has passed.             #
    # ------------------------------------------------------------------ #

    # Placeholder – replace with real pipeline code.
    print("[openbiometrics] Ready. (No camera initialised in this placeholder.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
