# Señales de reproducibilidad — #11

En desarrollo 0.2.0.dev0, no incluido en la prerelease 0.1.0a1. El propietario
autorizó continuar con #11 y después los issues posibles por dependencias,
fusiones/versiones tras controles y aviso ante prueba manual necesaria. Eso no
convierte CONTRIBUIR en un resultado favorable ni demuestra demanda.

`compare BASE HEAD --audit` añade únicamente la clave `audit` al informe previo.
Sin flag, el JSON anterior no cambia. `audit.schema` identifica la extensión
`modlock-audit-0.2-experimental`; `schema` superior sigue siendo
`modlock-0.1-experimental`. Consumidores estrictos pueden omitir el flag.
Markdown conserva toda la extensión dentro de Complete evidence; el formato de
revisión humana se tratará por separado en #14.

API interna `audit_export(NormalizedExport)`, sin I/O ni nuevas correspondencias.
Comparación y auditoría comparten `checked_export` para rechazar mutaciones que
hagan divergir raw y modelo tipado. Cada lado se evalúa independientemente, con
un registro por mod (también desactivados), por índice original. Separadores no
son mods ni hallazgos. Resumen: mods y número de señales unknown por nombre;
no es una puntuación de seguridad o completitud del juego.

| Señal | present | unknown |
|---|---|---|
| page_identifier | ID numérico positivo sin contradicción de página | ID textual local o contradicción |
| version | Texto declarado no vacío tras comprobar whitespace | Clave ausente (`missing_version`) o vacía/whitespace (`empty_version`) |
| file_references | Evidencia `referenced` del modelo: referencias completas, coherentes y localmente únicas | Referencias parciales, conteos inconsistentes, duplicados o ambigüedad |
| order | Posición validada en el export | No se interpreta orden de carga de plugins |
| content_hash | Nunca en este formato soportado | No hay evidencia de contenido verificada |
| provenance | Nunca | Productor/origen no autenticado |
| game | Nunca | Ni `--context` autentica el juego |

Cada señal tiene `state`, `reason` y `location`: ruta JSON esperada cuando existe
un campo conocido; puede señalar un campo ausente. `null` significa que no hay
campo soportado. No duplica nombres/rutas de origen. Los datos raw del informe
pueden contener información privada: no compartir sin revisarla.

Unknown significa evidencia insuficiente, no ausencia en disco, malware o
incompatibilidad. `present` es metadata declarada, no validación remota ni prueba
de reproducibilidad. Un campo desconocido llamado hash/game/provenance permanece
en raw pero no se asciende a señal fiable. No se abren referencias de los datos,
no se calculan hashes de mods ni se descargan archivos. El contexto y las reglas
del motor permanecen iguales; no se inventan correspondencias.

Smoke sintético desde el entorno local documentado:

```powershell
& .\.venv\Scripts\modlock.exe compare examples/base.json examples/head.json --context synthetic:release --audit --output NUEVO-audit.json
$report = Get-Content -Raw NUEVO-audit.json | ConvertFrom-Json
if ($report.summary.modified -ne 1 -or $report.audit.base.summary.mods -ne 1) { throw 'Resultado inesperado' }
```

Salida 0 incluso con unknown; salida 1 si existe el destino; 2 si uso inválido.
No hay prueba manual obligatoria del propietario: smoke real y tests se ejecutan
con datos sintéticos en Windows. Límites de corpus/ACL reales siguen explícitos.
