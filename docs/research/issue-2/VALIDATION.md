# Validación del corpus del issue #2

Fecha: **22-11-2026**. Contrato estudiado: [meteoric-json-v1.md](../../formats/meteoric-json-v1.md).

## Matriz de resultados esperados

Todos los ejemplos son sintéticos. Las carpetas `valid` y `anomalous` se obtienen del **exportador real** a partir de `sources.json`; no se escribe una implementación alternativa del exportador. `manifest.json` registra los SHA-256 de los 19 archivos. La especificación original y las muestras upstream se leen desde el checkout externo fijado.

| Archivo bajo fixtures/ | Condición y resultado esperado |
|---|---|
| valid/01-empty.json | Array vacío, sin error; no equivale a archivo vacío |
| valid/02-unsectioned-unicode.json | Unicode conservado, tags finales, plugins de raíz ordenados, Unsectioned y metadatos ausentes |
| valid/03-metadata.json | Separador con tag, mod desactivado, versión no semver y dos referencias a archivos |
| valid/04-empty-sections.json | General presente con cinco strings vacíos; installed presente con size 0 y files vacío |
| valid/05-name-collision.json | Dos nombres completos distintos con mismo modName/id textual; conservar ambos |
| valid/06-separator-only.json | Un separador, cero mods; nombre y contexto Unicode |
| anomalous/01-negative-size.json | El exportador emite size -1; advertir inconsistencia sin inventar archivos |
| anomalous/02-partial-installed.json | El exportador emite size 2 y un solo archivo tras un error de interpolación; preservar evidencia incompleta |
| invalid/01-root-object.json | JSON válido, raíz object; no es un export array |
| invalid/02-root-null.json | JSON válido, raíz null; no es lista vacía |
| invalid/03-missing-active.json | Falta un campo siempre emitido; no asumir true/false |
| invalid/04-active-string.json | active es string, no booleano |
| invalid/05-unknown-type.json | Discriminador no estudiado; variante no soportada por este contrato |
| invalid/06-general-array.json | general es array en lugar de objeto |
| invalid/07-order-fraction.json | order fraccional, inalcanzable en el productor fijado |
| invalid/08-orphan-section.json | Sección sin separador precedente ni contexto Unsectioned |
| invalid/09-order-gap.json | Un registro en posición cero declara order 3 |
| invalid/10-truncated.json | UTF-8 correcto, sintaxis JSON truncada |
| invalid/11-non-utf8.json | Byte FF impide decodificación UTF-8 estricta |

La condición negativa se comprueba contra el dato fijo y el contrato, **no contra un parser modlock**. No se atribuye a Meteoric rechazo de estos ejemplos. Los ocho roundtrips prueban el código del exportador con API simulada; no prueban integración con MO2 real. El error de meta.ini de la anomalía 02 es deliberado y local al montaje sintético.

## Comprobación reproducible con PowerShell

Ejecutar desde la raíz del repositorio. Usar un intérprete Python existente; no instalar paquetes ni cambiar Windows. Preparar un checkout nuevo temporal si no se dispone del SHA. La clonación necesita red; las comprobaciones posteriores son locales y no usan credenciales ni APIs.

```powershell
$meteor = Join-Path $env:TEMP 'meteoric-issue2-review'
# $python = ruta de un python.exe existente; no usar un alias de instalación automática.
git clone https://github.com/imightbemeteor/meteoric-modlist-tools.git $meteor
git -C $meteor checkout --detach 1e34b9918a81239b71789a5472f6bc16ffdab70b
$result = Join-Path $env:TEMP ('modlock-issue2-' + [guid]::NewGuid().ToString('N') + '.json')
$check = @'
import hashlib, importlib.util, json, platform, subprocess, sys, tempfile
from pathlib import Path
from types import SimpleNamespace

root, upstream, output = map(Path, sys.argv[1:])
manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
sha = subprocess.check_output(['git', '-C', str(upstream), 'rev-parse', 'HEAD'], text=True).strip()
assert sha == manifest['meteoric_commit'], 'Unexpected Meteoric commit'
assert not subprocess.check_output(['git', '-C', str(upstream), 'status', '--porcelain', '--untracked-files=no'], text=True).strip(), 'Modified upstream code'
assert not output.exists(), 'Choose a new output file'
spec = importlib.util.spec_from_file_location('experiment_exporter', upstream / 'mo2-plugins/modlist_compare/exporter_core.py')
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)
sys.modules['mobase'] = SimpleNamespace(ModState=SimpleNamespace(ACTIVE=1))
sources = json.loads((root / 'sources.json').read_text(encoding='utf-8'))
observed, records = {}, []
for entry in manifest['fixtures']:
    name = entry['path']
    raw = (root / 'fixtures' / name).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == entry['sha256'], name
    utf8, syntax = True, True
    try:
        data = json.loads(raw.decode('utf-8'))
    except UnicodeDecodeError:
        utf8, syntax = False, None
    except json.JSONDecodeError:
        syntax = False
    assert utf8 == (name != 'invalid/11-non-utf8.json'), name
    assert syntax == (None if not utf8 else name != 'invalid/10-truncated.json'), name
    roundtrip = None
    if syntax:
        observed[name] = data
    if name in sources:
        with tempfile.TemporaryDirectory() as temporary:
            mods, states = {}, {}
            for i, item in enumerate(sources[name]):
                directory = Path(temporary) / str(i)
                directory.mkdir()
                if item.get('meta') is not None:
                    (directory / 'meta.ini').write_text(item['meta'], encoding='utf-8')
                for plugin in item.get('plugins', []):
                    (directory / plugin).touch()
                mods[item['name']] = SimpleNamespace(
                    isSeparator=lambda item=item: item.get('separator', False),
                    absolutePath=lambda directory=directory: str(directory),
                    nexusId=lambda item=item: item.get('nexus', 0))
                states[item['name']] = int(item.get('active', True))
            api = SimpleNamespace(allModsByProfilePriority=lambda: list(mods), state=states.__getitem__)
            organizer = SimpleNamespace(modList=lambda: api, getMod=mods.get)
            assert exporter.export_modlist(organizer) == data, name
        roundtrip = True
    assert hashlib.sha256((root / 'fixtures' / name).read_bytes()).hexdigest() == digest, name
    records.append(dict(path=name, sha256=digest, utf8=utf8, json_syntax=syntax, exporter_roundtrip=roundtrip))

# Observations on these fixed negative fixtures; this is not a schema validator.
bad = lambda number: next(value for name, value in observed.items() if name.startswith('invalid/' + number + '-'))
checks = dict(
    root_object=isinstance(bad('01'), dict), root_null=bad('02') is None,
    missing_active='active' not in bad('03')[0], active_string=type(bad('04')[0]['active']) is str,
    unknown_type=bad('05')[0]['type'] not in ('mod', 'separator'),
    general_array=isinstance(bad('06')[0]['general'], list),
    order_fraction=type(bad('07')[0]['order']) is float,
    orphan_section=bad('08')[0]['separatorName'] == 'Absent',
    order_gap=bad('09')[0]['order'] != 0)
assert all(checks.values()), checks
assert len(records) == 19 and sum(r['exporter_roundtrip'] is True for r in records) == 8
assert observed['anomalous/01-negative-size.json'][0]['installed']['size'] == -1
partial = observed['anomalous/02-partial-installed.json'][0]['installed']
assert partial['size'] == 2 and len(partial['files']) == 1
files = ['README.md', 'LICENSE', 'mo2-plugins/modlist_compare/FORMAT_SPECIFICATION.md',
         'mo2-plugins/modlist_compare/exporter_core.py', 'mo2-plugins/modlist_compare/plugin_tools.py',
         'examples/lists/Example List 1.0.json', 'examples/lists/Example List 1.1.json']
result = dict(meteoric_commit=sha, python=platform.python_version(), fixtures=records,
              negative_observations=checks,
              upstream_file_sha256={p: hashlib.sha256((upstream / p).read_bytes()).hexdigest() for p in files})
output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('PASS: 19 fixture hashes intact; 8 real exporter roundtrips; 9 structural negative observations; expected UTF-8 and JSON failures')
'@
$check | & $python - docs/research/issue-2 $meteor $result
if ($LASTEXITCODE -ne 0) { throw 'Falló la comprobación de fixtures' }
Get-FileHash $result
Get-FileHash docs/research/issue-2/results.json
# Comparar hashes si se usa el mismo Python y los mismos bytes del checkout upstream.
```

El código del bloque monta exclusivamente este corpus, llama al exportador externo y comprueba datos conocidos. No es un lector reutilizable, ni contiene lógica de matching, ni valida entradas arbitrarias. Los placeholders temporales se eliminan al salir del montaje. `results.json` no incluye rutas locales. Los hashes de fuentes upstream corresponden a bytes de ese checkout; una conversión LF/CRLF puede cambiar esos hashes sin cambiar el contenido lógico. Los hashes de fixtures propios se mantienen con `.gitattributes`; el campo Python también puede variar con otro intérprete.

## Contraste con pruebas y muestras upstream

```powershell
& $python -m unittest discover -s "$meteor/mo2-plugins/modlist_compare" -p 'test_exporter_core.py' -v
& $python -m unittest discover -s "$meteor/tools" -p 'test_examples.py' -v
```

La primera suite comprueba helpers del exportador (tags, nombres, meta.ini y plugins) sin PyQt6. La segunda contrasta las dos muestras originales con orden, secciones y escenarios documentados. No se copian las muestras ni el código GPL al proyecto.

## Resultados ejecutados

Ejecutados en Windows 11 (10.0.26300.0), con Python **3.12.14** ya incluido en el runtime de Codex. Esta es la versión observada, no una elección de versión mínima del producto. Se extrajo y ejecutó el bloque Python de esta misma página sin una copia alternativa de su lógica; se usó el checkout externo intacto del SHA fijado.

| Comprobación | Resultado real |
|---|---|
| SHA y archivos versionados upstream intactos | PASS |
| 19 fixtures frente a sus SHA-256 y lectura sin modificación | PASS |
| 6 válidos y 2 anomalías frente al exportador real con API MO2 simulada | 8/8 iguales |
| Observaciones estructurales de negativos fijos | 9/9 coinciden con la matriz |
| UTF-8 inválido y JSON truncado | Fallos esperados del decodificador, comprobados |
| Pruebas upstream de exporter_core | 8 tests, OK |
| Pruebas upstream de las dos muestras oficiales | 14 tests, OK |
| Bytes de los 19 fixtures en el índice Git frente al manifiesto | PASS, incluidos los tres bytes del UTF-8 inválido |
| Enlaces locales de README, roadmap, formato y validación | Resuelven a archivos existentes |

Las observaciones y hashes están en [results.json](results.json). No se contabilizan las anomalías como conformes a todos los invariantes documentales. No hay prueba de rechazo por un lector modlock, que no existe. No se ha ejecutado lint/typecheck de producto ni creado suite de tests de modlock. Se revisaron diff, archivos staged, identidad Git y posibles secretos; `git diff --cached --check` no indicó errores. No se añaden servicios ni CI.

## Pruebas manuales del usuario y siguiente autorización

**Ninguna prueba manual de usuario es obligatoria para el alcance de #2.** Las comprobaciones anteriores las ejecuta el agente. No se requiere abrir MO2, proporcionar listas privadas ni instalar dependencias. La interfaz del plugin y la exportación con MO2 real siguen sin comprobarse; no se declaran PASS.

La PR del issue #2 queda para revisión y autorización de fusión. No comenzar #3 ni crear CLI/parser. Si se decide implementar después, transformar la matriz en pruebas del lector solo dentro de su issue autorizado, manteniendo las advertencias de las anomalías y los límites del veredicto CONTRIBUIR.
