# Openbiometrics-

For open source development of field biometrics.

---

## ⚠️ Adult-only / Opt-in Research Use Only

**This tool is strictly limited to consenting adults (18+) in opt-in research settings.**

| Requirement | Detail |
|-------------|--------|
| **Adult participants only** | The operator **must** confirm that every participant is 18 years of age or older before any session begins. Use on or near minors (anyone under 18, including teenagers and juveniles) is **strictly prohibited**. |
| **Explicit informed consent** | Every participant must give free, voluntary, and informed consent prior to data capture. No covert or passive recording is permitted. |
| **Operator responsibility** | The tool does **not** estimate, infer, or guess a participant's age from camera footage or any biometric signal. Age verification is the sole responsibility of the human operator. |
| **No background recording** | Sessions are operator-initiated only. No continuous or background data capture is supported. |

---

## Adult Attestation Gate

The CLI enforces an adult-only gate **before any camera or biometric data is accessed**.

### Required flag

```
--adult yes
```

Acceptable values: `yes` or `true` (case-insensitive).

If the flag is absent or not affirmative the program **exits immediately with a non-zero status** and prints a clear error — no camera is initialised and no data is captured.

### Usage

```bash
# Correct – operator attests participant is a consenting adult
python openbiometrics.py --adult yes

# Correct – 'true' is also accepted
python openbiometrics.py --adult true

# Rejected – exits non-zero, no data captured
python openbiometrics.py
python openbiometrics.py --adult no
```

---

## Running the tests

```bash
pip install pytest
pytest tests/
```

---

## License

See [LICENSE](LICENSE).
