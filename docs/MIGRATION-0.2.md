# Migración experimental v0.1 → v0.2

La CLI anterior sigue aceptada: compare BASE HEAD, --context, --format y
--output, ayuda/versión y códigos 0/1/2. No hay migración de archivos: se usan los
mismos exports Meteoric guardados. No aplicar informes como si fueran entradas.

JSON sin --audit conserva schema `modlock-0.1-experimental`, campos y reglas de
orden. Los campos desconocidos raw y advertencias se conservan. Consumidores
estrictos pueden seguir sin el nuevo flag. Con --audit aparece una sola clave
opcional audit, cuyo schema propio es `modlock-audit-0.2-experimental`.

Markdown incorpora Summary, Reader warnings y, con audit, Reproducibility
signals. La tabla de cambios y Complete evidence se mantienen, pero no se
garantiza layout tabular estable: para integrar, consumir JSON. Ambos formatos
son deterministas con mismos datos, versión y opciones.

Una corrección conservadora: cambio desde/hacia versión solo whitespace se
clasifica version_metadata, no version conocida. No se recorta ni reescribe el
raw; no es un comparador SemVer ni detección de actualización de contenido.

Las señales present son metadata declarada; content_hash, provenance y game
siguen unknown. --context es afirmación del llamador, no autenticación. Cambiar
fileid no fuerza matching. No hay snapshots de instalación ni restauración.

Python y runtime no cambian: CPython >=3.12,<3.13, Windows x64 probado. Mypy y
sus cinco distribuciones nuevas pertenecen al lock de desarrollo (24 total),
no al runtime (13). Ver DEPENDENCIES.md para avisos/licencias upstream.

Instalar v0.2 en un venv local nuevo; para volver a v0.1 usar sus propios assets
verificados y otro venv. No se modifican exports ni configuración de Windows.
No se publica una versión estable: todavía se requieren feedback real y
revisión humana para las puertas de v1.0. CONTRIBUIR histórico no cambia.
