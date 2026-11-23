# Matriz de formato y seguridad read-only — #17

Se admite la estructura documental Meteoric JSON 1.0 estudiada en el commit
`1e34b9918a81239b71789a5472f6bc16ffdab70b` del productor; no se autentica quién
produjo una entrada ni se certifican otras revisiones por semejanza. Corpus
propio, sintético y redistribuible, generado/contrastado con ese productor en #2,
con hashes y discrepancias reproducibles: docs/research/issue-2/VALIDATION.md,
manifest.json y sources.json. No se requieren perfiles privados ni una GUI MO2.

| Matriz | Evidencia y resultado requerido |
|---|---|
| Seis entradas válidas | Lector, modelo, diff, audit, JSON y Markdown conservan todos los registros |
| Dos anomalías emitidas por productor | Aceptadas con warnings; conteos parciales/negativos no inventan referencias |
| Once negativas | UTF-8/JSON/estructura/tipo no soportados: error controlado, no reparación |
| Export genérico object, texto de modlist y bytes ZIP | No soportados: error 1, no informe parcial |
| JSON de herramientas no documentadas | Sin soporte declarado; coincidencia de forma no certifica origen |
| Unicode, BOM, espacios y rutas con corchetes | Tests de snapshots/reader/CLI, sin reescribir bytes |
| Tamaño | Cada entrada acotada a 16 MiB; prueba real de límite+1 en #13, no benchmark |
| Directorio como entrada | Rechazado file_type |
| Referencias a archivos dentro de metadata | No abiertas, también con --audit; trazado de Path.open |
| Archivos hardlink | Lectura conservada; salida existente rechazada, contenido intacto |
| Atributo read-only de archivo | Lectura correcta; no se cambia configuración de Windows o ACL global |
| Symlink de entrada existente | Se sigue solo la ruta explícita a archivo regular; target intacto |
| Symlink de entrada roto | Error 1, no crear target |
| Symlink de salida existente o roto | Error 1, no modificar/crear target |

## Plataformas y límites de la evidencia

Local: Windows 11 x64 10.0.26300 / CPython 3.12.14. La creación de symlinks de
archivo devuelve Windows 1314 (privilegio no disponible); no se cambia Developer
Mode, políticas, permisos o configuración de Windows para forzarlo. Esos cuatro
casos se registran como SKIP local, **no PASS de Windows 11**. Hardlinks, atributo
read-only y demás casos sí se ejecutan en ese entorno.

CI estándar windows-latest (Windows Server, no Windows 11) debe ejecutar los
symlinks reales: si no puede crearlos los tests fallan, nunca saltan. Resultado
del SHA real constará en la PR antes de cerrar #17. No se declara soporte
comprobado de symlinks en Windows 11 con estos skips; usar archivos regulares
para el perfil local verificado. No hay prueba manual obligatoria del propietario
si CI cubre los enlaces y se mantiene esta limitación explícita.

Un atributo read-only no es una matriz de ACL; permisos denegados también se
simulan en tests anteriores. No se certifican todas las ACL, reparse points,
junctions, enlaces concurrentes o formatos de futuros productores. El lector
comprueba stat y fstat de archivo regular y limita bytes, pero no ofrece un
sandbox de filesystem o protección completa contra TOCTOU. La salida exclusiva
no transforma la comparación en una operación de escritura sobre instalaciones.

No se instala ni descarga contenido de mods. Los tests y corpus no prueban
integridad de instalación, juego, plugins, FOMOD, orden de carga ni compatibilidad.
Los informes preservan raw y pueden contener metadata privada proporcionada por
el usuario: mantenerlos locales. Es seguridad operacional acotada, no auditoría
de seguridad exhaustiva ni validación de demanda. CONTRIBUIR permanece histórico.


## Fallo real y corrección #17

CI 45236084982 sobre d6f5400381274c131657208223b7c1ee6488b6e0 ejecutó todos los
symlinks: 204 tests pasaron y falló el destino de symlink roto. En Windows,
open(x) siguió ese enlace ya existente y creó su target: el CLI devolvió 0.
No era un fallo de la expectativa; contradice la política de salida nueva.
La corrección consulta lstat (entrada sin seguir enlace) y rechaza cualquier
entrada final existente antes de open(x). Se mantiene creación exclusiva para
colisiones ordinarias; no se promete aislamiento de sustituciones concurrentes
entre comprobación y apertura. Los cuatro casos reales deben pasar en nuevo CI.

Afecta a 0.1.0a1 y 0.2.0a1 en Windows con salida symlink rota; hasta instalar la
corrección, usar únicamente destinos nuevos que no sean enlaces. El fallo crea
el target ausente; no se ha observado modificación de las entradas. No se cambia
la semántica del parser/audit ni se necesita un nuevo formato o dependencia.
