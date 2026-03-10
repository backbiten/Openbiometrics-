# Seat of Life — Source Snapshot Guide

The "Seat of Life" tooling creates a deterministic, self-contained archive of
the Openbiometrics source tree so the project can be **fully restored** even if
the repository is removed from the internet.

---

## What is a Seat of Life snapshot?

A snapshot is a portable record of the project at a point in time:

| File | Description |
|------|-------------|
| `openbiometrics-<tag>.tar.gz` | Deterministic gzip-compressed archive of every tracked source file |
| `manifest.json` | JSON listing every file path + its SHA-256 hash |
| `openbiometrics-<tag>.tar.gz.enc` | (Optional) Fernet-encrypted copy of the archive |

Because the archive uses fixed timestamps and normalised ownership metadata,
the same source tree always produces the **same archive bytes** — making it
easy to detect tampering.

---

## Generating a snapshot locally

```bash
# Basic snapshot (no encryption)
python tools/seat_of_life/snapshot.py --output-dir dist --tag v1.0.0

# With optional encryption (requires: pip install cryptography)
python tools/seat_of_life/snapshot.py --output-dir dist --tag v1.0.0 --encrypt
```

You will find the archive and manifest in `dist/`.

---

## Snapshot as a GitHub Release artifact

Every time a GitHub Release is published the **Release workflow**
(`.github/workflows/release.yml`) automatically:

1. Builds the snapshot archive and manifest.
2. Uploads them as **workflow artifacts** (visible under the Actions tab).
3. Attaches them directly to the GitHub Release as downloadable assets.

You can also trigger the workflow manually from the **Actions** tab using
**workflow_dispatch** without creating a release.

---

## Verifying a snapshot

```bash
# Verify every file in the manifest
python - <<'EOF'
import hashlib, json, sys
from pathlib import Path

manifest = json.loads(Path("manifest.json").read_text())
errors = []
for entry in manifest["files"]:
    p = Path(entry["path"])
    if not p.exists():
        errors.append(f"MISSING  {entry['path']}")
        continue
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    if digest != entry["sha256"]:
        errors.append(f"MISMATCH {entry['path']}")
if errors:
    print("VERIFICATION FAILED:")
    for e in errors:
        print(" ", e)
    sys.exit(1)
print(f"All {len(manifest['files'])} files verified OK.")
EOF
```

---

## Restoring from a snapshot

If the repository is unavailable, restore the project from a snapshot archive:

```bash
# Unpack the archive
tar -xzf openbiometrics-<tag>.tar.gz

# Verify integrity against the manifest
cp manifest.json openbiometrics-<tag>/
cd openbiometrics-<tag>
python - <<'EOF'
import hashlib, json, sys
from pathlib import Path
manifest = json.loads(Path("manifest.json").read_text())
errors = []
for entry in manifest["files"]:
    p = Path(entry["path"])
    if not p.exists():
        errors.append(f"MISSING  {entry['path']}")
        continue
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    if digest != entry["sha256"]:
        errors.append(f"MISMATCH {entry['path']}")
if errors:
    print("VERIFICATION FAILED:")
    for e in errors:
        print(" ", e)
    sys.exit(1)
print(f"All {len(manifest['files'])} files verified OK.")
EOF
```

---

## Decrypting an encrypted snapshot

If you used `--encrypt` to produce a `.enc` file:

```bash
python - <<'EOF'
import base64, getpass, sys
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

enc_path = Path("openbiometrics-<tag>.tar.gz.enc")
data = enc_path.read_bytes()
salt, token = data[:16], data[16:]
passphrase = getpass.getpass("Passphrase: ").encode()
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
key = base64.urlsafe_b64encode(kdf.derive(passphrase))
plaintext = Fernet(key).decrypt(token)
out = enc_path.with_suffix("")   # removes the .enc suffix
out.write_bytes(plaintext)
print(f"Decrypted → {out}")
EOF
```

**Note:** Encryption is optional and uses only standard library primitives
(`cryptography` package — Fernet symmetric encryption, which is AES-128-CBC
with PKCS7 padding + HMAC-SHA256 for authentication).  The KDF (PBKDF2-HMAC-
SHA256) produces a 32-byte key; Fernet uses the first 16 bytes for AES-128
and the remaining 16 bytes for HMAC.  No novel or proprietary cryptographic
algorithms are introduced.

---

## What is excluded from the snapshot

The following are **not** included in the archive to keep it clean and
reproducible:

- `.git/` — version-control metadata
- `__pycache__/`, `*.pyc`, `*.pyo` — compiled Python bytecode
- `.pytest_cache/` — test runner cache
- `dist/` — previously generated snapshots (prevents self-referential archives)

To change the exclusion list, edit `EXCLUDE_PATTERNS` in
`tools/seat_of_life/snapshot.py`.
