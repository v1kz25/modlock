# Issue #1 — Validación frente a Meteoric

Consulta y ejecución: **22 de noviembre de 2026**. Alcance: [issue #1](https://github.com/v1kz25/modlock/issues/1).

## Decisión propuesta: CONTRIBUIR

Hay brechas verificables en la presentación de incertidumbre, referencias a archivos y estado activo, pero Meteoric ya proporciona el comparador MO2, matching, changelog, diff visual, coverage y ejecución local que ocuparían gran parte del MVP propuesto. Conviene proponer una mejora acotada de auditoría en Meteoric antes de financiar con tiempo otro motor de comparación. Esto es una decisión técnica provisional: diez casos sintéticos no acreditan demanda de usuarios ni aceptación del mantenedor.

No iniciar #2, #3 ni el MVP. La decisión y esta evidencia quedan pendientes de revisión del propietario; no se cierra automáticamente #1 ni se contacta al proyecto externo. Reconsiderar un producto independiente solo con casos redistribuibles de usuarios, necesidad de auditoría demostrada y evidencia de que colaborar con Meteoric no resuelve esa necesidad.

## Estado y contraste del backlog

Árbol inicialmente limpio, rama `develop`. Remoto exclusivo de trabajo: `https://github.com/v1kz25/modlock.git`. `develop` local y remoto: `f7d021373fe4fae9675ef7a3dc002ee4aaea4a0b`; `main`: `502bfbe9fa3d520ebe618cb8ed050801697b157b`. Se ejecutó `git fetch origin` antes de crear `feature/1-meteoric-validation` desde `origin/develop`. Git conserva la identidad configurada, sin ajustes ni trailers de asistentes.

GitHub: #1–#4 y #6–#20 abiertos; #5 es la PR documental de Gitflow, fusionada; no había otras PRs ni releases. Se leyeron los cuerpos de todos esos issues, AGENTS.md, README, ROADMAP y DEVELOPMENT antes de editar. Los cuerpos consultados no asignan milestones: las versiones se proponen en los títulos/cuerpos, no son publicaciones ni fechas comprometidas. [Issues](https://github.com/v1kz25/modlock/issues), [PR #5](https://github.com/v1kz25/modlock/pull/5), [releases](https://github.com/v1kz25/modlock/releases).

Inconsistencias y solapamientos detectados:

- ROADMAP retenía una condición anterior sobre comenzar otro repositorio; la instrucción de esta sesión autoriza exclusivamente este spike de modlock y la sustituye.
- #4 ya acota el motor y remite lectura/modelo/reportes a #6/#7/#8; no duplicar esa implementación.
- #4 y #12 incluyen orden; delimitar antes de implementar qué se cubre experimentalmente y qué sería ampliación. #8/#14 comparten informes; #13 comparte comparación local de snapshots con #8. Deben justificar valor incremental.
- #11 coloca la auditoría en v0.2, aunque es precisamente la diferenciación que tendría que justificar #1. La comparación básica de v0.1 no demuestra esa diferenciación.
- #10/#15/#18 repiten controles de distribución en distintas puertas de madurez; reutilizar evidencia sin fingir que una versión previa garantiza estabilidad.
- #19 pide PR de release hacia `main`, mientras su párrafo Git genérico menciona `develop`. La regla específica de release de AGENTS/DEVELOPMENT resuelve ese caso futuro; no afecta a esta rama de spike.

No se recrean, editan masivamente ni cierran issues. El cambio de ROADMAP está incluido aquí porque comunica las consecuencias directas de #1, sin redefinir funciones ni comprometer versiones.

## Fuentes primarias y formato comprobado

Meteoric se descargó en un checkout temporal separado, sin modificación de sus archivos versionados: commit **`1e34b9918a81239b71789a5472f6bc16ffdab70b`**. Todo resultado ejecutado se refiere a ese commit, no a una versión futura.

- [README de Meteoric](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/README.md): requisitos Python 3.9+, exportador MO2 2.5.0+, herramientas sin dependencias externas para la comparación.
- [Especificación 1.0](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/mo2-plugins/modlist_compare/FORMAT_SPECIFICATION.md) y [exportador](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/mo2-plugins/modlist_compare/exporter_core.py): raíz array; registros `separator`/`mod`; orden secuencial; `id` numérico o nombre; `general`/`installed` pueden estar vacíos. Incluye `active`, tags, nombres, plugins y fileids; no incluye campo de hash de contenido ni contexto explícito de juego.
- [Matching y versiones](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/tools/modlist_utils.py): asignación por página con señales de archivo/nombre, plugins, nombre normalizado y fuzzy. Umbral por defecto 0.80. Los fileids sí participan en matching; no afirmar que Meteoric los ignora por completo.
- [Diff](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/tools/generate_diff.py): clasificación de movimientos entre secciones; presenta ambos órdenes, pero no clasifica un intercambio dentro de la misma sección como `moved` en el caso 03.
- [Coverage](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/tools/generate_coverage.py): distingue plugins, versiones y cobertura; una versión desconocida sin diferencia de plugins puede ser `common`. Su porcentaje de cobertura sirve a una tarea distinta de medir suficiencia de referencias.
- [Ejemplos y pruebas de Meteoric](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/tools/test_examples.py): cubren renombres, merges, movimientos y drift de plugins. Se ejecutó la suite de herramientas completa; esos escenarios no equivalen a validación de instalaciones reales.

El corpus se construyó después de leer especificación y exportador. Son veinte JSON de exportación sintética, agrupados en diez pares, no veinte exportaciones recogidas de usuarios. Todos se reproducen exactamente llamando al exportador real sobre una API MO2 simulada y archivos `meta.ini` sintéticos. Esto comprueba que el formato es alcanzable por el código del exportador. No se ejecutó MO2 ni se accedió a juegos, perfiles o mods del usuario.

## Métricas adicionales

**M1 — Cobertura de referencias explícitas a archivos (CRE).** Por snapshot: registros mod con versión explícita no vacía/desconocida y lista no vacía y completa de referencias `(id numérico de página, fileid positivo)` coherentes con `installed.size` y `files[].modid`, sin claves repetidas en ese snapshot, divididos entre todos los registros mod. Separadores excluidos. En este corpus todas las listas `installed.files` tienen longitud 1 o están ausentes. No se recuperan versiones del nombre del archivo para esta métrica: interesa la evidencia explícita. Permite detectar metadatos insuficientes y distinguir una página compartida de archivos concretos.

CRE no prueba integridad, disponibilidad de descarga, juego correcto, equivalencia de opciones FOMOD ni ausencia de modificaciones locales. El JSON no aporta hashes de bytes ni contexto explícito de juego; incluso 100% significa suficiencia de esas referencias dentro de un contexto de juego conocido externamente. No se consulta Nexus ni se atribuye existencia real a IDs sintéticos.

**M2 — Estabilidad de correspondencias (EC).** Pares de registros de la correspondencia base que se mantienen en **todas** las permutaciones de enumeración de candidatos viejos y nuevos, divididos entre pares de la correspondencia base. Se invoca la API `match_mods` con los mismos objetos y mismos valores de `order`, sin cambiar los exports. Se comparan conjuntos por `displayName`, único en cada snapshot. En el corpus hay como máximo dos mods por lado: se recorren exhaustivamente 1 o 4 combinaciones, no una muestra aleatoria. Sin pares el resultado sería no aplicable.

EC comprueba sensibilidad a desempates de enumeración, no equivalencia de listas reordenadas ni estabilidad de los informes completos. Con exports byte a byte idénticos Meteoric sí fue determinista en las repeticiones. EC=100% tampoco acredita una identidad correcta: el caso fuzzy 05 tiene un único candidato y carece de referencias. Conviene usar ambas métricas y conservar `unknown`.

## Diez pares: resultados ejecutados

`common` es una categoría de coverage de Meteoric, no una garantía de reproducibilidad. En todos los casos se ejecutaron changelog OLD→NEW, diff OLD→NEW y coverage NEW→OLD, sin ignores y con umbral 0.80. Cada comando se repitió y se compararon sus bytes. Los resultados detallados, correspondencias, estados y hashes están en [results.json](results.json); entradas en [fixtures](fixtures).

| Par | Identidad, versión y orden; incertidumbre/duplicados/metadatos | Meteoric ejecutado | Auditoría adicional candidata | CRE OLD→NEW | EC |
|---|---|---|---|---|---|
| 01 identical | Una página/archivo único, versión igual, orden igual; sin colisiones ni faltantes de referencia | 1 match; sin cambios; common | Informar alcance de referencias, sin prometer hashes | 1/1→1/1 | 1/1 |
| 02 version | Página igual, fileid y versión cambian; sin reordenación ni colisiones | 1 actualizado 1.0→2.0; newer | Conservar evidencia de fileid además de versión | 1/1→1/1 | 1/1 |
| 03 order | Dos identidades por archivo, intercambio dentro de Core; versiones iguales, referencias completas | 2 matches, cero moved en clasificación; HTML conserva ambos órdenes; common×2 | Cambio explícito de prioridad relativa; sin afirmar conflicto de carga | 2/2→2/2 | 2/2 |
| 04 section | Alpha cambia Core→Extras; Birch permanece; versiones iguales, sin colisiones | 2 matches; 1 moved; common×2 | Ya lo detecta el diff; solo añadir contexto de auditoría si se justifica | 2/2→2/2 | 2/2 |
| 05 fuzzy | Nombres locales Kit→Kits; versión y referencias ausentes; único candidato, identidad incierta | 1 match fuzzy; sin actualizaciones; common | Mostrar evidencia débil y unknown; estabilidad no es certeza | 0/1→0/1 | 1/1 |
| 06 shared-page | Dos mods de la misma página, fileids distintos, orden invertido; versiones iguales | 2 matches correctos por archivo; common×2; sin alerta de duplicado por página | Conservar ambos; no confundir página compartida con duplicado de archivo | 2/2→2/2 | 2/2 |
| 07 ambiguous | `[A] Local Patch` y `[B] Local Patch` distintos en MO2; mismo nombre limpio/id textual, sin metadatos, orden invertido | 2 matches cruzados, cero cambios y common×2; dos asignaciones al permutar | Conservar candidatos y colisión sin elegir identidad por orden | 0/2→0/2 | **0/2** |
| 08 missing-meta | Un mod local, igual nombre/orden; general e installed vacíos; versión desconocida | 1 match; cero actualizaciones; common | Referencias ausentes y contenido no verificable, aunque el nombre coincida | 0/1→0/1 | 1/1 |
| 09 file-change | Misma página/nombre/versión/orden, fileid 1001→1009; sin colisión | 1 match; cero actualizaciones; common | Advertir cambio de referencia a archivo sin inferir diferencia de bytes | 1/1→1/1 | 1/1 |
| 10 active | Identidad/versión/orden iguales, active true→false; referencias completas | 1 match; cero actualizaciones; common | Informar cambio de activación relevante a reproducibilidad | 1/1→1/1 | 1/1 |

CRE agregada: **10/14 = 71,43% por snapshot**, 20/28 contando ambos. EC agregada por pares: **12/14 = 85,71%**; nueve escenarios con 100%, uno con 0%. Se evaluaron 22 combinaciones de enumeración entre los diez casos. Estas cifras describen un corpus diseñado para explorar límites; no estiman prevalencia en modlists reales.

## Dos reproducciones directas revisadas

Además del runner, se ejecutaron directamente estos comandos y se leyó su salida. Desde la raíz de modlock, con `$python` apuntando a un ejecutable Python ya disponible y `$meteor` al checkout fijado:

```powershell
& $python "$meteor/tools/generate_changelog.py" docs/research/issue-1/fixtures/07-ambiguous/old.json docs/research/issue-1/fixtures/07-ambiguous/new.json
& $python "$meteor/tools/generate_changelog.py" docs/research/issue-1/fixtures/09-file-change/old.json docs/research/issue-1/fixtures/09-file-change/new.json
```

Ambos devolvieron Added=0, Removed=0, Updated=0. En 07, `results.json` registra A→B y B→A en la base y dos asignaciones distintas al enumerar candidatos. Los nombres completos son distintos, pero quitar los tags iniciales produce la colisión de nombre limpio. No se sabe si el contenido es igual: es justamente lo que no debe darse por probado. En 09, se verificó en los JSON el cambio de `installed.files[0].fileid`; no se alteró la versión. El resultado confirma que el informe de versiones no cubre ese cambio de referencia. No se afirma corrupción ni incompatibilidad.

Se revisaron también los resúmenes HTML de 03 y 04 como texto: 0 y 1 moved, respectivamente. No se hizo QA visual del HTML ni de la GUI MO2.

## Reproducción completa

No hay instalación de modlock, entorno virtual nuevo, pyproject ni dependencias nuevas. `run.py` es exclusivamente un experimento de corpus fijo: llama al exportador y herramientas upstream, mide resultados y comprueba hallazgos. No acepta formatos arbitrarios ni implementa matching de producto.

```powershell
# Elegir rutas temporales nuevas; no usar la carpeta de listas de un usuario.
$meteor = Join-Path $env:TEMP 'meteoric-issue1-review'
$output = Join-Path $env:TEMP 'modlock-issue1-review'
# $python debe ser la ruta de un intérprete disponible, no el alias de Microsoft Store.
git clone https://github.com/imightbemeteor/meteoric-modlist-tools.git $meteor
git -C $meteor checkout --detach 1e34b9918a81239b71789a5472f6bc16ffdab70b
& $python docs/research/issue-1/run.py $meteor $output
& $python -m unittest discover -s "$meteor/tools" -p 'test_*.py'
```

El runner exige SHA y checkout versionado intacto; rechaza un directorio de salida existente. Verifica los fixtures contra las definiciones sintéticas, crea los ausentes, compara exportador real con los veinte JSON, guarda informes solo en el destino nuevo, comprueba repetibilidad e integridad de entradas y escribe `results.json`. Comparar sus casos y hashes con el archivo versionado; el campo Python puede variar con otro intérprete. El `.gitattributes` de esta carpeta fija LF para conservar los bytes de los fixtures al hacer checkout en Windows, sin cambiar configuración Git. No se versionan plantillas HTML ni código GPL de Meteoric: se regeneran desde el checkout externo. La clonación requiere red; las comparaciones y el experimento no usan red ni credenciales.

Entorno ejecutado: Windows 11, versión del sistema 10.0.26300.0, Python **3.12.14** incluido en el runtime de Codex. Es la versión observada, no una selección de versión mínima para modlock. El alias `python` de Windows no estaba operativo en el sandbox; se usó el ejecutable existente del runtime, sin cambiar PATH ni Windows.

## Herramientas relacionadas: inspección, sin ejecución

- **MO2**, commit `4ba22f0d8b6f9e08e44008b8395cd774551b4ebe`: gestor de colecciones y prioridades, con funciones de instalación y gestión que están fuera del alcance de modlock. Se inspeccionaron [README](https://github.com/ModOrganizer2/modorganizer/blob/4ba22f0d8b6f9e08e44008b8395cd774551b4ebe/readme.md), [modlist.cpp](https://github.com/ModOrganizer2/modorganizer/blob/4ba22f0d8b6f9e08e44008b8395cd774551b4ebe/src/modlist.cpp) y licencia. El JSON estudiado lo produce el plugin de Meteoric; no se presenta como un export JSON nativo universal de MO2. No se evaluaron exhaustivamente todos sus plugins.
- **Wabbajack**, commit `a44228e42720e9a3c59dd97375328f2ac2e004ab`: el [README](https://github.com/wabbajack-tools/wabbajack/blob/a44228e42720e9a3c59dd97375328f2ac2e004ab/README.md) describe reproducción de instalaciones. Los modelos [ModList](https://github.com/wabbajack-tools/wabbajack/blob/a44228e42720e9a3c59dd97375328f2ac2e004ab/Wabbajack.DTOs/ModList/ModList.cs) y [Archive](https://github.com/wabbajack-tools/wabbajack/blob/a44228e42720e9a3c59dd97375328f2ac2e004ab/Wabbajack.DTOs/Archive.cs) incluyen juego, directivas, hash, tamaño y estado de descarga. Por inspección, ya existe representación de reproducibilidad más rica que el JSON Meteoric. No se ejecutó ni se probó disponibilidad de archivos o equivalencia de instalaciones. No concluir que carece de auditoría por no haberla ensayado.

## Evaluación técnica provisional y licencias

Python sigue siendo adecuado para una auditoría local de JSON: biblioteca estándar suficiente para este experimento, anotaciones de tipos, pruebas y manipulación de rutas. Su ejecución funcionó en Windows 11. Una biblioteca de lógica pura facilita verificar conservación de registros e incertidumbre. No hace falta un servidor ni IA.

Typer puede aportar ayuda y validación de argumentos a una futura CLI, pero no es necesario para aportar los hallazgos a Meteoric, que ya utiliza argparse. No justificar una CLI nueva solo por tipado: argparse más anotaciones internas también sirve. No se instala Typer ni se fija una versión. El [pyproject consultado](https://github.com/fastapi/typer/blob/2517edde5a1292a712e2f16e600754c52c6f00d9/pyproject.toml) requiere Python >=3.11 y declara Pydantic, Shellingham, Rich, annotated-doc y Colorama en Windows; esa es la metadata del commit consultado, no un lock ni una promesa sobre todas las versiones.

Comprobación primaria de licencias (22-11-2026):

| Componente | Evidencia | Resultado / límite |
|---|---|---|
| Meteoric | [LICENSE](https://github.com/imightbemeteor/meteoric-modlist-tools/blob/1e34b9918a81239b71789a5472f6bc16ffdab70b/LICENSE) | GPL v3; ejecución local separada; no copiar su implementación al producto sin resolver obligaciones |
| MO2 | [LICENSE](https://github.com/ModOrganizer2/modorganizer/blob/4ba22f0d8b6f9e08e44008b8395cd774551b4ebe/LICENSE) y cabecera del código | GPL v3, con cláusula de versión posterior en código inspeccionado |
| Wabbajack | [LICENSE.txt](https://github.com/wabbajack-tools/wabbajack/blob/a44228e42720e9a3c59dd97375328f2ac2e004ab/LICENSE.txt) | Declara GPLv3 para código y CC BY-NC-SA 4.0 para modlists; no se redistribuyen listas ni código |
| CPython | [LICENSE](https://github.com/python/cpython/blob/main/LICENSE) | PSF y avisos históricos/componentes; conservar avisos si se redistribuye runtime |
| Typer | [LICENSE](https://github.com/fastapi/typer/blob/2517edde5a1292a712e2f16e600754c52c6f00d9/LICENSE) | MIT |
| Pydantic | [LICENSE](https://github.com/pydantic/pydantic/blob/1aaef01805ae0bc436954a4e863cc0b64a827193/LICENSE) | MIT |
| Shellingham | [LICENSE](https://github.com/sarugaku/shellingham/blob/926401c4543b84f9f579932d30fb52a104639398/LICENSE) | ISC |
| Rich | [LICENSE](https://github.com/Textualize/rich/blob/3a109ccdffe5b2d0e30684a304fbd388e99ce57b/LICENSE) | MIT |
| annotated-doc | [LICENSE](https://github.com/fastapi/annotated-doc/blob/f8f99b4dec732a49411d19a55962ac71262603fb/LICENSE) | MIT |
| Colorama | [LICENSE.txt](https://github.com/tartley/colorama/blob/841634ed2a0da5d5ac2d867db533da8131266cb2/LICENSE.txt) | BSD de tres cláusulas |

No se auditaron ni resolvieron todas las dependencias transitivas de un futuro paquete. Si se autoriza #3, elegir una versión mantenida compatible con Windows 11 y revisar el árbol realmente resuelto, incluidas ruedas nativas y avisos. Una distribución sdist/wheel y ejecución en entorno de usuario pueden tener coste obligatorio 0 €; un ejecutable empaquetado requeriría otra decisión y auditoría. La [documentación oficial de Python para Windows](https://docs.python.org/3/using/windows.html) describe instalaciones aisladas/offline; no se realizó una instalación nueva ni smoke de un paquete modlock inexistente. La licencia propia sigue pendiente del propietario; no se añade LICENSE.

## Verificaciones y límites de aceptación

- **Experimento final:** PASS, 10 pares, 20 reproducciones con exportador real/API simulada, 60 ejecuciones CLI (tres herramientas × diez casos × dos repeticiones), igualdad de bytes en cada repetición, hashes de entradas intactos y aserciones de hallazgos. Las salidas factuales y hashes quedan versionados.
- **Suite upstream:** 307 tests en `tools`, OK. No representa tests de modlock ni prueba integral de MO2. No se creó configuración de tests del producto.
- **Reproducción directa:** casos 07 y 09, comandos independientes del runner y lectura de sus salidas, ambos con cero Added/Removed/Updated.
- **Revisión de formato:** especificación 1.0, exportador y ejemplos, seguida de comprobación exacta de los veinte exports con fuentes sintéticas.
- **Git y privacidad:** sin cambios locales previos; sin listas privadas, credenciales, descargas de mods ni APIs de pago. Los artefactos versionados no incluyen rutas de usuario ni trazas. Revisar diff, staged e identidad antes del commit y push.

El alcance de #1 queda respaldado para revisión: diez pares analizados, dos métricas medidas, dos reproducciones directas, formatos/licencias y veredicto. Quedan **sin comprobar** demanda real, aceptación upstream, GUI/API MO2 real, comparación entre juegos, integridad/descargabilidad de mods, rendimiento en listas grandes y distribución de una CLI propia. Ninguno se presenta como PASS ni se convierte en compromiso de roadmap.

## Próximo paso condicionado

Con CONTRIBUIR, el siguiente trabajo recomendado es revisar esta decisión y autorizar una propuesta acotada para Meteoric; no ejecutar el issue #2 como si se hubiera aprobado CONTINUAR. No se abre ninguna comunicación externa desde este spike.

Prompt sugerido:

> Trabaja exclusivamente en la decisión del issue #1 de v1kz25/modlock. Revisa su PR y docs/research/issue-1/REPORT.md. Si apruebo CONTRIBUIR, prepara para mi revisión una propuesta de mejora a Meteoric sobre colisiones de nombre, incertidumbre y referencias a archivo, usando los casos 07/09 y sus métricas. No contactes al mantenedor ni publiques nada sin mi instrucción explícita; no empieces #2/#3 ni el MVP. Si decido CONTINUAR pese al informe, documenta primero qué evidencia nueva justifica el cambio y solicita el alcance autorizado para #2.
