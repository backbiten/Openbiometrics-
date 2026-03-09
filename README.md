# Openbiometrics-

For open source development of field biometrics.

---

## Adult-only gate (21+)

Openbiometrics is restricted to participants who are **21 years of age or older**.  
Access is controlled entirely through **explicit operator attestation** and a
**signed consent file** — the tool does **not** infer age, gender, height, body
shape, or any other demographic characteristic from images or biometric signals.

Both flags are **required**; the program exits before initialising any camera or
loading any image if either is missing or invalid.

---

## Required CLI flags

### `--attest-21 yes`

The operator must explicitly attest that the participant is 21 or older.  
Accepted values: `yes` or `true` (case-insensitive).

```bash
python openbiometrics.py --attest-21 yes --consent-file consent.json
```

### `--consent-file <path>`

Path to a JSON file containing the participant's signed consent.

---

## Consent file format

The file must be valid JSON containing **at minimum** the following fields:

| Field               | Type    | Description                                          |
|---------------------|---------|------------------------------------------------------|
| `consent`           | boolean | Must be `true`                                       |
| `adult_attestation` | boolean | Must be `true` — attests participant is 21+          |
| `signed_at`         | string  | ISO-8601 datetime of signing, e.g. `2026-03-09T12:34:56Z` |
| `participant_id`    | string  | Non-empty identifier (pseudonymous values are fine)  |

Additional fields are allowed and ignored.

### Example — `consent.json`

```json
{
  "consent": true,
  "adult_attestation": true,
  "signed_at": "2026-03-09T12:34:56Z",
  "participant_id": "anon-001"
}
```

An example file is included in the repository as [`consent.example.json`](consent.example.json).

---

## Failure behaviour

If any requirement is not met the program:

1. Prints a clear refusal message to stderr explaining what is missing.
2. Exits with a **non-zero** exit code (2).
3. Does **not** open a camera, read frames, or write any image data.

Example refusal output:

```
REFUSED: This tool requires explicit consent + 21+ attestation. No data was captured.
Reason: Consent file field 'adult_attestation' must be true.
```

---

## No biometric age inference

This tool does **not** attempt to estimate a participant's age from their face,
height, body shape, or any other biometric or physical characteristic.  
The adult-only guarantee is enforced solely through the explicit attestation
flags described above.

---

## Running the tests

```bash
python -m pytest tests/
```

All tests use Python's standard library only — no external test dependencies
beyond `pytest`.
