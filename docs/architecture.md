# Architecture (Draft)

> **Status:** Draft — subject to change as implementation begins.

## Overview

Openbiometrics is structured as a pipeline of loosely coupled components.
Each component has a single responsibility and communicates through well-defined
interfaces so that individual pieces can be replaced or extended without
affecting the rest of the system.

```
┌───────────┐    raw     ┌────────────┐  features  ┌──────────┐
│ Collector │ ─────────► │ Processing │ ──────────► │ Matching │
└───────────┘            └────────────┘             └──────────┘
                                                          │
                                                     score/result
                                                          │
                                              ┌───────────┴────────┐
                                              │  API   │   CLI     │
                                              └────────┴───────────┘
```

## Components

### Collector (`src/collector/`)

Responsible for capturing raw biometric signals from sensors or files.

- Abstracts hardware differences behind a common interface.
- Must operate in low-connectivity, resource-constrained environments.
- Produces a *capture bundle*: raw data plus provenance metadata.

### Processing (`src/processing/`)

Transforms raw captures into feature representations suitable for matching.

- Pre-processing (noise reduction, normalisation, segmentation).
- Feature extraction (algorithm-dependent; pluggable backends).
- Must be deterministic and reproducible given the same input.

### Matching (`src/matching/`)

Compares feature sets and produces a similarity score or decision.

- Supports 1:1 verification and 1:N identification modes.
- Pluggable algorithm backends (threshold and scoring strategy configurable).
- Returns structured results with confidence metadata.

### API (`src/api/`)

HTTP/gRPC service layer exposing the pipeline to networked clients.

- Thin layer over the core pipeline; no business logic.
- Authenticated and rate-limited by default.
- Versioned endpoints to allow non-breaking evolution.

### CLI (`src/cli/`)

Command-line interface for local use, scripting, and integration testing.

- Mirrors API functionality for offline and developer use.
- Human-readable and machine-readable (JSON) output modes.

## Principles

1. **Privacy by design.** No real biometric data enters the repository.
   Synthetic or anonymised samples are used for tests only.
2. **Modularity.** Components interact through documented interfaces.
   Swapping an algorithm or transport should not ripple across the codebase.
3. **Fail-safe defaults.** Deny-by-default access control; errors surface
   clearly rather than silently degrading.
4. **Auditability.** All matching decisions are logged with enough context to
   reproduce and review them.
5. **Build-system agnosticism (early stage).** No toolchain is mandated until
   the community agrees on a language and build approach.
