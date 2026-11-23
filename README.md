# modlock

CLI **1.0.0** para comparar exports Meteoric locales y registrar evidencia de
reproducibilidad, conservando las ambigüedades. Contrato público de CLI/informes
para un formato documentado; APIs internas fuera de ese contrato.

## Uso

[Instalación y verificación de paquetes](docs/RELEASE-1.0.md) en venv local,
CPython >=3.12,<3.13 / Windows x64. [Versiones publicadas](https://github.com/v1kz25/modlock/releases).
No instalar globalmente ni cambiar Windows. No es un ejecutable autónomo.

```powershell
& .\.venv\Scripts\modlock.exe --help
& .\.venv\Scripts\modlock.exe --version
& .\.venv\Scripts\modlock.exe compare BASE.json HEAD.json --context JUEGO:LINAJE --audit --format markdown --output NUEVO.md
```

Solo declarar contexto si se conoce mismo juego Y linaje de exportación; no es
verificación del juego. Sin contexto, los mods permanecen ambiguos. `--audit`
añade señales present/unknown y es opcional. JSON es el formato predeterminado;
Markdown conserva toda la evidencia. Sin --output se usa stdout; con destino,
se crea un archivo nuevo y se rechaza una entrada final existente, incluido un
symlink roto. No se ofrecen garantías contra sustituciones concurrentes.

Código 0: operación correcta, incluso diferencias/unknown; 1: error de
entrada/salida/contexto; 2: uso inválido. [CLI](docs/CLI.md), [contrato 1.x](docs/PUBLIC-CONTRACT.md)
y [migración v0.1/v0.2](docs/MIGRATION-0.2.md).

## Alcance comprobado

Un [formato Meteoric JSON fijado](docs/formats/meteoric-json-v1.md), validación y
metadata original conservada, [identidad incierta](docs/IDENTITY.md),
[comparación conservadora](docs/COMPARISON.md), [señales de auditoría](docs/AUDIT.md)
y [exports guardados como snapshots](docs/SNAPSHOTS.md). Referencias exactas
localmente únicas y contexto conocido permiten correspondencias; cambiar fileid
no se supone actualización. Versiones/orden son metadata declarada.

No se comprueba contenido instalado, hashes, FOMOD, orden de carga o compatibilidad.
No hay instalación/descarga de mods, fuzzy, autenticación, restauración de
perfiles ni segundo parser. Content_hash/game/provenance siguen unknown.
Un informe raw puede contener datos privados del export: mantenerlo local y
revisarlo antes de compartir. La herramienta no transmite datos.

[Compatibilidad y límites Windows](docs/COMPATIBILITY.md): Windows 11 x64 /
CPython 3.12.14 local; Windows Server / 3.12.10 en CI con enlaces reales.
No se certifican otras plataformas ni symlinks Windows 11 omitidos por falta de
privilegio. Los IDs JSON heredados con texto experimental se conservan como
cadenas opacas para compatibilidad; no detectan versión/productor de entrada.

## Desarrollo y procedencia

[DEVELOPMENT.md](docs/DEVELOPMENT.md), [calidad](docs/QUALITY.md),
[mantenimiento](docs/SUPPORT.md), [roadmap](docs/ROADMAP.md) y [AGENTS.md](AGENTS.md).
Entornos y ejecución locales, dependencias fijadas con hashes, tests/Ruff/Mypy,
CI estándar gratuito en repo público. Coste adicional obligatorio **0 €**.

El [spike #1](docs/research/issue-1/REPORT.md) conserva **CONTRIBUIR** a Meteoric.
El propietario decidió después continuar como herramienta independiente y
complementaria y autorizó trabajo/publicaciones incrementales. Esto no demuestra
demanda ni justifica todo el backlog. [#20](docs/research/issue-20/REPORT.md)
rechaza por ahora el segundo formato aislado investigado. La publicación estable
se rige por la revisión del candidato exigida en #19; un número de versión en
fuente no significa por sí solo que exista su tag/release.

## Licencia

[MIT](LICENSE), elegida expresamente por el propietario. [Inventario de dependencias](docs/DEPENDENCIES.md)
y [avisos de terceros](THIRD_PARTY_NOTICES.md). Wheel propia sin intérprete ni
código/dependencias upstream empaquetados; sus distribuciones conservan avisos.
No se incorpora implementación GPL de Meteoric/MO2.
