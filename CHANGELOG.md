# Changelog

## 1.0.0

Contract stabilization for the documented Meteoric input and local CLI/reports.
Prepared for human candidate review in #19; publication/tag state is recorded
in GitHub, not inferred from this version heading.

- Public 1.x CLI/JSON contract, unknown fallbacks and deprecation policy, based
  on owner feedback for v0.2 and golden compatibility with the published v0.1 wheel.
- Existing JSON schema IDs/payload retained as opaque legacy identifiers;
  optional audit unchanged. Internal APIs are outside the public contract.
- Version/help/package wording and two Markdown headings become version neutral;
  complete evidence unchanged. No new parser, dependency or matching heuristic.
- Incorporates corrected dangling output handling, native filesystem matrix,
  offline wheel/sdist verification, license inventory and maintenance guide.

Scope is a stable limited interface, not certified installed content, game,
compatibility, TOCTOU isolation, untested platforms or evidence of market demand.
Historical CONTRIBUIR and owner decision remain distinct.

## 0.2.0a2 — 2026-11-23

- Fix Windows dangling output symlinks: lstat rejects an existing final entry
  before exclusive creation. A real Windows CI regression caught creation of
  the absent target with open(x) in earlier prereleases. Those releases retain
  their bytes and a known-issue note; this does not claim TOCTOU isolation.
- Native filesystem/format matrix: real CI symlinks (no skips), hardlinks,
  read-only attribute and explicit-input-only access. Windows 11 cannot create
  file symlinks here (1314); those four local cases remain explicitly skipped.
- Distribution checks for complete wheel content, metadata, entrypoint, own
  license notices, exact runtime dependency closure and offline repeatable build.
- Windows support/maintenance guide; no new runtime/development dependencies.

Still experimental. #16 needs v0.2 feedback and #19 human review before stable.

## 0.2.0a1 — 2026-11-23

- Optional --audit records present/unknown reproducibility signals per mod/side;
  no fabricated content hashes, provenance or game verification.
- More semantic golden cases; whitespace versions remain version_metadata.
- Saved exports verified as snapshots, including inverse comparisons, Unicode,
  BOM, bounded input and unchanged original files.
- Markdown category counts, reader warnings and optional unknown summaries;
  complete JSON evidence retained. Default JSON schema/fields stay compatible.
- Full format corpus through optional audit in JSON/Markdown, Windows CI,
  gradual Mypy typecheck and verified source/wheel distributions.

Still experimental: no installed-content audit, conflict detection, guaranteed
reproducibility or stable public contract. Migration: docs/MIGRATION-0.2.md.

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
