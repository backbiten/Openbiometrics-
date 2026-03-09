# Data Policy

This document defines the rules for collecting, handling, storing, and deleting data within the Openbiometrics project.

## 1. Consent-first data collection

- **Only collect biometric data from participants who have given explicit, informed consent.** See [ethics.md](ethics.md) for consent requirements.
- Do not collect biometric data in public spaces or any context where individuals have not been individually informed and have not opted in.
- Record consent (e.g., signed consent form, timestamped digital acknowledgement) and retain that record for the duration of the study plus any legally required period.
- If consent is withdrawn, delete or anonymize the participant's data promptly.

## 2. No real biometric data in the repository

- Do **not** commit real participant biometric data (images, audio, sensor readings, derived embeddings, etc.) to this repository or any connected repository.
- Use synthetic datasets, publicly licensed benchmark data, or fully anonymized samples for development, testing, and example code.
- If example data files are needed, document their provenance and confirm they contain no real identifiable individuals.

## 3. De-identification and pseudonymization

- **De-identification:** Remove or replace all direct identifiers (name, date of birth, device ID, study ID linked to personal records) before sharing or publishing data.
- **Pseudonymization:** Where full de-identification is not practicable during active research, replace identifiers with opaque tokens. The mapping table (key) must be:
  - Stored separately from the pseudonymized dataset
  - Access-controlled and encrypted at rest
  - Deleted as soon as re-identification is no longer needed
- **Key separation:** Never store the pseudonymization key in the same location, system, or repository as the pseudonymized biometric data.

## 4. Data security

- Biometric data must be encrypted at rest and in transit.
- Access must be restricted to personnel who need it for the stated research purpose (principle of least privilege).
- Log access to sensitive data and review logs periodically.
- Report any unauthorized access or data breach to the relevant data protection authority and affected participants as required by applicable law.

## 5. Data minimization and purpose limitation

- Collect only the data necessary for the specific research objective.
- Do not repurpose data collected under one study for a different purpose without obtaining new consent and, where required, a new ethics approval.

## 6. Retention and deletion

- Establish a retention schedule before data collection begins.
- Identifiable data should be deleted or anonymized as soon as the retention period expires.
- Maintain a deletion log to demonstrate compliance.

---

*This document does not constitute legal advice. Contributors and researchers are responsible for ensuring compliance with applicable data protection laws and institutional policies.*
