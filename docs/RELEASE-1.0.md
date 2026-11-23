# Distribución 1.0.0 — candidato del issue #19

Contrato estable de CLI/informes para **un único formato Meteoric documentado**.
Estabilidad no significa integridad instalada, compatibilidad de mods o demanda
demostrada. CONTRIBUIR sigue histórico y la decisión del propietario de continuar
es independiente. [Contrato](PUBLIC-CONTRACT.md), [matriz](COMPATIBILITY.md),
[mantenimiento/licencias](SUPPORT.md) y DEPENDENCIES.md delimitan el perfil.

## Estado de preparación y revisión

Los paquetes 1.0.0 se construyen y prueban en `dist/v1.0.0` antes de crear tag
o release. La PR release/1.0.0 → main registra commit, hashes reales y controles.
**#19 exige revisión humana del candidato antes de tag**. La autorización general
permite integrar/publicar tras controles, pero no sustituye esa revisión. No
marcarla hecha por el feedback de un ejemplo anterior ni por CI. Los pasos
posteriores de esta guía son el procedimiento, no resultados ejecutados por
existir este documento; la PR registra cada resultado real.

## Perfil y assets

CPython >=3.12,<3.13 / Windows x64. Local Windows 11 10.0.26300, CPython 3.12.14;
CI Windows Server, CPython 3.12.10. No se prueban otras familias/plataformas.
Py3-none-any indica contenido Python, no cobertura multiplataforma ni .exe
autónomo. Symlinks reales se exigen en CI; cuatro pruebas locales se omiten
por privilegio Windows 1314, sin cambiar Developer Mode/ACL/configuración.
No se declara probado ese caso en Windows 11; perfil local con archivos regulares.

Después de publicación, descargar estos siete assets de GitHub Releases:

- modlock-1.0.0-py3-none-any.whl: solo paquete propio, metadata y licencias.
- modlock-1.0.0.tar.gz: fuentes, docs, tests y corpus sintético.
- requirements-runtime.txt: 13 wheels de runtime fijadas por versión/hash.
- THIRD_PARTY_NOTICES.md, base.json, head.json y SHA256SUMS.

SHA256SUMS contiene hashes reales de los otros seis archivos; no es firma
independiente. Source code automático de GitHub no equivale al sdist construido.
No se empaqueta Python, pip, dependencias, código GPL o datos privados.

## Verificar e instalar en PowerShell

Desde carpeta local nueva con los assets; definir `$python` como ruta a CPython
3.12 x64 existente. No cambiar PATH/políticas/Windows ni instalar globalmente.

```powershell
foreach ($line in Get-Content .\SHA256SUMS) {
    $expected, $name = $line -split '  ', 2
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $name).Hash.ToLowerInvariant() -ne $expected) {
        throw "Checksum incorrecto: $name"
    }
}
& $python --version
& $python -m venv .venv
& .\.venv\Scripts\python.exe -m pip --isolated download --only-binary=:all: --require-hashes -r requirements-runtime.txt --dest .venv/wheels
& .\.venv\Scripts\python.exe -m pip --isolated install --no-index --find-links .venv/wheels --only-binary=:all: --require-hashes -r requirements-runtime.txt
& .\.venv\Scripts\python.exe -m pip --isolated install --no-deps .\modlock-1.0.0-py3-none-any.whl
& .\.venv\Scripts\python.exe -m pip check
& .\.venv\Scripts\modlock.exe --version
& .\.venv\Scripts\modlock.exe --help
& .\.venv\Scripts\modlock.exe compare base.json head.json --context synthetic:release --audit --output report.json
$report = Get-Content -Raw report.json | ConvertFrom-Json
if ($report.summary.modified -ne 1 -or $report.summary.separator -ne 2 -or $report.audit.base.summary.mods -ne 1) { throw 'Smoke inesperado' }
& .\.venv\Scripts\modlock.exe compare base.json head.json --context synthetic:release --audit --format markdown --output report.md
```

Comprobar `$LASTEXITCODE` tras cada ejecutable: 0, salvo errores deliberados;
detenerse ante fallo. Salida existente debe dar 1 y conservarla; opción inválida
2; diferencias/unknown 0. Primera descarga usa PyPI; instalación desde wheels,
comparación y auditoría funcionan offline. No se necesita activar el entorno.

Contexto del ejemplo es sintético. Solo declarar contexto propio si se conoce
mismo juego Y linaje; no autentica nada. Version/active son metadata del ejemplo,
no contenido instalado. Content_hash/game/provenance siguen unknown. Informes
incluyen raw, que puede contener datos privados: revisar antes de compartir.

## Reproducir fuente y paquetes

Extraer sdist en carpeta nueva, entrar en su raíz y seguir DEVELOPMENT.md con
requirements-dev.txt (24 distribuciones, hashes). El backend ya fijado flit_core
4.2.0 evita nueva herramienta de publicación. Sin red durante build:

```powershell
$env:SOURCE_DATE_EPOCH = '315532800'
New-Item -ItemType Directory -Path dist -Force | Out-Null
& .\.venv\Scripts\python.exe -c "from flit_core import buildapi; print(buildapi.build_sdist('dist')); print(buildapi.build_wheel('dist'))"
Get-FileHash -Algorithm SHA256 .\dist\*
& .\.venv\Scripts\python.exe -m pytest -q -rs
& .\.venv\Scripts\python.exe -m ruff check src tests
& .\.venv\Scripts\python.exe -m ruff format --check src tests
& .\.venv\Scripts\python.exe -m mypy src/modlock
```

Timestamps normalizados a 01-01-1980 UTC. Comparar builds desde los mismos bytes
del sdist/backend/entorno; no prometer mismo hash con checkouts CRLF/LF distintos.
Probar wheel y sdist en venv nuevos, sin editable, `--no-deps` y para fuente
`--no-build-isolation` con backend ya instalado; pip check e import desde
site-packages fuera del repositorio. Los tests reconstruyen/inspeccionan wheel
y cierre runtime; CI repite suite después de instalar wheel no editable.

## Compatibilidad y promoción

JSON conserva IDs opacos heredados y su payload previo; no se añade otro modo.
Markdown simplifica dos encabezados, mantiene secciones/evidencia y snapshot
revisado. Consumidores deben usar JSON, no anchos/tablas/texto de ayuda como API.
APIs internas no forman parte del contrato público. Sin parser de segundo formato.

Tras revisión humana registrada y CI correcto del SHA final: fusionar la PR
release hacia main, comprobar árbol idéntico al revisado, crear tag v1.0.0 en
ese commit y publicar los bytes probados con SHA256SUMS. Descargar los siete
assets y compararlos byte a byte. Después PR main → develop con controles para
propagar estabilización. Nunca force push, borrar ramas, auto-merge o sustituir
assets de tags históricos. No sincronizar ni declarar publicado antes de hacerlo.

Coste adicional obligatorio 0 €: repo público, runner estándar gratuito,
publicación manual GitHub, sin PyPI, credenciales nuevas, tarjeta o servicios.
No hay prueba PowerShell pendiente del propietario: el agente ejecuta comandos;
la única puerta humana de #19 es revisar el candidato concreto.
