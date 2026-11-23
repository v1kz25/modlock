# CLI experimental #8

`modlock compare BASE HEAD` lee únicamente dos archivos explícitos del formato Meteoric estudiado. La operación es offline. Sin `--context` todos los mods quedan sin correspondencia confirmada. `--context JUEGO:LINAJE` es una declaración del llamador de mismo juego y linaje de exportación, no algo que modlock pueda verificar. No usarla para comparar listas sin contexto conocido. Las reglas del [motor](COMPARISON.md) se aplican sin heurísticas nuevas en CLI.

```powershell
& .\.venv\Scripts\modlock.exe compare docs/research/issue-2/fixtures/valid/03-metadata.json docs/research/issue-2/fixtures/valid/03-metadata.json --context synthetic:example
& .\.venv\Scripts\modlock.exe compare BASE.json HEAD.json --context JUEGO:LINAJE --format markdown --output NUEVO.md
```

El primer comando es un smoke sintético sin diferencias y no valida instalaciones reales. El segundo muestra la sintaxis para archivos explícitos. `--format json` es el valor predeterminado; `--format markdown` incluye tabla humana y toda la evidencia JSON, sin perder hallazgos. El esquema `modlock-0.1-experimental` puede cambiar antes de estabilidad.

Salidas UTF-8 deterministas, JSON con claves ordenadas y caracteres escapados. Markdown escapa texto de tablas y usa un fence dinámico para evidencia que contiene backticks. Los informes incluyen categorías, campos modificados, motivos, contexto declarado, advertencias del lector y datos originales decodificados. No insertan automáticamente rutas de origen del sistema; los metadatos originales sí pueden contener nombres/rutas proporcionados por quien generó el export. Mantener los informes locales cuando esos datos sean privados; la herramienta no transmite datos.

Sin `--output`, escribe a stdout; con `--output`, crea un archivo nuevo de forma exclusiva. Nunca sobrescribe exports o informes existentes; tampoco referencias mediante symlinks que ya existen. No abre rutas mencionadas dentro del JSON. No crea directorios automáticamente ni altera los exports en error.

| Código | Significado |
|---|---|
| 0 | Comparación e informe completados, incluso con diferencias/ambigüedades |
| 1 | Error de lectura/formato/contexto o imposibilidad de crear salida nueva |
| 2 | Uso inválido de CLI, argumento u opción no soportados |

`--help` y `--version` siguen disponibles; sin argumentos se muestra ayuda con 0. No hay descarga de mods, resolución de conflictos, autenticación ni conclusión sobre compatibilidad. Pruebas: `python -m pytest -q`, Ruff check/format desde el entorno local. Corpus sintético, golden JSON, JSON/Markdown repetibles, contexto ausente, warnings, escaping hostil, archivos intactos y fallos/códigos. No se necesita una prueba manual de usuario para #8.

## Extensión opcional #11 (desarrollo v0.2)

`--audit` añade señales de reproducibilidad a ambos lados, sin cambiar el matching ni el JSON sin flag. Ver [contrato y límites](AUDIT.md). La extensión es opt-in y desconocidos siguen unknown. No implica auditoría de archivos instalados.

Comparación de archivos guardados como snapshots, repetibilidad/reversibilidad y privacidad: [SNAPSHOTS.md](SNAPSHOTS.md). No se introduce formato nuevo ni comando de restauración.

## Presentación de revisión #14

Markdown incorpora Summary por categoría (incluye ambiguous), Reader warnings por lado/ubicación/código/mensaje y, solo con --audit, recuentos de señales unknown. Mantiene íntegra la tabla de cambios y Complete evidence. Todas las celdas se escapan con las mismas reglas, incluso advertencias, categorías y señales. El payload JSON completo puede extraerse sin perder hallazgos.

No se cambia el esquema JSON: summary, warnings y changes ya aportaban la evidencia requerida; audit sigue opt-in con su schema propio. El layout Markdown sí añade secciones; no analizarlo como API tabular estable, consumir JSON para integración. Snapshot de revisión sintético (metadata parcial), igualdad del JSON embebido, casos hostiles/Unicode y vacío protegen la salida. No implica compatibilidad ni certificación de contenido.
