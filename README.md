# Openbiometrics

Open-source toolkit for field biometrics collection, processing, and matching.

## Project Status

**Early-stage scaffold.** The directory structure, documentation stubs, and
contribution guidelines are in place. Core implementation has not yet started.
All interfaces and architecture decisions are open for discussion.

## Goals

- Provide a modular, extensible platform for collecting biometric signals in
  field conditions (low-connectivity, resource-constrained environments).
- Implement privacy-by-design: no real biometric data stored in this repository.
- Expose a clean API and CLI so downstream tools can integrate easily.
- Remain build-system agnostic during early development; language and tooling
  choices will be made collaboratively.

## Repository Layout

```
Openbiometrics-/
├── docs/                  # Architecture, data policy, threat model
├── src/
│   ├── collector/         # Signal capture and sensor adapters
│   ├── processing/        # Pre-processing and feature extraction
│   ├── matching/          # Matching algorithms and scoring
│   ├── api/               # HTTP/gRPC service layer
│   └── cli/               # Command-line interface
├── models/
│   └── manifests/         # Model metadata and checksums (no binary models)
├── data/
│   └── schemas/           # JSON/Protobuf schemas (no real biometric data)
├── tests/                 # Integration and end-to-end tests
└── scripts/
    ├── dev/               # Local development helpers
    └── release/           # Release automation
```

## Contributing

Bug fixes and small, well-scoped improvements are welcome — feel free to open a
pull request directly.

For larger features or architectural changes, **please open an issue first** so
the approach can be discussed before implementation begins.

See [docs/architecture.md](docs/architecture.md) for design context.

## Security & Privacy

Biometric data is sensitive. Before contributing data-handling code, read
[docs/data-policy.md](docs/data-policy.md) and
[docs/threat-model.md](docs/threat-model.md).

## License

See [LICENSE](LICENSE).
