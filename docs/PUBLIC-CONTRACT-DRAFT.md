# Propuesta de contrato público — #16, pendiente de feedback

**Borrador: no es un contrato estable ni una versión v1.0.** #16 exige
«Depende de feedback v0.2». No consta todavía feedback de uso de 0.2.0a1.
La autorización para avanzar/fusionar/publicar no sustituye esa evidencia.
Esta propuesta y sus tests se entregan en PR draft; no cerrar #16 ni fijar
estabilidad hasta revisarla con feedback. #19 exige además revisión humana.

## Superficie observada y propuesta a conservar

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

JSON superior actual: schema, context, summary, warnings, changes, limitations;
audit opcional. Schema actual `modlock-0.1-experimental`; extensión
`modlock-audit-0.2-experimental`. No se asigna identificador estable nuevo sin
decidir la transición. Registros conservan índices por lado, identidad y raw
decodificado; no bytes originales ni promesa de compatibilidad de instalación.

Orden observado: cambios por índices base, después head no emparejados;
categorías/keys de JSON y recuentos ordenados al serializar. Sin timestamps
ni rutas de origen añadidas; raw puede contener datos privados. Celdas Markdown
escapadas y fence dinámico; consumir JSON para integración, no parsear tablas
o asumir anchos/saltos de la ayuda. El texto de diagnósticos puede mejorar;
usar códigos de salida/categorías, no mensajes como API estable.

## Fallbacks y deprecación propuestos, sujetos a revisión

- Consumidores de informes: conservar/ignorar claves nuevas que no entiendan;
  categoría/señal nueva debe mostrarse como desconocida, nunca como unchanged
  o seguro. Un schema no reconocido no autoriza reinterpretarlo silenciosamente.
- Inputs: desconocidos se conservan con warning; tipo de registro o estructura
  no soportados se rechazan. Esto no certifica formatos nuevos por semejanza.
- Antes de estabilidad se permiten cambios documentados con migración y golden.
  Propuesta para 1.x: cambios aditivos que no alteren significado; para romper
  un campo/comando, aviso/migración y nuevo contrato de versión mayor. No se
  promete calendario ni periodo de soporte sin decisión del propietario.
- Mantener los golden de v0.1/v0.2 y pruebas CLI al cambiar datos o versiones.
  Correcciones conservadoras pueden reducir certeza, explicadas en CHANGELOG.

## Evidencia y límites

`contract-v0.1.json` procede del CLI de la wheel 0.1.0a1 publicada, instalada
independientemente; no generado por el renderer nuevo. El ejemplo sintético
tiene modified=1/separator=2. Tests comparan JSON actual completo contra esa
base, con/sin audit, alias -o, códigos y desconocidos sin perder evidencia.
Los golden de informes/comparación anteriores cubren la extensión actual.
Sin nuevos formatos/dependencias. CPython 3.12/Windows x64 es el perfil probado.

## Revisión de usuario pendiente (no ejecutable por el agente)

1. Leer el [ejemplo Markdown de v0.2](../tests/fixtures/review-report.md): dos
   registros ambiguos de metadata parcial, warnings y unknown por lado.
2. Comprobar si distingue claramente metadata declarada, unknown y contenido
   instalado no verificado; si los recuentos y códigos ayudan a revisarlo.
3. Indicar qué texto/comando/schema resulta confuso o falta para el uso previsto,
   o aportar feedback real existente. No hace falta compartir listas privadas,
   instalar mods ni ejecutar PowerShell: esos comandos ya están verificados.

No marcar este paso PASS sin respuesta real. No presentar sintéticos, tests o
autorización genérica como feedback. La PR debe registrar el resultado y las
decisiones antes de salir de draft. Los issues independientes pueden continuar.
