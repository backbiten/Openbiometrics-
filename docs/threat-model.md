# Threat Model (Draft)

> **Status:** Draft — to be refined as implementation progresses.

## Scope

This document covers threats relevant to the Openbiometrics pipeline:
Collector → Processing → Matching → API/CLI.

Out of scope for this draft: deployment infrastructure, key management
infrastructure, and physical security of sensor hardware.

## Assumptions

- The pipeline runs in a partially trusted environment (field device or
  on-premise server), not a fully hardened data centre.
- Network connectivity between components may be intermittent or untrusted.
- Operators are trusted; end-users submitting biometric samples are not.
- Open-source code means the implementation is known to adversaries.

## Assets

| Asset | Sensitivity |
|-------|-------------|
| Raw biometric captures | Critical |
| Extracted feature vectors | High |
| Matching scores and decisions | Medium |
| Model weights / algorithms | Medium |
| Audit logs | Medium |
| Configuration and credentials | High |

## Threat Scenarios

### T1 — Data Exfiltration
**Threat:** An attacker gains read access to stored biometric data or feature
vectors.  
**Impact:** Privacy violation; identity theft risk.  
**Mitigations:**
- Encrypt biometric stores at rest (AES-256 or equivalent).
- Enforce access control on storage APIs.
- Prefer storing feature vectors over raw captures.

### T2 — Adversarial Input (Spoofing / Presentation Attack)
**Threat:** An attacker submits a synthetic or replayed biometric sample to
impersonate a legitimate subject.  
**Impact:** Unauthorised access; false match.  
**Mitigations:**
- Liveness detection in the Collector component.
- Replay-resistant capture bundles (timestamp + nonce signed by device).

### T3 — Model Poisoning
**Threat:** A malicious contributor substitutes a model binary with one that
introduces backdoors.  
**Impact:** Systematic false matches or denials.  
**Mitigations:**
- No binary model files in the repository; use manifests with checksums.
- Verify checksums at runtime before loading any model.
- Code review requirement for changes to model loading paths.

### T4 — API Abuse
**Threat:** An unauthenticated or over-privileged client makes excessive
matching requests, enumerating identities or causing denial of service.  
**Impact:** Privacy leakage; service degradation.  
**Mitigations:**
- Authentication required on all API endpoints.
- Rate limiting and request size limits enforced by default.
- Structured audit log of all matching requests.

### T5 — Supply Chain Attack
**Threat:** A dependency is compromised and introduces malicious code.  
**Impact:** Arbitrary code execution; data exfiltration.  
**Mitigations:**
- Pin dependency versions; use lock files.
- Enable automated dependency vulnerability scanning (e.g. Dependabot).
- Minimal dependency footprint.

### T6 — Insider Threat / Accidental Data Commit
**Threat:** A contributor accidentally commits real biometric data.  
**Impact:** Privacy violation; potential legal liability.  
**Mitigations:**
- CI check to detect likely biometric file types before merge.
- Clear data policy (see [data-policy.md](data-policy.md)).
- Private security advisory process for fast removal.

## Residual Risks

- Liveness detection effectiveness depends on the quality of the implementation
  and is an active research area.
- Regulatory compliance is the responsibility of the deployer, not this project.

## Review Cadence

This threat model should be revisited whenever a new component is added or an
existing interface changes significantly.
