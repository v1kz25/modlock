# Motor experimental #4

El propietario autoriza completar #4/#8/#9/#10 y publicar una prerelease experimental; la decisión histórica CONTRIBUIR y la falta de evidencia de demanda se conservan. No se autoriza v0.2 ni estabilidad.

`compare_exports(base, head, context=None)` consume dos modelos del #7 en memoria. No hace I/O ni informes. Copia las entradas, comprueba posiciones y evidencia de identidad recalculada y conserva cada registro exactamente una vez por lado en el resultado (también separadores, categoría `separator`). No es un validador de modelos construidos arbitrariamente: usar resultados intactos de `normalize_export`.

**Contexto:** sin contexto explícito todos los mods quedan ambiguos, incluso con referencias iguales. Un string no vacío declara responsabilidad del llamador de que ambos exports comparten juego y linaje; no se deduce de nombres/rutas ni se verifica externamente. No sustituye hashes de contenido o integridad de instalación.

Solo se emparejan conjuntos completos, únicos e idénticos de referencias página/archivo y estado `referenced` en ambos lados. Un ID de archivo cambiado no se convierte en actualización por coincidir página/nombre. Solapamientos o páginas sin correspondencia exacta quedan ambiguos. Un registro incierto en el otro export impide afirmar adición/eliminación de un registro no emparejado. No hay fuzzy, heurística por nombre o asignación voraz.

Adiciones/eliminaciones describen referencias declaradas ausentes dentro del contexto afirmado, no descarga o desaparición de contenido real. En pares establecidos se distinguen nombre, sección, activación, plugins/tags, metadatos y strings de versión. Versión vacía/ausente frente a conocida es `version_metadata`, sin afirmar actualización real. No se ordenan versiones ni se infiere compatibilidad. Un cambio entre dos versiones explícitas se conserva literalmente.

`reordered` usa posición relativa entre pares establecidos, no desplazamientos absolutos por inserciones/separadores. Un mod puede tener flags de orden y de modificación a la vez (categoría `modified`). Las entradas siguen orden base, luego registros head no emparejados; motivos/campos estables. Los separadores se conservan por lado sin emparejarlos por nombre. No se pierden duplicados ni se fusionan mods.

Pruebas sintéticas: contexto ausente, cambio de nombre/versión/metadatos/activación, referencia cambiada, inversiones, añadidos/eliminados, orden relativo, incertidumbre, conteos, determinismo e input inválido. Comandos: `python -m pytest -q`, `python -m ruff check src tests`, `python -m ruff format --check src tests` dentro del entorno local. No requiere prueba manual de usuario ni listas privadas. No se añade dependencia ni se cambia licencia propia en #4.
