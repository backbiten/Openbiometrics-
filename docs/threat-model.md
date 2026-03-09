# Threat Model

This document describes the primary threat scenarios relevant to the Openbiometrics project, the associated risks, and the mitigations in place or recommended.

## 1. In-scope use

Openbiometrics is designed for **opt-in research and usability studies** with informed participants. All assets and threat analysis are scoped to that context.

## 2. Assets

| Asset | Description |
|---|---|
| Participant biometric data | Raw sensor data, images, audio, derived embeddings |
| Pseudonymization keys | Mapping tables linking tokens to participant identities |
| Study metadata | Protocols, consent records, research outputs |
| Source code and models | Algorithms, trained models, configuration |

## 3. Standard threat scenarios

### 3.1 Unauthorized access to participant data
- **Risk:** Attacker or insider exfiltrates biometric data, enabling re-identification.
- **Mitigations:** Encryption at rest and in transit; role-based access control; audit logging; key separation (see [data-policy.md](data-policy.md)).

### 3.2 Re-identification of pseudonymized data
- **Risk:** Combining pseudonymized biometric data with external datasets re-identifies participants.
- **Mitigations:** Strict key separation; delete keys when no longer needed; avoid releasing datasets that can be cross-referenced with public data.

### 3.3 Accidental data leak via version control
- **Risk:** Real participant data committed to a public repository.
- **Mitigations:** Policy prohibiting real biometric data in the repo (see [data-policy.md](data-policy.md)); pre-commit checks; code review requirements.

### 3.4 Supply-chain compromise
- **Risk:** Malicious dependency or model weight exfiltrates data or introduces a backdoor.
- **Mitigations:** Pin dependency versions; review third-party models before use; verify checksums where possible.

## 4. Misuse

This section addresses the risk of the project's code or outputs being repurposed for harmful applications outside its intended research scope.

### 4.1 Repurposing for surveillance and public-space profiling

- **Risk:** Algorithms or trained models are adapted to identify, track, or profile individuals in public spaces without their consent.
- **Impact:** Mass privacy violations; chilling effects on freedom of movement and association; potential targeting of activists, journalists, or minority groups.
- **Mitigations:**
  - **Policy:** The acceptable-use policy (README.md, ethics.md) explicitly prohibits covert surveillance and public-space profiling.
  - **Governance:** Contributors are expected to review and abide by the ethics guidelines before contributing code or models.
  - **Code-level:** Avoid building or exposing APIs that are purpose-built for real-time identification of non-consenting individuals. Flag such use cases in code review.

### 4.2 Weaponized psychological manipulation

- **Risk:** Biometric signals (e.g., emotion recognition, physiological indicators) are used to craft targeted disinformation, manipulate emotional responses, or conduct influence operations.
- **Impact:** Harm to individuals and communities; erosion of trust in information ecosystems.
- **Mitigations:**
  - **Policy:** Prohibited use case under ethics.md.
  - **Governance:** Ethics review required for studies that involve emotional or psychological signals in contexts beyond direct participant wellbeing.

### 4.3 Law-enforcement or military weaponization

- **Risk:** Research outputs are integrated into systems used for law-enforcement targeting or armed-conflict applications without appropriate oversight and legal authority.
- **Impact:** Potential violations of human rights law; harm to individuals incorrectly identified or targeted.
- **Mitigations:**
  - **Policy:** Explicitly prohibited without lawful authority and appropriate independent oversight (ethics.md).
  - **Governance:** Any proposed integration with law-enforcement or defense applications must be reviewed by the project maintainers and, where applicable, an ethics board.

### 4.4 Targeting vulnerable populations

- **Risk:** Project tools are used to collect or analyze biometric data from minors, people under duress, or individuals with diminished capacity without adequate safeguards.
- **Impact:** Exploitation of vulnerable individuals; violation of special-category data protections.
- **Mitigations:**
  - **Policy:** Requires additional safeguards and guardian consent (ethics.md).
  - **Governance:** Studies involving vulnerable populations require explicit ethics committee approval before data collection.

## 5. Out-of-scope threats

The following are explicitly out of scope and must not be enabled by this project:

- Real-time identification of non-consenting individuals in public spaces
- Covert biometric capture of any kind
- Integration into systems designed for mass surveillance

---

*This threat model is a living document. It should be reviewed and updated whenever significant new features, models, or deployment contexts are introduced.*
