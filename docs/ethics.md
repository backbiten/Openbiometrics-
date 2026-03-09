# Ethics Guidelines

This document sets out the ethical requirements for all research and development work conducted under the Openbiometrics project.

## 1. Consent requirements

- **Informed consent is mandatory.** Participants must be fully informed about the nature of the study, the types of biometric data being collected, how that data will be used and stored, and who will have access to it — before any data collection begins.
- Consent must be freely given, specific, and unambiguous. Pre-ticked boxes or bundled consent are not acceptable.
- Participants must be able to **withdraw consent at any time** without penalty. Upon withdrawal, their data must be deleted or anonymized promptly unless a lawful basis for retention independently exists and has been disclosed to the participant.
- Where participants are minors or otherwise lack full legal capacity, appropriate guardian or parental consent must be obtained in accordance with applicable law.

## 2. Data minimization

- Collect only the biometric data that is strictly necessary for the stated research purpose.
- Avoid collecting additional personal attributes (e.g., location, device identifiers, demographic details) unless they are directly required and covered by the consent given.
- Aggregate or anonymize data at the earliest practicable stage of the research pipeline.
- Do not retain identifiable data beyond the period required for the research objective.

## 3. Prohibited use cases

The following uses are explicitly prohibited:

| Category | Examples |
|---|---|
| Covert surveillance | Capturing biometrics without participant knowledge; monitoring people in public spaces without consent |
| Mass profiling | Building individual or group profiles from biometric data collected without explicit consent |
| Psychological manipulation / warfare | Using biometric signals to manipulate emotional states, craft targeted disinformation, or conduct influence operations |
| Targeting vulnerable groups | Studies that exploit minors, people under duress, or individuals with diminished capacity without appropriate ethical safeguards |
| Law enforcement / military weaponization | Repurposing research outputs for identification, tracking, or targeting of individuals in law-enforcement or armed-conflict contexts without lawful authority and appropriate oversight |
| Commercial re-identification | Selling or licensing datasets that could re-identify participants without their consent |

This list is illustrative, not exhaustive. When in doubt, consult an ethics review body before proceeding.

## 4. Data retention guidance

- Define a retention period before the study begins and document it in the study protocol.
- Identifiable biometric data should be deleted or irreversibly anonymized as soon as the research objective no longer requires it.
- Pseudonymized data (where the key is held separately and securely) may be retained longer if justified by the research purpose, but the key must itself be deleted once re-identification is no longer needed.
- Do not commit real participant biometric data to version control. Use synthetic or fully anonymized datasets for development and testing.
- Maintain a data retention log so that deletion obligations can be verified.

## 5. IRB / ethics review recommendation

For any study involving human participants, a review by an **Institutional Review Board (IRB)**, Research Ethics Committee (REC), or equivalent body is strongly recommended and may be legally required depending on jurisdiction, funding source, or institutional policy.

Submit a protocol that covers:
- Research objectives and methods
- Types of data collected and their sensitivity
- Consent procedures
- Data security and retention plan
- Risk assessment and participant safeguards

Approval should be obtained before data collection begins. Keep a copy of the approval on file and follow any conditions attached to it.

---

*This document does not constitute legal advice. Researchers are responsible for understanding and complying with all applicable laws and institutional requirements in their jurisdiction.*
