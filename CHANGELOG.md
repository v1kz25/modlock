# Changelog

## 0.1.0a1 — 2026-11-22

First experimental prerelease, tested on Windows 11 x64 / CPython 3.12.14.

- One documented Meteoric JSON export structure, bounded read-only input,
  validation, unknown fields preserved and explicit uncertainty.
- Conservative reference comparison with caller-declared game/export-lineage
  context. Added/removed, metadata changes and relative order among settled
  pairs; changed file IDs are not inferred to be updates.
- `modlock compare`, help/version, deterministic JSON and Markdown, exclusive
  output creation and documented exit codes.
- Synthetic regression corpus, Windows CI and reproducible wheel/sdist with
  SHA-256 checksums; MIT selected explicitly by the owner.

This is not a stable audit product. No installed-content/hash verification,
game detection, fuzzy matching, snapshots, mod installation/download or network
service. Without explicit context, mods remain ambiguous. Context is an
assertion, not authentication. Reports can contain original private metadata.
The JSON schema and CLI may change. Other Python families/platforms are untested.

The issue #1 spike's historical verdict remains CONTRIBUIR. The owner's later
decision to continue and publish this limited experiment does not demonstrate
demand, validate the product or authorize v0.2.
