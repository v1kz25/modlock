# Desarrollo — modlock

## Estado

#4 integrado; #8 incorpora CLI compare e informes JSON/Markdown. [Comandos y códigos actuales](CLI.md). Las secciones del setup registran sus verificaciones históricas; la suite actual se verifica en cada PR. La autorización vigente cubre #4/#8/#9/#10 y publicación experimental, sin habilitar v0.2.

Estado actual: #3/#6/#7/#4/#8/#9 integrados. Lector, identidad, motor conservador, CLI e informes disponibles; #10 prepara distribución 0.1.0a1 con MIT autorizada. La evidencia histórica de #3 se mantiene abajo identificada como tal. CONTRIBUIR permanece como veredicto del spike. [Instalación del artefacto y reproducción](RELEASE.md).

## Entorno comprobado y elección de versiones

- Windows 11 x64 (ensayado en 10.0.26300.0); Git y GitHub CLI (`gh`).
- Perfil experimental admitido: **CPython >=3.12,<3.13**. Se limita a una familia comprobada, sin prometer compatibilidad con otras familias/plataformas. Python 3.12 sigue en soporte de seguridad hasta octubre de 2028 según la [guía oficial](https://devguide.python.org/versions/); la [documentación de Windows](https://docs.python.org/3.12/using/windows.html) incluye plataformas posteriores a Windows 8.1.
- La selección se contrastó con requisitos de dependencias y wheels Windows, instalación aislada y tests; no se dedujo simplemente del spike. El intérprete disponible usado fue **3.12.14**, que no se impone como parche mínimo ni se presenta como el más reciente. Usar un parche de seguridad mantenido de la familia; no se han probado todos los parches. Ampliar el rango requiere otra verificación.
- Typer 0.29.2 (runtime), pytest 9.2.0 (pruebas), Ruff 0.17.6 (lint/formato) y flit_core 4.2.0 (backend de instalación sin dependencias externas). Son versiones estables consultadas en PyPI y comprobadas en este entorno; no una selección anticipada para una release.
- [requirements-dev.txt](../requirements-dev.txt) fija también las dependencias transitivas y hashes de las wheels ensayadas para CPython 3.12/Windows x64. No es un lock multiplataforma. [DEPENDENCIES.md](DEPENDENCIES.md) registra necesidad, licencias y componentes incluidos.
- Sin hosting, cuentas de servicios comerciales, API keys ni infraestructura de pago.

## Instalación local en PowerShell

Desde la raíz del repositorio, definir `$python` como ruta absoluta de un **python.exe CPython 3.12 existente** y comprobar `& $python --version`. En la verificación se usó el ejecutable ya incluido en el runtime de Codex. No usar un alias que instale Python automáticamente ni cambiar PATH, políticas de ejecución o configuración de Windows.

```powershell
& $python -m venv .venv
& .\.venv\Scripts\python.exe -m pip --isolated download --only-binary=:all: --require-hashes -r requirements-dev.txt --dest .venv/wheels
& .\.venv\Scripts\python.exe -m pip --isolated install --no-index --find-links .venv/wheels --only-binary=:all: --require-hashes -r requirements-dev.txt
& .\.venv\Scripts\python.exe -m pip --isolated install --no-build-isolation --no-deps -e .
& .\.venv\Scripts\python.exe -m pip check
```

Comprobar `$LASTEXITCODE` después de cada comando y detenerse si no es 0. La descarga inicial usa PyPI; la instalación desde wheels, la CLI y las pruebas son locales. No se necesita activar el entorno. `.venv/` ya está ignorado por Git. La instalación editable usa el backend fijado del entorno, sin resolver dependencias ocultas en un entorno de build adicional. No se ha instalado nada globalmente ni se distribuyen intérpretes/binaries en el repositorio.

Se repitió la instalación desde cero en `.venv/clean`, entorno independiente creado para comprobación dentro de la carpeta ignorada: mismo requirements con hashes, instalación editable, `pip check`, pytest y Ruff correctos. Las wheels `pydantic_core` y Ruff para Windows x64 evitaron necesitar compiladores o cambios de Windows. No se probó instalación desde sdist ni generación de un ejecutable distribuible.

## Flujo de trabajo

1. Leer AGENTS.md, roadmap y el issue activo.
2. Crear `feature/<issue>-<nombre>` desde `develop` para una única tarea (Gitflow).
3. Implementar sólo su alcance y tests; revisar dependencias/licencias.
4. Ejecutar y registrar pruebas; comprobar Git diff y la identidad Git.
5. Proponer Pull Request; no fusionarla sin permiso.
6. Actualizar el README únicamente para funciones realmente disponibles.

## Tests, lint y smoke

```powershell
& .\.venv\Scripts\python.exe -m pytest -q
& .\.venv\Scripts\python.exe -m ruff check src tests
& .\.venv\Scripts\python.exe -m ruff format --check src tests
& .\.venv\Scripts\modlock.exe --help
& .\.venv\Scripts\modlock.exe --version
& .\.venv\Scripts\python.exe -m modlock --version
& .\.venv\Scripts\modlock.exe --unknown-option
# Este último debe terminar con $LASTEXITCODE = 2.
```

Estado histórico del setup #3 (la CLI actual añade compare): Sin argumentos muestra ayuda y sale con 0; `--help` y `--version` salen con 0; opciones/argumentos inválidos salen con 2 y diagnóstico sin traceback. Versión de desarrollo: `0.0.0.dev0`, única fuente en `src/modlock/__init__.py` y metadata calculada por flit. No se añaden comandos simulados de comparación.

Resultados ejecutados el **22-11-2026**:

| Verificación | Resultado |
|---|---|
| Instalación aislada con hashes e instalación editable | OK en `.venv` y en entorno vacío `.venv/clean` |
| pytest: ayuda explícita/sin argumentos, versión/metadata, cuatro usos inválidos y entrada `python -m` fuera del repositorio | 8 tests OK en ambos entornos |
| Ruff `check src tests` | OK en ambos entornos |
| Ruff `format --check src tests` | 4 archivos ya formateados |
| `pip check` | Sin requisitos rotos en ambos entornos |
| Smoke de `modlock.exe` fuera del repositorio | Ayuda/sin argumentos/versión: 0; opción desconocida y compare: 2 |
| Licencias y versiones instaladas | 19 distribuciones fijadas contrastadas; bootstrap documentado por separado |

La primera ejecución de tests detectó una aserción frágil por el salto de línea de la ayuda en terminal estrecha; se corrigió normalizando espacios en esa aserción y la suite final pasó completa. No se alteró la CLI para acomodar una salida falsa. El lint se limita al paquete y sus tests; no convierte scripts históricos de investigación en código del producto. No se configura CI ni publicación.

La tabla anterior registra el setup #3. La validación del lector #6 se describe en el [contrato del lector](formats/meteoric-json-v1.md#lector-interno-del-issue-6); reglas, golden y comandos del modelo #7 en [IDENTITY.md](IDENTITY.md). La normalización no hace I/O: recibe un resultado del lector y conserva copias separadas de sus datos. No hay prueba manual obligatoria de usuario: el agente ejecuta comandos y smoke sintéticos. La GUI MO2 y auditorías siguen fuera del alcance.

## Después de v0.1, sin autorización automática

Terminar #10 y publicar la prerelease autorizada agota este alcance. No iniciar v0.2. La siguiente dependencia propuesta es #11, condicionada a revisar necesidad, feedback y autorización del propietario.

## Gitflow

- `main`: versiones estables; rama predeterminada. No trabajar directamente en ella después de la preparación inicial.
- `develop`: integración de la próxima versión; punto de partida de tareas y spikes.
- `feature/<issue>-<nombre>`: una tarea pequeña o spike del issue activo, creada desde `develop`; PR hacia `develop`. No avanzar al siguiente issue.
- `release/<version>`: estabilización de una versión desde `develop`; solo correcciones, pruebas y documentación. PR hacia `main` y sincronización posterior hacia `develop` mediante otra PR.
- `hotfix/<issue>-<nombre>`: corrección urgente de una versión publicada, desde `main`; PR hacia `main` y otra hacia `develop` para propagar la corrección.
- Preparación de ramas y PRs autorizada dentro del issue activo. Toda fusión requiere aprobación explícita del usuario. No habilitar auto-merge.
- No hacer force push, rebase de ramas compartidas, ni eliminar ramas. Si la interfaz ofrece eliminar la rama tras fusionar, desactivar esa opción.
- Usar Git y GitHub CLI estándar; no se necesita instalar una extensión Gitflow ni añadir servicios o pipelines.
- Antes de una PR: revisar diff, pruebas relevantes, identidad Git y ausencia de secretos. Registrar resultados y bloqueos reales.
