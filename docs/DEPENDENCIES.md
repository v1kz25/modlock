# Dependencias y licencias — setup #3 / distribución #10

Revisión: **22-11-2026**, Windows 11 x64 / CPython 3.12.14. El propietario eligió expresamente MIT para modlock en #10. LICENSE y THIRD_PARTY_NOTICES.md se incluyen en wheel y sdist. No se redistribuyen wheels ajenas ni intérprete; las dependencias conservan sus avisos upstream.

## Necesidad y compatibilidad

Una dependencia directa de runtime (Typer), dos herramientas de desarrollo (pytest y Ruff) y un backend pequeño sin dependencias externas (flit_core). Pydantic y las demás transitivas se instalan porque esta versión de Typer los requiere; no se añade un framework de modelos al código de modlock. No se añaden gestores de entornos, typecheckers, plugins de tests ni publicación.

La resolución para CPython 3.12/Windows x64 contiene las 19 distribuciones de la tabla, incluido el backend. Se descargaron wheels públicas, verificando SHA-256, METADATA y textos LICENSE/NOTICE incluidos antes de instalarlas; después se contrastaron las versiones instaladas. [requirements-dev.txt](../requirements-dev.txt) fija versiones y hashes exactos. Las wheels quedan locales en `.venv/wheels`, ignoradas por Git. Los enlaces PyPI identifican las distribuciones primarias revisadas, sin inferir licencias de versiones distintas.

## Licencias directas y transitivas resueltas

| Distribución | Versión | Uso | Licencia declarada / texto incluido |
|---|---|---|---|
| [Typer](https://pypi.org/project/typer/0.29.2/) | 0.29.2 | Directa: runtime | MIT |
| [pytest](https://pypi.org/project/pytest/9.2.0/) | 9.2.0 | Directa: pruebas | MIT |
| [Ruff](https://pypi.org/project/ruff/0.17.6/) | 0.17.6 | Directa: lint/formato | MIT |
| [flit_core](https://pypi.org/project/flit-core/4.2.0/) | 4.2.0 | Directa: backend | BSD-3-Clause |
| [annotated-doc](https://pypi.org/project/annotated-doc/0.0.7/) | 0.0.7 | Transitiva: Typer | MIT |
| [annotated-types](https://pypi.org/project/annotated-types/0.8.0/) | 0.8.0 | Transitiva: Pydantic | MIT |
| [Colorama](https://pypi.org/project/colorama/0.4.6/) | 0.4.6 | Transitiva: terminal Windows | BSD-3-Clause |
| [iniconfig](https://pypi.org/project/iniconfig/2.3.1/) | 2.3.1 | Transitiva: pytest | MIT |
| [markdown-it-py](https://pypi.org/project/markdown-it-py/4.3.0/) | 4.3.0 | Transitiva: Rich | MIT |
| [mdurl](https://pypi.org/project/mdurl/0.1.2/) | 0.1.2 | Transitiva: markdown-it-py | MIT |
| [packaging](https://pypi.org/project/packaging/26.3/) | 26.3 | Transitiva: pytest | Apache-2.0 OR BSD-2-Clause |
| [pluggy](https://pypi.org/project/pluggy/1.7.0/) | 1.7.0 | Transitiva: pytest | MIT |
| [Pydantic](https://pypi.org/project/pydantic/2.14.4/) | 2.14.4 | Transitiva: Typer | MIT |
| [pydantic_core](https://pypi.org/project/pydantic-core/2.50.5/) | 2.50.5 | Transitiva: Pydantic | MIT |
| [Pygments](https://pypi.org/project/Pygments/2.21.0/) | 2.21.0 | Transitiva: Rich/pytest | BSD-2-Clause |
| [Rich](https://pypi.org/project/rich/15.0.0/) | 15.0.0 | Transitiva: Typer | MIT |
| [Shellingham](https://pypi.org/project/shellingham/1.5.4/) | 1.5.4 | Transitiva: Typer | ISC |
| [typing-inspection](https://pypi.org/project/typing-inspection/0.4.5/) | 0.4.5 | Transitiva: Pydantic | MIT |
| [typing_extensions](https://pypi.org/project/typing-extensions/4.16.0/) | 4.16.0 | Transitiva: Pydantic | PSF-2.0 |

Typer requiere Python >=3.11, pytest >=3.10, Ruff >=3.7 y flit_core >=3.8. Son requisitos de las herramientas, no la política de soporte de modlock. La familia 3.12 elegida y ensayada se justifica en [DEVELOPMENT.md](DEVELOPMENT.md). Se instalaron pydantic_core cp312-win_amd64 y Ruff win_amd64 sin compiladores.

También se revisaron los avisos de código incluido: `typer/_click/LICENSE.txt` (Pallets/Click, BSD-3-Clause), `flit_core/vendor/tomli-1.2.3.dist-info/LICENSE` (MIT), y `LICENSE.markdown-it` dentro de markdown-it-py (MIT). Packaging ofrece una elección Apache-2.0 **o** BSD-2-Clause. La licencia principal de una herramienta no sustituye los avisos de sus componentes. Los textos permanecen en los paquetes instalados; no se copian implementaciones a modlock.

## Bootstrap existente, separado del proyecto

El runtime existente aportó CPython 3.12.14 ([licencia PSF y avisos](https://github.com/python/cpython/blob/3.12/LICENSE)) y `venv/ensurepip`; este último creó pip **25.0.1**, MIT, en ambos entornos locales. No se actualizó ni instaló pip globalmente. Se inspeccionó su `vendor.txt` y se consultó metadata primaria PyPI de cada componente incluido. Estas son declaraciones de proveedores del bootstrap, no nuevas dependencias de runtime de modlock:

| Componentes incluidos en pip 25.0.1 | Licencia declarada |
|---|---|
| CacheControl 0.14.1, distro 1.9.0, msgpack 1.1.0, requests 2.32.3 | Apache-2.0 |
| distlib 0.3.9, typing_extensions 4.12.2 | PSF-2.0 |
| packaging 24.2 | Apache-2.0 OR BSD-2-Clause |
| platformdirs 4.3.6, pyproject-hooks 1.2.0, urllib3 1.26.20, rich 13.9.4, setuptools 70.3.0, tomli 2.2.1, truststore 0.10.0 | MIT |
| certifi 2024.8.30 | MPL-2.0 |
| idna 3.10 | BSD-3-Clause |
| Pygments 2.18.0 | BSD-2-Clause |
| resolvelib 1.0.1 | ISC |

Las declaraciones se consultaron en `https://pypi.org/pypi/<nombre>/<versión>/json`; inventario de referencia: [pip 25.0.1 vendor.txt](https://github.com/pypa/pip/blob/25.0.1/src/pip/_vendor/vendor.txt). No se presenta como auditoría de fuentes completa de pip ni se redistribuyen sus componentes.

## Alcance y obligaciones

La revisión cubre el grafo Python resuelto, sus textos de licencia y avisos incluidos identificados, más las declaraciones del bootstrap. Las licencias revisadas permiten uso local sin cuota obligatoria; conservar copyright, licencias y avisos cuando corresponda redistribuir. No se incorpora Meteoric/GPL como dependencia ni se copia código suyo.

No se audita el árbol de compilación Rust/C de cada binario upstream ni se prepara redistribución de intérprete o ejecutable. Un empaquetado distribuible requeriría revisar sus componentes y avisos concretos. La selección MIT satisface la decisión pendiente de licencia propia; no cambia las licencias upstream. requirements-runtime.txt contiene solo las 13 distribuciones de runtime del mismo grafo/hashes ya revisados; requirements-dev.txt conserva las 19. No se certifican otras plataformas/familias de Python. Al cambiar dependencias, revisar de nuevo licencias y hashes y repetir instalación, tests, lint y smoke.


## Typecheck de #15 (23-11-2026)

Mypy 2.4.1 se añade solo a desarrollo porque #15 exige typecheck real. Se eligió
la versión estable consultada en PyPI y wheels compatibles comprobadas para
CPython 3.12/Windows x64, no se cambia el rango Python del producto. Una sola
herramienta directa, sin extras/daemon/plugins. Runtime de modlock no cambia.
El lock de desarrollo pasa de 19 a 24 distribuciones; runtime mantiene 13.

| Distribución | Versión | Licencia/avisos inspeccionados |
|---|---|---|
| [mypy](https://pypi.org/project/mypy/2.4.1/) | 2.4.1 | MIT; Typeshed incluido Apache-2.0 |
| [mypy-extensions](https://pypi.org/project/mypy-extensions/1.2.0/) | 1.2.0 | MIT |
| [pathspec](https://pypi.org/project/pathspec/1.1.1/) | 1.1.1 | MPL-2.0, LICENSE de wheel y classifier del proveedor |
| [librt](https://pypi.org/project/librt/0.17.0/) | 0.17.0 | MIT |
| [ast-serialize](https://pypi.org/project/ast-serialize/0.13.1/) | 0.13.1 | MIT y crates/LICENSE MIT (Ruff crates) |

Se revisaron metadata Requires-Python/Requires-Dist, compatibilidad de tags y
SHA-256 de las cinco wheels antes de instalarlas offline en venv. typing_extensions
ya está fijada en el grafo previo; tomli no se requiere en Python 3.12. No se
instalaron extras psutil/lxml/orjson/setuptools ni las alternativas de Pathspec.
No se redistribuyen herramientas de desarrollo en la wheel de modlock. Pathspec
no se modifica ni copia; si se redistribuyera, conservar avisos y cumplir MPL-2.0
sobre ese componente. Esto no cambia la licencia MIT del código propio.
Typeshed/avisos permanecen dentro de las wheels upstream. No se certifica el
árbol Rust completo de los binarios; mismo límite de revisión previo.
