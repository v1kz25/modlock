# Third-party notices — modlock 1.0.0

modlock's own code and documentation are MIT licensed; see LICENSE. The owner
expressly selected MIT for issue #10 on 2026-11-22.

The modlock wheel contains its own Python package and license notices. It does
not bundle Python, pip, dependency wheels, Meteoric or other mod managers.
Dependencies are installed separately from their upstream distributions and
retain their original licenses and notices.

Runtime distributions (versions and wheel hashes: requirements-runtime.txt):

| License | Distributions |
|---|---|
| MIT | Typer, annotated-doc, annotated-types, Pydantic, pydantic_core, Rich, markdown-it-py, mdurl, typing-inspection |
| BSD-3-Clause | Colorama; Click code vendored inside Typer |
| BSD-2-Clause | Pygments |
| ISC | Shellingham |
| PSF-2.0 | typing_extensions |

Typer includes Pallets/Click's BSD-3-Clause LICENSE.txt; markdown-it-py
includes the MIT LICENSE.markdown-it. Keep these notices with the upstream
packages when redistributing those packages. They are not relicensed by MIT
for modlock.

Development distributions are not runtime dependencies: pytest (MIT), Ruff
(MIT), iniconfig (MIT), pluggy (MIT), packaging (Apache-2.0 OR BSD-2-Clause),
and build backend flit_core (BSD-3-Clause, vendored tomli MIT).

See docs/DEPENDENCIES.md in the source distribution/repository for the complete
versioned inventory, primary links, bootstrap notices and review limitations.
No upstream GPL implementation has been copied into this package. This review
does not audit all Rust/C source used to build upstream binary wheels.

Typecheck added in #15: Mypy 2.4.1 (MIT, bundled Typeshed Apache-2.0),
mypy-extensions 1.2.0 (MIT), Pathspec 1.1.1 (MPL-2.0), librt 0.17.0 (MIT),
ast-serialize 0.13.1 (MIT, Ruff crates MIT). Development only, unmodified and
not bundled in the modlock wheel; upstream distributions retain their notices.
