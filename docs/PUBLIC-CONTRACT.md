# Contrato público 1.x — #16

Especificación para la línea 1.x; **no anuncia una release v1.0 publicada**.
El 23-11-2026 el propietario confirmó que había revisado el ejemplo v0.2 y se
entendían sus ambigüedades, advertencias y unknown. Ese feedback satisface la
dependencia de #16 y se limita a la presentación del ejemplo: no es prueba de
demanda, compatibilidad de mods ni ensayo de perfiles reales. 0.2.0a2 ya está
publicada con la corrección Windows. #19 exige revisar el candidato concreto
antes del tag estable; la autorización general no sustituye esa revisión.

## Superficie conservada

| Entrada | Resultado actual |
|---|---|
| Sin argumentos / --help | Ayuda, exit 0 |
| --version / python -m modlock --version | Versión de paquete, exit 0 |
| compare BASE HEAD | JSON stdout; contexto desconocido, sin inferencia |
| --context TEXTO | Afirmación mismo juego/linaje, nunca autenticación |
| --format json/markdown | JSON predeterminado, Markdown con evidencia completa |
| --output NUEVO / -o NUEVO | UTF-8, creación exclusiva; no sobreescribir |
| --audit | Clave audit opt-in, conserva matching y campos JSON anteriores |
| Diferencias/unknown/ambigüedad | Operación correcta, exit 0 |
| Lectura/formato/contexto/escritura fallidos | Diagnóstico stderr, exit 1 |
| Argumentos/opciones/formato inválidos | Diagnóstico stderr, exit 2 |

JSON superior: schema, context, summary, warnings, changes, limitations;
audit opcional. Se conservan como identificadores opacos heredados
`modlock-0.1-experimental` y `modlock-audit-0.2-experimental`: no se renombran
ni se introduce otro modo incompatible por publicar la versión 1.x. No son
detección del productor. La estabilidad se refiere a este contrato y sus tipos,
no a una garantía de contenido instalado. Registros conservan índices por lado, identidad y raw
decodificado; no bytes originales ni promesa de compatibilidad de instalación.

| Campo requerido | Tipo y significado |
|---|---|
| schema | String literal heredado indicado arriba |
| context | String declarado por llamador o null |
| summary | Objeto categoría → entero no negativo; categoría ausente cuenta 0 |
| warnings | Objeto base/head, cada uno array de code/location/message strings |
| changes | Array de category string, fields array de strings, reason string/null, base/head registro/null |
| limitations | Array de strings explicativos, no condiciones comprobadas |

Registro: index entero no negativo; data objeto JSON raw; identity contiene
state string (referenced/incomplete/ambiguous/not_applicable), references array
de objetos page_id/file_id enteros positivos, reasons array de strings y
conflicting_indices array de enteros no negativos. Las categorías actuales son
added/removed/modified/reordered/unchanged/ambiguous/separator; fields separa
version de version_metadata y metadata/orden. Added/removed son referencias
observadas, no prueba de contenido instalado. Cada entrada se conserva una vez
por lado; separadores se cuentan por lado, no como una correspondencia inventada.

audit opcional contiene schema literal heredado, limitations array de strings
y base/head. Cada lado contiene records (array de index y signals) y summary
(mods entero no negativo; unknown_signals objeto nombre → entero no negativo).
Una señal contiene state present/unknown, location string/null y reason string.
Records de auditoría son solo mods, también desactivados; no separadores.
Location puede apuntar a un campo ausente esperado y null indica falta de campo
soportado. Present no prueba contenido, unknown no prueba ausencia o malware.
Campos raw admiten JSON decodificado, incluyendo desconocidos; no coerción o
promesa de formato nuevo. No añadir campos de versión de productor inferidos.

Orden observado: cambios por índices base, después head no emparejados;
categorías/keys de JSON y recuentos ordenados al serializar. Sin timestamps
ni rutas de origen añadidas; raw puede contener datos privados. Celdas Markdown
escapadas y fence dinámico; consumir JSON para integración, no parsear tablas
o asumir anchos/saltos de la ayuda. El texto de diagnósticos puede mejorar;
usar códigos de salida/categorías, no mensajes como API estable. Desde a2, la salida
rechaza también el symlink final roto mediante lstat. No se promete aislamiento
frente a sustituciones concurrentes; ver COMPATIBILITY.md.

## Fallbacks y deprecación

- Consumidores de informes: conservar/ignorar claves nuevas que no entiendan;
  categoría/señal nueva debe mostrarse como desconocida, nunca como unchanged
  o seguro. Un schema no reconocido no autoriza reinterpretarlo silenciosamente.
- Inputs: desconocidos se conservan con warning; tipo de registro o estructura
  no soportados se rechazan. Esto no certifica formatos nuevos por semejanza.
- En 1.x se mantienen nombres, tipos y significado de campos/comandos/códigos
  existentes. Se permiten campos o valores aditivos con fallback desconocido;
  no eliminar/renombrar/reinterpretar silenciosamente los anteriores. Una
  deprecación se documenta en CHANGELOG/migración y permanece admitida durante
  1.x; una ruptura exige versión mayor y guía de transición. No hay comandos
  deprecados hoy ni calendario/periodo de soporte prometido.
- Mantener los golden de v0.1/v0.2 y pruebas CLI al cambiar datos o versiones.
  Correcciones conservadoras pueden reducir certeza, explicadas en CHANGELOG.

## Evidencia y límites

`contract-v0.1.json` procede del CLI de la wheel 0.1.0a1 publicada, instalada
independientemente; no generado por el renderer nuevo. El ejemplo sintético
tiene modified=1/separator=2. Tests comparan JSON actual completo contra esa
base, con/sin audit, alias -o, códigos y desconocidos sin perder evidencia.
Los golden de informes/comparación anteriores cubren la extensión actual.
Sin nuevos formatos/dependencias. CPython 3.12/Windows x64 es el perfil probado.

## Revisión de usuario recibida

1. Leer el [ejemplo Markdown de v0.2](../tests/fixtures/review-report.md): dos
   registros ambiguos de metadata parcial, warnings y unknown por lado.
2. Comprobar si distingue claramente metadata declarada, unknown y contenido
   instalado no verificado; si los recuentos y códigos ayudan a revisarlo.
3. Indicar qué texto/comando/schema resulta confuso o falta para el uso previsto,
   o aportar feedback real existente. No hace falta compartir listas privadas,
   instalar mods ni ejecutar PowerShell: esos comandos ya están verificados.

Resultado: el propietario respondió «He revisado el ejemplo y se entiende».
No se presenta como ensayo de comandos/perfiles reales o aprobación de un tag
estable todavía inexistente. El resultado se registra en la PR antes de salir
de draft. Los comandos de PowerShell y tests siguen ejecutados por el agente.
