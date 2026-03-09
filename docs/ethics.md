# Ethics & Responsible Use Policy

## Purpose

OpenBiometrics (`obx`) is a research-grade data-collection tool intended
**exclusively** for opt-in usability studies and academic research where
every participant has given explicit, informed consent before any recording
begins.

---

## Core Principles

### 1. Explicit, Informed Consent — Always

- Participants must affirmatively agree to be recorded **before** the session
  begins.
- `obx` enforces this technically: the `--consent yes` flag must be passed on
  every invocation or the tool exits immediately with an error.
- Verbal or implied consent is not sufficient; ensure written consent is
  obtained following your IRB / ethics committee requirements.

### 2. No Hidden or Covert Recording

- Do not run `obx` in the background without the participant's knowledge.
- When a video session is active, the preview window displays a prominent
  **"RECORDING (CONSENTED)"** overlay and the console prints the output path.
- Do not attempt to suppress or redirect this notice.

### 3. Prohibited Use Cases

The following uses are **explicitly prohibited**:

| Prohibited | Reason |
|------------|--------|
| Monitoring public spaces | Surveillance without consent |
| RTSP / IP camera ingestion | Security camera feeds are not supported and will not be added |
| Recording minors without parental / guardian consent | Legal and ethical obligation |
| Covert employee monitoring | Violates labour law in most jurisdictions |
| Law-enforcement or immigration use | Out of scope; not validated for evidentiary purposes |
| Biometric identification of individuals | Not the purpose; data must remain de-identified |

### 4. De-Identified Outputs

- `metadata.json` must **not** contain names, email addresses, employee IDs,
  device serial numbers, or any other personally identifiable information.
- Session IDs are randomly generated and carry no personal information.
- Video and audio files should be stored on encrypted, access-controlled
  storage and processed under your institution's data-management plan.

### 5. Data Minimisation & Retention

- Record only the modalities strictly necessary for your study.
- Delete raw captures as soon as they are no longer needed.
- Follow your institution's data-retention policy (typically ≤ 5 years for
  research data).

### 6. Participant Rights

- Participants have the right to withdraw consent at any time (including
  after recording) and have their data deleted.
- Provide a clear point of contact for data-deletion requests.

---

## Contributor Responsibility

All contributors to this project must:

1. Ensure new features do not undermine the consent gate or the de-identified
   output requirement.
2. Not add RTSP, HLS, or other network-stream ingestion that could enable
   surveillance.
3. Include ethics review steps in any pull request that adds a new capture
   modality.

---

## Reporting Misuse

If you become aware of `obx` being used for surveillance or non-consensual
recording, please open a GitHub issue or contact the maintainers directly.

---

## Legal Disclaimer

This tool is provided for research purposes only. Users are solely responsible
for complying with applicable laws regarding recording consent, data protection
(e.g., GDPR, CCPA, HIPAA), and ethical research standards in their
jurisdiction.
