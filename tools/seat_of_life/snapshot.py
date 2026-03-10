#!/usr/bin/env python3
"""
tools/seat_of_life/snapshot.py — "Seat of Life" source snapshot tool.

Creates a deterministic, reproducible archive of the repository and a
manifest.json listing every included file with its SHA-256 hash.

The snapshot can be used to restore the project if the source repository
is ever removed from the internet.

Usage:
    python tools/seat_of_life/snapshot.py [OPTIONS]

Options:
    --output-dir DIR   Directory to write snapshot + manifest (default: ./dist)
    --tag LABEL        Version/tag label embedded in the archive name
                       (default: "snapshot")
    --encrypt          Encrypt the archive with a passphrase (requires the
                       'cryptography' package; optional).  If cryptography is
                       not installed the flag is ignored with a warning.

Output files:
    <output-dir>/openbiometrics-<tag>.tar.gz        Deterministic source archive
    <output-dir>/manifest.json                      File list + SHA-256 hashes
    <output-dir>/openbiometrics-<tag>.tar.gz.enc    Encrypted archive (optional)

Encryption note:
    When --encrypt is used the script uses Fernet symmetric encryption from the
    'cryptography' package (AES-128-CBC + HMAC-SHA256).  No novel or custom
    cryptographic primitives are introduced.  The encryption key is derived from
    a user-supplied passphrase via PBKDF2-HMAC-SHA256 (600,000 iterations).
    The unencrypted archive is also kept unless you delete it manually.

Restoration:
    See docs/SeatOfLife.md for step-by-step restoration instructions.
"""

import argparse
import hashlib
import json
import sys
import tarfile
import time
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Files / directories to exclude from the snapshot.
EXCLUDE_PATTERNS = {
    "__pycache__",
    ".pytest_cache",
    ".git",
    "dist",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _should_exclude(path: Path) -> bool:
    """Return True if *path* (relative to repo root) should be excluded."""
    for part in path.parts:
        if part in EXCLUDE_PATTERNS or part.endswith(".pyc") or part.endswith(".pyo"):
            return True
    return False


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _collect_files(root: Path):
    """Yield (relative_path_str, absolute_path) for every tracked file."""
    for abs_path in sorted(root.rglob("*")):
        if not abs_path.is_file():
            continue
        rel = abs_path.relative_to(root)
        if _should_exclude(rel):
            continue
        yield str(rel), abs_path


# ---------------------------------------------------------------------------
# Archive builder
# ---------------------------------------------------------------------------

def build_archive(output_dir: Path, tag: str) -> tuple:
    """
    Build a deterministic .tar.gz archive and a manifest.json.

    Returns (archive_path, manifest_path).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_name = f"openbiometrics-{tag}.tar.gz"
    archive_path = output_dir / archive_name
    manifest_entries = []

    # Use a fixed mtime so the archive is deterministic across runs.
    fixed_mtime = 0  # 1970-01-01T00:00:00Z

    with tarfile.open(archive_path, "w:gz") as tar:
        for rel_str, abs_path in _collect_files(REPO_ROOT):
            digest = _sha256(abs_path)
            manifest_entries.append({"path": rel_str, "sha256": digest})

            info = tar.gettarinfo(str(abs_path), arcname=rel_str)
            info.mtime = fixed_mtime
            # Normalise ownership so archives are identical regardless of who
            # runs the tool.
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            with open(abs_path, "rb") as fh:
                tar.addfile(info, fh)

    # Write manifest
    manifest_path = output_dir / "manifest.json"
    manifest = {
        "tool": "seat_of_life",
        "tag": tag,
        "archive": archive_name,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": manifest_entries,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return archive_path, manifest_path


# ---------------------------------------------------------------------------
# Optional encryption
# ---------------------------------------------------------------------------

def _try_encrypt(archive_path: Path, passphrase: str) -> Optional[Path]:
    """
    Encrypt *archive_path* using Fernet (from the 'cryptography' package).

    Returns the encrypted file path, or None if the package is unavailable.
    """
    try:
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
        from cryptography.fernet import Fernet
        import base64
        import os as _os
    except ImportError:
        print(
            "WARNING: 'cryptography' package not found — skipping encryption.\n"
            "         Install it with:  pip install cryptography",
            file=sys.stderr,
        )
        return None

    # Derive a 32-byte key from the passphrase using PBKDF2.
    salt = _os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    f = Fernet(key)

    plaintext = archive_path.read_bytes()
    token = f.encrypt(plaintext)

    enc_path = archive_path.with_suffix(archive_path.suffix + ".enc")
    # Prepend the 16-byte salt so decryption can re-derive the key.
    enc_path.write_bytes(salt + token)

    return enc_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="snapshot",
        description="Seat of Life — create a deterministic source snapshot.",
    )
    parser.add_argument(
        "--output-dir",
        default="dist",
        help="Directory to write the archive and manifest (default: dist).",
    )
    parser.add_argument(
        "--tag",
        default="snapshot",
        help="Label embedded in the archive filename (default: snapshot).",
    )
    parser.add_argument(
        "--encrypt",
        action="store_true",
        default=False,
        help=(
            "Encrypt the archive with a passphrase. "
            "Requires the 'cryptography' package."
        ),
    )
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    print(f"Building snapshot (tag={args.tag}) → {output_dir}/")

    archive_path, manifest_path = build_archive(output_dir, args.tag)
    print(f"  Archive  : {archive_path}")
    print(f"  Manifest : {manifest_path}")

    if args.encrypt:
        passphrase = _prompt_passphrase()
        enc_path = _try_encrypt(archive_path, passphrase)
        if enc_path:
            print(f"  Encrypted: {enc_path}")
        else:
            print("  Encryption skipped (see warning above).")

    print("\nDone. See docs/SeatOfLife.md for restoration instructions.")
    return 0


def _prompt_passphrase() -> str:
    import getpass
    while True:
        pw1 = getpass.getpass("Passphrase for encryption: ")
        pw2 = getpass.getpass("Confirm passphrase       : ")
        if pw1 == pw2:
            return pw1
        print("Passphrases do not match — try again.", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
