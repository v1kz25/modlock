# Primer formato estudiado: JSON de Meteoric 1.0

Issue: [#2](https://github.com/v1kz25/modlock/issues/2). Consulta y validación: **22-11-2026**.

## Decisión y alcance autorizado

Se selecciona para investigación el JSON del plugin **Modlist Compare** de Meteoric, especificación **1.0**, fijado al commit `1e34b9918a81239b71789a5472f6bc16ffdab70b`. La consulta de `main` de Meteoric coincidió con ese SHA. No es una declaración de soporte implementado ni un formato universal de MO2.

El [issue #1](../research/issue-1/REPORT.md) concluyó CONTRIBUIR. Tras la revisión, el propietario autorizó fusionar la [PR #21](https://github.com/v1kz25/modlock/pull/21) y realizar #2 como investigación limitada pese a ese veredicto. La base de esta rama es `develop` en `ee9fbcad2144be2bf6d362af150871b8bccc7ba5`. Esa autorización no sustituye el veredicto por CONTINUAR ni habilita #3, #6 o el MVP.

Entregables: descripción del formato, corpus sintético válido/anómalo/inválido, evidencia reproducible y plan de lectura. No se añade CLI, parser, esquema ejecutable, entorno, dependencias ni configuración de tests del producto.

## Fuentes primarias fijadas

Todos estos enlaces pertenecen al commit seleccionado:

- [Especificación 1.0](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/mo2-plugins/modlist_compare/FORMAT_SPECIFICATION.md): estructura y campos documentados.
- [exporter_core.py](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/mo2-plugins/modlist_compare/exporter_core.py): extracción efectiva, valores por defecto y manejo de fallos.
- [plugin_tools.py](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/mo2-plugins/modlist_compare/plugin_tools.py): escritura del JSON exportado.
- [Pruebas del exportador](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/mo2-plugins/modlist_compare/test_exporter_core.py) y ejemplos [1.0](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/examples/lists/Example%20List%201.0.json) / [1.1](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/examples/lists/Example%20List%201.1.json): contraste con muestras upstream, no incluidas en el corpus propio.
- [README del plugin](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/mo2-plugins/modlist_compare/README.md) y [licencia](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/LICENSE): requisitos y GPL v3.

El plugin declara versión **1.1.0** en `plugin_tools.py` y documenta MO2 2.5.0 o posterior; no se ha ejecutado una instancia MO2. Python ya disponible basta para ejecutar su núcleo con una API simulada. Los números 1.0/1.1 de los ejemplos son versiones de la lista, **no versiones del formato**.

## Contenedor, codificación y versión

El documento es un array JSON en UTF-8. Cada elemento describe un separador o mod. El exportador escribe con indentación de dos espacios; espacios y saltos no definen identidad. No se añaden comentarios al JSON. Un array vacío es alcanzable con una lista sin registros y no demuestra fallo de lectura.

No existe una propiedad de versión del esquema en el archivo ni un contenedor con juego, versión de MO2 o SHA del exportador. La versión se conoce por procedencia externa documentada. Un futuro lector no puede certificar el commit productor mirando solo la forma del JSON. No se modifica el formato para introducir un campo inventado.

Los fixtures usan UTF-8 sin BOM y LF; la política para BOM u otras codificaciones deberá fijarse con evidencia antes del lector #6. Un archivo UTF-8 inválido no se debe reparar silenciosamente. No confundir JSON malformado con un JSON bien formado cuyo contenido no pertenece a este formato.

## Campos de cada registro

Los once campos siguientes aparecen en la salida normal del exportador. Los tipos enteros se deducen del código productor; la especificación usa el término más amplio `number`. Un booleano no debe convertirse en un entero de identidad u orden.

| Campo | Representación observada | Significado y límites |
|---|---|---|
| `type` | `separator` o `mod` | Discriminador; un valor nuevo requiere estudiar otra variante |
| `id` | null en separador; entero positivo o string en mod | El entero procede de Nexus; en ausencia de ID positivo se usa el nombre limpio, no un identificador global |
| `separatorName` | string | Contexto de sección; empieza en `Unsectioned` y cambia al encontrar un separador |
| `modName` | string | Nombre con los tags iniciales eliminados; puede colisionar con otro registro |
| `displayName` | string | Nombre completo recibido de MO2; conservarlo sin reemplazarlo por el limpio |
| `plugins` | array de strings | Nombres de archivos de plugin, sin sus bytes ni hashes |
| `general` | objeto | Metadatos de General o `{}` si no se obtienen |
| `installed` | objeto | Referencias de installedFiles o `{}`; véanse fallos parciales abajo |
| `order` | entero desde cero | Posición consecutiva del elemento en el array, incluidos separadores |
| `tags` | array de strings | Grupos entre corchetes recogidos del nombre completo |
| `active` | booleano | Activación del mod; el productor fija true para separadores |

Un separador tiene `id=null`, `plugins=[]`, `general={}`, `installed={}` y `active=true`; su nombre limpio y contexto de sección coinciden. No representa un mod ni cuenta como contenido instalado. Su nombre se deriva eliminando tags iniciales y el marcador `_separator`.

Antes del primer separador, un mod pertenece a `Unsectioned`. Después, su `separatorName` corresponde al separador más reciente, no a una sección futura ni a cualquier nombre del documento. Array y `order` deben conservarse; no ordenar por nombre, deduplicar ni renumerar para ocultar una inconsistencia.

### `general`

Si se puede leer `[General]`, el productor entrega cinco strings: `modid`, `version`, `newestVersion`, `category`, `installationFile`. Las claves ausentes de esa sección se materializan como strings vacíos. Si la sección no existe, entrega `{}`. Son estados diferentes y ambos son válidos.

`modid` permanece como texto aunque el campo superior `id` sea numérico. `version` es el valor instalado registrado, sin garantía de semver; `newestVersion` es conocimiento local y puede estar obsoleto. `category` puede incluir comillas/comas. `installationFile` es una pista textual sobre el archivo de instalación: no demuestra existencia, integridad ni procedencia. No convertirla en ruta a leer o ejecutar.

### `installed`

En el caso normal: `size` es un entero no negativo y `files` un array de esa longitud. Cada entrada incluye `modid` y `fileid` como strings, que pueden estar vacíos. `size=0` con `files=[]` difiere de `{}`. Un mismo ID de página puede alojar varios archivos; un fileid no constituye por sí solo una identidad entre juegos o proveedores.

No hay checksum de contenido ni selección FOMOD completa. Compartir página/archivo no prueba igualdad de instalación. IDs ausentes, inconsistentes o repetidos son información incompleta/ambigua; no son licencia para inventar correspondencias.

### Nombres, Unicode y plugins

Solo se quita el bloque de tags del principio de `displayName` para producir `modName`; los tags interiores o finales se mantienen en el nombre limpio y también pueden figurar en `tags`. Dos nombres completos distintos como `[A] Local Patch` y `[B] Local Patch` generan el mismo nombre limpio e ID textual. Son dos registros válidos que deben conservarse.

Se enumeran nombres con sufijo `.esp`, `.esm` o `.esl` directamente en el directorio del mod, sin recursión, y se ordenan. No contienen el orden de carga de plugins, archivos de recursos ni prueba del contenido de los binarios. Se conserva el Unicode y la grafía de entrada; este spike no decide reglas de normalización para matching.

## Diferencias comprobadas entre especificación y productor

El tratamiento de fallos de `read_meta_ini` no garantiza que un objeto no vacío esté completo. Se ejecutaron estas dos entradas sintéticas con el productor fijado:

| Caso alcanzable | Salida real | Tratamiento propuesto para el futuro lector |
|---|---|---|
| installedFiles con `size=-1` | size negativo y array vacío | Conservar evidencia, advertir conteo anómalo; referencias desconocidas, sin usar ese tamaño para reservar memoria |
| size 2 y error de interpolación de ConfigParser en el segundo fileid | size 2 pero un solo elemento en files | Conservar el objeto parcial y advertir pérdida/incompletitud; no completar el segundo archivo |

El bloque de captura de excepciones puede dejar datos parciales ya asignados. Por ello estos archivos se separan como **anómalos emitidos por el productor**, no como JSON inventados ni como ejemplos normales conformes a todos los invariantes de la especificación. Tampoco se afirma que Meteoric los rechace: su carga JSON no constituye un validador estricto del esquema.

Un futuro lector deberá separar los errores estructurales que impiden interpretar registros de las advertencias sobre metadatos parciales. La política propuesta aquí no está implementada. No rechazar automáticamente toda una exportación real por una incidencia de metadatos ni ocultarla con valores por defecto.

## Corpus y evidencia

Ubicación: [issue-2](../research/issue-2/VALIDATION.md), [manifest.json](../research/issue-2/manifest.json), [fuentes sintéticas](../research/issue-2/sources.json).

| Grupo | Casos | Evidencia prevista |
|---|---:|---|
| Válidos | 6 | Vacío, Unicode y Unsectioned con plugins, metadatos completos, secciones vacías, colisión de nombre limpio, solo separador |
| Anómalos del productor | 2 | Tamaño negativo y estructura parcial reproducidos con el exportador real |
| Negativos | 11 | Raíz object/null, campo ausente, tipo incorrecto, discriminador desconocido, metadatos array, orden fraccional/con salto, sección inexistente, JSON truncado y UTF-8 inválido |

Todos los datos se inventaron para este experimento; no hay listas de usuarios ni archivos de juego. Los archivos de plugin usados para comprobar enumeración son placeholders vacíos temporales. No se descargan mods ni se consulta la existencia de IDs. `sources.json` es una descripción interna del montaje de prueba (nombre/API/meta.ini), no otro formato de exportación soportado.

Los negativos tienen una sola desviación respecto al fixture de control cuando es posible. Su condición se explica en VALIDATION; **no se anuncia que un parser modlock inexistente los haya rechazado**. Las pruebas de sintaxis usan exclusivamente los decodificadores UTF-8/JSON de Python. Los casos semánticos se contrastan por aserciones sobre esos ejemplos fijos y por inspección del contrato.

## Plan de lectura para una tarea posterior

Solo si se autoriza la implementación y sus dependencias:

1. Leer exclusivamente el archivo explícito, sin mutarlo ni seguir referencias de los campos. Acordar límites de tamaño, codificación y rutas/errores de Windows en #6 antes de implementarlos.
2. Separar decodificación, sintaxis JSON y estructura del documento en diagnósticos distintos, con posición/campo útil y sin incluir rutas privadas en ejemplos públicos.
3. Exigir array y registros interpretables, discriminador conocido, objetos y tipos primitivos coherentes. Un campo requerido ausente no equivale a vacío, null o false. No intentar adivinar un formato alternativo.
4. Preservar valores originales, índice, orden declarado, nombres, campos desconocidos y metadatos parciales. Advertir inconsistencias sin reparar silenciosamente. Las decisiones sobre compatibilidad de campos desconocidos y BOM requieren casos adicionales; no certificar otra versión por parecido.
5. Representar ausencia de referencias/versiones como desconocida. Conservar duplicados/colisiones; la definición de identidad corresponde a #7 y la comparación a #4, no al lector #6. No reutilizar el fuzzy matching para aceptar entradas malformadas.
6. Convertir la matriz del corpus en pruebas de aceptación cuando exista lector: válidos admitidos, negativos con diagnóstico, anomalías preservadas y advertidas, errores con originales intactos. Después abordar límites grandes, permisos/symlinks y compatibilidad MO2 real según el alcance que se apruebe.

No se seleccionan módulos, dependencias ni una versión de Python para producto en este documento. La licencia propia sigue pendiente. Meteoric es GPL v3; se inspecciona y ejecuta desde su checkout externo y no se incorpora su código al repositorio. Los fixtures propios contienen datos sintéticos y el esquema existente; no se copian modlists públicas cuya redistribución no se haya revisado.

## Resultado y límites

El formato queda suficientemente identificado para planificar una lectura conservadora: versión documental y SHA concretos, campos y ausencias diferenciados, corpus y discrepancias del productor reproducibles. La evidencia ejecutada y sus resultados están en VALIDATION.md. No se ha probado una GUI MO2 ni otras revisiones del exportador, ni integridad/descarga de mods.

No hay una prueba manual de usuario necesaria para este alcance documental. Si posteriormente se exige comprobar exportación desde MO2 real, deberá autorizarse con un perfil sintético y pasos explícitos en su PR; esta investigación no permite acceder a perfiles privados. Detenerse al entregar la PR del #2: cualquier fusión y cualquier issue posterior requieren autorización propia.

## Lector interno del issue #6

El estudio anterior registra el alcance histórico de #2. Después de integrar #3, el propietario autorizó continuar con #6. La implementación independiente está en `src/modlock/meteoric.py`; no se copia código de Meteoric ni se añaden dependencias. No implica que el archivo leído realmente proceda del commit estudiado: solo se reconoce su estructura conocida.

API interna (desarrollo, todavía sin contrato público estable): `read_meteoric(path, max_bytes=16*1024*1024)` devuelve `MeteoricExport` con ruta de origen, tupla de registros tipados y advertencias. Cada registro conserva índice, orden declarado, nombres, ID de origen, activación, plugins/tags, metadatos extraídos y `raw` con todos los valores decodificados. No hay identidad normalizada ni comparación. Dos nombres/IDs iguales siguen siendo dos registros. Las dataclasses impiden reasignar atributos; los diccionarios devueltos no son profundamente inmutables, pero cambiarlos no escribe el archivo.

Políticas adoptadas y comprobadas en #6:

- UTF-8 estricto con o sin BOM; UTF-16 y bytes UTF-8 inválidos se rechazan, sin recodificar el archivo. El BOM aceptado es una decisión de lectura comprobada con un caso sintético, no un nuevo campo de formato.
- Límite inicial de **16 MiB** de entrada, BOM incluido, configurable mediante entero positivo. Es una protección operativa para acotar la lectura completa, no un límite que publique Meteoric ni una garantía sobre memoria total o listas grandes. Se lee como máximo límite+1 bytes para detectar crecimiento después del stat. Los ensayos del límite usan tamaños pequeños equivalentes; no son un benchmark de listas de 16 MiB.
- Solo archivos regulares, abiertos como `rb`; no se abren rutas nombradas dentro del JSON. Una ruta explícita puede ser un enlace a un archivo regular, siguiendo el comportamiento de Path/open; no se ofrece aislamiento contra cambios concurrentes del sistema de archivos. No se prueba aquí una matriz de symlinks o ACL reales de Windows.
- Array y once campos superiores requeridos; tipos conocidos estrictos, sin convertir booleanos en enteros o strings en bool. `order` consecutivo y contexto de sección coherente; separadores con sus invariantes propios. No se reordenan, renumeran ni deduplican registros.
- Campos desconocidos aceptados y conservados en `raw`, con `unknown_field` en el objeto que los contiene. Los nombres/valores desconocidos no se reproducen en el texto del diagnóstico. No se interpretan como soporte certificado de una revisión futura.
- `general={}` difiere de cinco strings vacíos; `.general.get("version")` devuelve None si la clave falta y string vacío si estaba vacía. `installed.size/files` ausentes se representan como None, frente a 0/tupla vacía presentes. En archivos instalados faltantes, `.get("fileid")` devuelve None; no se crea un fileid vacío para sustituirlo.
- Metadatos parciales, versión vacía o referencias a archivos con campos ausentes/vacíos generan `incomplete_metadata`. Conteos negativos o que difieren de la lista real generan `metadata_count`; se conservan el conteo y los elementos recibidos sin completarlos. Tipos incorrectos en un campo conocido impiden leer la estructura y generan error.
- Claves JSON duplicadas se rechazan para evitar pérdida silenciosa de valores. Esto no es detección de mods duplicados. Constantes no estándar (NaN/Infinity), números no finitos al decodificarlos y límites propios del decodificador generan error controlado. `raw` conserva el valor JSON decodificado, no la representación textual de números/espacios ni los bytes del archivo.

`ReaderError` incluye `code`, `location` JSON y mensaje sin contenido privado del archivo. Categorías: `io` (acceso/ruta), `file_type`, `size`, `encoding`, `json`, `structure` y `unsupported` (tipo de registro desconocido). Errores JSON de sintaxis incluyen línea/columna. Los tipos JSON que no son registros se rechazan como estructura cuando el decodificador consigue leerlos. Un parámetro `max_bytes` inválido es un error de configuración ValueError, antes de leer.

Los tipos de lectura son estructuras del formato, no el modelo normalizado del #7. No se evalúa certeza de identidad, igualdad entre IDs/archivos, antigüedad de versiones, ni riesgos de reproducibilidad. No se conecta a la CLI: esa integración pertenece a un issue posterior.

### Comprobación local del lector

Desde la raíz, después de la instalación local documentada:

```powershell
& .\.venv\Scripts\python.exe -m pytest -q
& .\.venv\Scripts\python.exe -m ruff check src tests
& .\.venv\Scripts\python.exe -m ruff format --check src tests
& .\.venv\Scripts\python.exe -c "from modlock.meteoric import read_meteoric; r = read_meteoric('docs/research/issue-2/fixtures/valid/03-metadata.json'); print(len(r.records), len(r.warnings))"
# El smoke imprime 2 0: separador + mod, sin advertencias en ese fixture.
```

La suite incluye los 19 fixtures íntegros del manifiesto de #2: seis válidos, dos anómalos aceptados con advertencia y once negativos rechazados. Se comprueban repetibilidad y bytes intactos en éxito/error. Los casos adicionales prueban tipos sin coerción, desconocidos en cuatro niveles, faltantes frente a vacíos, Unicode/BOM/UTF-16, duplicación de claves, números no finitos, anidamiento, rutas y límites de lectura. El fallo de permisos se simula mediante monkeypatch: no se cambiaron ACL de Windows. Un rastreo de Path.open comprueba que se abre solo la entrada como rb y no las referencias a archivos o plugins.

Resultados finales ejecutados el 22-11-2026, Windows 11 x64 / CPython 3.12.14:

| Verificación | Resultado |
|---|---|
| Suite completa (incluye las ocho pruebas de CLI del setup) | **64 tests OK** en `.venv` y `.venv/clean` |
| Ruff `check src tests` | OK en ambos entornos |
| Ruff `format --check src tests` | Seis archivos formateados |
| Reinstalación editable sin build isolation/dependencias en el segundo entorno | OK; `pip check` sin requisitos rotos en ambos |
| Smoke documentado con fixture válido | `2 0` |
| Importación y lectura desde directorio ajeno al repositorio con el segundo intérprete | OK |
| Dependencias y licencia propia | Sin cambios; solo biblioteca estándar para el lector |

Un primer test asumía que 2.000 arrays anidados siempre provocarían un límite del decodificador; en este entorno se decodificaron y fallaron correctamente como registro de tipo inválido. La prueba final admite ambos diagnósticos controlados, sin exigir un límite interno idéntico entre decodificadores. Se añadió también un caso de ruta con NUL: se convierte en error `io` sin exponer la ruta.

No hay prueba manual obligatoria de usuario ni se solicita una lista privada. No se ha probado exportación desde una instancia real de MO2; el corpus y los datos nuevos son sintéticos. No se inicia #7 ni se fusiona la PR del #6 sin otra autorización.
