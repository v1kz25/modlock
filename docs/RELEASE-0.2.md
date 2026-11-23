# Segunda prerelease experimental 0.2.0a1 — #15

## Alcance y decisión

Un único formato [Meteoric JSON](formats/meteoric-json-v1.md), comparación
conservadora e informes JSON/Markdown. Windows 11 x64 / CPython 3.12.14 probado;
se requiere CPython >=3.12,<3.13, sin promesa para otras plataformas. El nombre
`py3-none-any` de la wheel describe su contenido Python, no una matriz probada.
No es un ejecutable autónomo: necesita Python y dependencias.

CONTRIBUIR sigue siendo el veredicto del spike #1. El propietario autorizó
expresamente completar v0.1, fusionar y publicar este experimento; eligió MIT
para #10. Eso no demuestra demanda, diferenciación ni valida todo el backlog.
Se añaden señales opcionales de auditoría y comparación de snapshots guardados. No hay auditoría de contenido instalado, hashes o inferencia de
actualizaciones por nombres/IDs cambiados. Ver [límites de CLI](CLI.md).

## Descargar y comprobar

Desde la prerelease de GitHub, guardar en una carpeta local nueva:

- `modlock-0.2.0a1-py3-none-any.whl`: paquete propio y licencias, sin dependencias.
- `modlock-0.2.0a1.tar.gz`: fuente, docs, pruebas y fixtures sintéticos.
- `requirements-runtime.txt`: 13 wheels de runtime fijadas por versión/SHA-256,
  específicamente comprobadas en Windows x64 / CPython 3.12.
- `THIRD_PARTY_NOTICES.md`, `base.json`, `head.json`, `SHA256SUMS`.

`SHA256SUMS` contiene hashes de los seis primeros archivos, no de sí mismo.
Comprobar **todos** antes de instalar, desde esa carpeta en PowerShell:

```powershell
foreach ($line in Get-Content .\SHA256SUMS) {
    $expected, $name = $line -split '  ', 2
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $name).Hash.ToLowerInvariant() -ne $expected) {
        throw "Checksum incorrecto: $name"
    }
}
```

Los hashes detectan alteración accidental; no son una firma independiente.
Los archivos automáticos Source code de GitHub no son el sdist construido.

## Instalación local y smoke PowerShell

Definir `$python` como ruta a un CPython 3.12 x64 existente. No cambiar Windows,
PATH, políticas ni instalar globalmente. No hace falta activar el entorno.

```powershell
& $python --version
& $python -m venv .venv
& .\.venv\Scripts\python.exe -m pip --isolated download --only-binary=:all: --require-hashes -r requirements-runtime.txt --dest .venv/wheels
& .\.venv\Scripts\python.exe -m pip --isolated install --no-index --find-links .venv/wheels --only-binary=:all: --require-hashes -r requirements-runtime.txt
& .\.venv\Scripts\python.exe -m pip --isolated install --no-deps .\modlock-0.2.0a1-py3-none-any.whl
& .\.venv\Scripts\python.exe -m pip check
& .\.venv\Scripts\modlock.exe --version
& .\.venv\Scripts\modlock.exe --help
& .\.venv\Scripts\modlock.exe compare base.json head.json --context synthetic:release --audit --output report.json
$report = Get-Content -Raw report.json | ConvertFrom-Json
if ($report.summary.modified -ne 1 -or $report.summary.separator -ne 2) { throw 'Smoke inesperado' }
& .\.venv\Scripts\modlock.exe compare base.json head.json --context synthetic:release --audit --format markdown --output report.md
```

Comprobar `$LASTEXITCODE` después de cada ejecutable: debe ser 0; detenerse si
falla. La primera descarga requiere PyPI; después instalación y comparación
funcionan offline. No se incluyen credenciales, servicios ni descargas de mods.
El contexto del ejemplo es sintético; con datos propios solo declararlo si
se conoce mismo juego Y linaje de exportación. No es una verificación del juego.
El cambio del ejemplo es metadata de versión y active; no prueba un cambio
de contenido instalado. Los dos separadores son uno por lado, conservados.

Repetir una salida existente debe devolver 1 y conservarla; opción desconocida
devuelve 2. Diferencias/ambigüedad no son fallos: salida 0. Los informes incluyen
metadata original: revisar privacidad antes de compartirlos.

## Reconstruir y probar el sdist

Extraer el sdist en una carpeta nueva (o usar el commit/tag indicado en la
release), entrar en su raíz y preparar el entorno según DEVELOPMENT.md con
`requirements-dev.txt`. No se incorpora una herramienta de publicación.
El backend flit_core ya está fijado y revisado. Build sin red ni dependencias
nuevas; timestamps normalizados al 01-01-1980 UTC para repetibilidad:

```powershell
$env:SOURCE_DATE_EPOCH = '315532800'
New-Item -ItemType Directory -Path dist -Force | Out-Null
& .\.venv\Scripts\python.exe -c "from flit_core import buildapi; print(buildapi.build_sdist('dist')); print(buildapi.build_wheel('dist'))"
Get-FileHash -Algorithm SHA256 .\dist\*
```

Comparar los hashes con los publicados usando exactamente los archivos fuente,
backend y entorno documentados. El sdist incluye tests/docs necesarios para
el corpus; la wheel solo código propio/metadata/licencias. No incluye `.git`,
`.venv`, credenciales ni datos privados. No se promete reproducibilidad entre
checkouts con distintas conversiones CRLF/LF: usar el sdist publicado.

Para probar la distribución fuente con herramientas ya instaladas y sin
resolver builds ocultos:

```powershell
& .\.venv\Scripts\python.exe -m pip --isolated install --no-build-isolation --no-deps RUTA\modlock-0.2.0a1.tar.gz
& .\.venv\Scripts\python.exe -m pip check
& .\.venv\Scripts\python.exe -m pytest -q
& .\.venv\Scripts\python.exe -m ruff check src tests
& .\.venv\Scripts\python.exe -m ruff format --check src tests
& .\.venv\Scripts\python.exe -m mypy src/modlock
```

Usar un entorno nuevo para cada instalación de wheel/sdist y verificar que
`modlock.__file__` apunta a site-packages, sin editable ni PYTHONPATH. Los
resultados reales y hashes finales se registran en la PR/release; no se infiere
éxito de estas instrucciones. Las comparaciones automáticas usan solo fixtures
sintéticos; no hay prueba manual obligatoria del propietario para este alcance.

## Publicación y Gitflow

PR #15 hacia develop, controles reales y fusión autorizada. Crear rama
`release/0.2.0a1` desde develop actualizado y PR de estabilización hacia main.
La prerelease se etiqueta en el SHA revisado de release, sin fusionar el
experimento en main (reservada a versiones estables). Esa PR queda como draft
para una futura decisión de estabilización, sin auto-merge ni borrar ramas.
No hay cambios exclusivos de release que sincronizar a develop.

Publicación manual autorizada en GitHub Releases con indicador prerelease y
artefactos/checksums ya verificados; no PyPI, ejecutable congelado ni workflow
de publicación. CI usa runner estándar gratuito en repo público. Coste adicional
obligatorio 0 €. No presentar v0.2 como estable: #16 exige feedback y #19 revisión humana antes del tag estable.

Migración desde v0.1: [MIGRATION-0.2.md](MIGRATION-0.2.md). Cambia presentación Markdown, audit es opt-in; JSON predeterminado conserva su schema. El typecheck usa las 24 distribuciones del lock de desarrollo, no el lock runtime de 13.
