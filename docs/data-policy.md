# Data Policy (Draft)

> **Status:** Draft — subject to review before any production data handling
> is implemented.

## Core Rule

**No real biometric data may be committed to this repository, ever.**

This includes — but is not limited to — fingerprint images, iris scans, face
photos, voice recordings, gait samples, or any other biometric modality
collected from real individuals.

## What May Be Committed

| Type | Allowed | Notes |
|------|---------|-------|
| Synthetic / algorithmically generated samples | ✅ | Must be clearly labelled as synthetic |
| Anonymised / fully de-identified samples | ⚠️  | Requires maintainer review; justify in PR |
| Real biometric data | ❌ | Never |
| Schema definitions (no data) | ✅ | JSON Schema, Protobuf, etc. |
| Model weight checksums / manifests | ✅ | No binary model files in repo |

## Handling Rules for Derived Projects

If you build a system on top of Openbiometrics that processes real biometric
data, the following baseline rules apply:

1. **Purpose limitation.** Collect only the biometric data needed for the
   stated purpose; do not repurpose without fresh consent.
2. **Data minimisation.** Store feature vectors where possible rather than raw
   captures. Delete raw captures once features are extracted, unless raw
   retention is explicitly required.
3. **Access control.** Restrict access to biometric stores to the minimum set
   of services and personnel that need it.
4. **Retention limits.** Define and enforce a retention period; delete data
   when it is no longer needed.
5. **Audit logging.** Log all access to and matching operations on biometric
   stores. Logs must be tamper-evident.
6. **Incident response.** Have a documented plan for responding to a data
   breach involving biometric data.

## Regulatory Awareness

Biometric data is classified as *sensitive personal data* under GDPR (Article 9),
CCPA, BIPA, and many other jurisdictions. Deployers are responsible for their
own legal compliance. This project does not constitute legal advice.

## Reporting a Violation

If you believe real biometric data has been inadvertently committed to this
repository, open a **private** security advisory (GitHub → Security →
Advisories) so it can be removed from history promptly.
