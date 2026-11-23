# Identidad e incertidumbre — issue #7

Alcance: modelo interno para **un export** del [formato estudiado](formats/meteoric-json-v1.md), después de `read_meteoric`. No compara listas, no decide correspondencias ni añade comandos de CLI o informes. La instrucción posterior del propietario «sigue con la siguiente tarea» autoriza #7 tras integrar #6; conserva el veredicto histórico CONTRIBUIR y no lo convierte en demanda demostrada ni autorización del MVP.

## Qué puede comprobarse con estos datos

Un ID numérico superior identifica una página declarada; `installed.files[].modid/fileid` aporta referencias declaradas a archivos. El lector permite comprobar su presencia, forma, coherencia local y repeticiones. No consulta Nexus para verificar que existan. **No hay juego, hash de contenido ni selección FOMOD completa en este formato**: ninguna clave construida aquí demuestra identidad global del mod ni igualdad de instalaciones.

Por ello se distingue evidencia de referencia completa dentro del export de una identidad verificada externamente. `FileReference(page_id, file_id)` tiene contexto limitado al origen leído, cuyo juego no se conoce. No es una clave global. Antes de una comparación futura habrá que decidir cómo se acredita ese contexto; #7 no introduce un juego supuesto ni un ID nuevo.

Nombres, versiones, archivo de instalación, tags y plugins son pistas conservadas en `original`; no prueban identidad por sí solos. No se limpian versiones, no se recuperan IDs/versiones de nombres, no se comparan conjuntos de plugins ni se usa fuzzy matching.

## Modelo y API interna

`modlock.identity.normalize_export(export: MeteoricExport) -> NormalizedExport` recibe el resultado validado del lector #6. No lee ni escribe archivos ni usa red. No es un segundo parser de objetos arbitrarios. Los modelos son de desarrollo, sin contrato público estable ni esquema de exportación universal.

- `NormalizedExport`: procedencia `source`, registros en su secuencia original y advertencias del lector sin perderlas.
- `NormalizedRecord`: `original`, copia del registro leído con todos sus valores decodificados, y `identity`, la evidencia de ese registro.
- `IdentityEvidence`: `state`, referencias numéricas ordenadas, motivos de incertidumbre e índices de los otros registros implicados en colisiones locales.

Se realiza una copia separada del resultado del lector: normalizar no lo modifica y cambiar después los diccionarios originales del lector no cambia el modelo ya obtenido. Los diccionarios dentro de `original` siguen siendo mutables, como en #6; tratar el modelo devuelto como solo lectura. La evidencia se calcula al normalizar, no se recalcula si el consumidor modifica esas copias.

No se descarta ningún registro, incluidos separadores, nombres/IDs repetidos o entradas ambiguas. `original` conserva índice, orden declarado, activación, nombres Unicode, metadatos parciales/vacíos, campos desconocidos y orden de los archivos instalados. Los motivos e índices se ordenan para que el resultado sea determinista. No se normaliza ni se usa la ruta de procedencia como identidad.

## Estados

| Estado | Condición | Alcance de la afirmación |
|---|---|---|
| `referenced` | Página superior numérica, lista completa no vacía de referencias válidas, sin contradicciones ni colisiones detectadas | Evidencia local completa; **no** mod verificado ni instalación reproducible certificada |
| `incomplete` | Falta página numérica, referencias válidas o integridad de la lista declarada | Identidad no resuelta; se conservan las referencias parciales disponibles |
| `ambiguous` | Referencia repetida, metadatos de página contradictorios/no corroborables o colisión de nombre | No elegir arbitrariamente un registro ni fusionarlo con otro |
| `not_applicable` | Separador | No es contenido instalado; no participa en índices de identidad de mods |

`ambiguous` tiene precedencia si también faltan datos. Todos los motivos se conservan, no solo el primero. Una versión ausente/vacía no invalida por sí sola una referencia explícita a archivo: se conserva como tal, junto con el aviso de lectura y el valor original. `referenced` no equivale a ausencia de advertencias del lector ni certeza de reproducibilidad.

## Reglas concretas

1. El campo superior `id` solo sustenta página numérica cuando el lector lo entrega como entero. Un ID textual como `"101"` sigue siendo texto y no se convierte en página a partir del nombre o de otros metadatos.
2. Dentro de `installed.files`, ambos identificadores deben ser strings decimales ASCII positivos para construir una referencia numérica. `"00101"` y `"101"` representan el mismo número en esa evidencia; los strings originales permanecen intactos. No se eliminan espacios, signos o puntuación ni se convierten dígitos de otros alfabetos. Un valor no representable por el límite de conversión del intérprete permanece desconocido.
3. Una referencia necesita su propio `modid` y `fileid`: no se rellena un campo ausente usando el ID superior. Se conservan todas las referencias válidas parciales y todo el objeto original, incluidos los elementos inválidos que no pueden convertirse en referencia.
4. Si el `general.modid` no vacío no corrobora la página superior conocida, o un archivo declara otra página, se marca `conflicting_page_id`. No se reemplaza el dato contradictorio. Si la página superior falta, metadatos adicionales no la suplen automáticamente.
5. El tamaño ausente o distinto de la longitud real marca `incomplete_file_list`. Ausencia, cero y conteo negativo siguen diferenciados por `original`. Una lista vacía o referencias sin IDs válidos marcan `missing_file_reference`; `missing_page_id` señala ausencia de página numérica superior.
6. Una referencia `(página, archivo)` repetida en uno o varios registros marca **todos** los implicados con `duplicate_reference`. Las ocurrencias repetidas siguen en la tupla, sin deduplicación. Una intersección parcial de listas de archivos también se marca; no constituye una unión, split o match. Compartir solo página con archivos distintos no es duplicado. Compartir solo número de archivo en páginas distintas tampoco.
7. `modName.casefold()` se usa únicamente como detector conservador de colisiones locales (`name_collision`). Puede producir advertencias conservadoras como `Straße`/`STRASSE`; no certifica la equivalencia de nombres de MO2/Windows, ni produce una clave de identidad, ni modifica el nombre. No se recortan espacios, sufijos o tags ni se aplica normalización de composición Unicode. Variantes canónicamente equivalentes de Unicode pueden quedar distintas; no se promete detectar todas las colisiones posibles.

Los índices de colisión identifican posiciones de otros registros del mismo export. Una repetición dentro de un único registro no inventa un segundo registro: tiene motivo `duplicate_reference` e índices ajenos vacíos. Los separadores no entran en los índices de nombres o referencias de mods.

## Fixtures y verificación

`tests/fixtures/identity/export.json` es un export sintético con nueve registros (un separador y ocho mods), basado en los campos validados en #2. No son IDs consultados ni mods descargados. Incluye referencia con ceros iniciales, página compartida con archivos distintos, referencia duplicada, colisión de nombre limpio entre tags/mayúsculas y conteo parcial.

`expected.json` contiene expectativas de identidad escritas independientemente del resultado del código. La vista JSON que compara ese golden existe **solo en tests**: no es un serializador de producto ni un informe público. Los valores completos y la procedencia se verifican por separado para no ocultar pérdida de datos detrás de esa vista reducida.

Las pruebas verifican también IDs textuales, valores ausentes/vacíos, dígitos no ASCII y otros tokens inválidos, páginas contradictorias, duplicados internos y solapamientos parciales, referencias iguales en páginas distintas, mayúsculas/Unicode sin reescritura, versión desconocida, export vacío, independencia de copias y ausencia de I/O en la normalización. Dos importaciones repetidas producen el mismo modelo. Para contenidos iguales leídos desde rutas distintas coinciden registros/evidencia, pero se conserva cada ruta de procedencia.

Comandos desde la raíz tras la instalación local:

```powershell
& .\.venv\Scripts\python.exe -m pytest -q
& .\.venv\Scripts\python.exe -m ruff check src tests
& .\.venv\Scripts\python.exe -m ruff format --check src tests
& .\.venv\Scripts\python.exe -c "from collections import Counter; from modlock.meteoric import read_meteoric; from modlock.identity import normalize_export; r = normalize_export(read_meteoric('tests/fixtures/identity/export.json')); print(sorted(Counter(x.identity.state for x in r.records).items()))"
# [('ambiguous', 4), ('incomplete', 1), ('not_applicable', 1), ('referenced', 3)]
```

Resultados ejecutados el 22-11-2026, Windows 11 x64 / CPython 3.12.14:

| Verificación | Resultado |
|---|---|
| Suite completa, incluidos lector y CLI previos | **94 tests OK** en `.venv` y `.venv/clean` |
| Golden independiente y conservación de originales/procedencia/advertencias | OK |
| Ruff `check src tests` | OK en ambos entornos |
| Ruff `format --check src tests` | Ocho archivos formateados |
| Reinstalación editable en segundo entorno, sin build isolation ni resolver dependencias | OK |
| `pip check` | Sin requisitos rotos en ambos entornos |
| Smoke documentado | 4 ambiguos, 1 incompleto, 1 separador y 3 referencias completas locales |
| Importación y normalización con el segundo intérprete desde fuera del repositorio | OK |

No se necesita una prueba manual de usuario ni una lista privada. No se añaden dependencias ni se cambia la licencia propia pendiente. No se certifican otros formatos, juegos, contextos o instalaciones reales.

Después de revisar e integrar #7, el siguiente issue técnico sería #4 (motor sobre modelos normalizados), con nueva autorización. No se inicia comparación, conexión a CLI, informes, CI, publicación ni otra fase en esta tarea.
