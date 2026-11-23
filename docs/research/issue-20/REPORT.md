# Spike #20 — segundo formato candidato: MO2 modlist.txt

Fecha: **23-11-2026**. Resultado: **RECHAZAR el formato aislado por ahora**, sin
implementar parser. El propietario autorizó investigar los issues posibles;
no implica que exista demanda demostrada para este adaptador. #20 está fuera
del compromiso v1.0. El veredicto histórico CONTRIBUIR del #1 permanece intacto.

## Candidato y fuentes primarias

Se investigó el archivo nativo de perfil MO2 modlist.txt, no otro JSON, ZIP,
Vortex o exportador. Revisión de código fijada a
`4ba22f0d8b6f9e08e44008b8395cd774551b4ebe`; no una promesa de soporte de todas
las releases MO2 ni una exportación real ejecutada en GUI.

- [Escritor y lector de perfil, revisión fijada](https://github.com/ModOrganizer2/modorganizer/blob/4ba22f0d8b6f9e08e44008b8395cd774551b4ebe/src/profile.cpp#L243): emite UTF-8, líneas CRLF, prefijos de activación/foreign y nombres; recorre prioridades en sentido inverso y omite entradas de prioridad automática. No emite los metadatos de identidad necesarios para el modelo modlock.
- [LICENSE del mismo commit](https://github.com/ModOrganizer2/modorganizer/blob/4ba22f0d8b6f9e08e44008b8395cd774551b4ebe/LICENSE): GPLv3. La cabecera de profile.cpp declara GPL-3.0-or-later. Se inspecciona la implementación, sin copiarla, incorporarla, ejecutarla o relicenciarla como MIT. Tampoco se redistribuyen perfiles o listas de terceros.

## Demanda observada, sin inflarla

Dos peticiones públicas reales del proyecto se revisaron como señales limitadas:

| Fuente primaria | Petición / fechas | Lo que no demuestra |
|---|---|---|
| [MO2 #923](https://github.com/ModOrganizer2/modorganizer/issues/923) | Empaquetar/exportar contenido; creada 06-12-2019, última actualización consultada 23-09-2020, abierta al consultar | Necesidad de otro auditor o de este formato aislado |
| [MO2 #2259](https://github.com/ModOrganizer2/modorganizer/issues/2259) | Exportar/respaldar sin juego instalado; creada 12-07-2025, actualización 14-07-2025, abierta al consultar | Demanda validada para modlock o aceptación de un adaptador nuevo |

No son solicitudes recientes de auditoría reproducible ni estudio de mercado.
No se verifican las alegaciones técnicas de esos reportes ni se toman como
hechos sobre corrupción de perfiles. No hay entrevistas, feedback de uso del
adaptador, muestra de cliente con permiso o necesidad priorizada. Autorización
del propietario y existencia de peticiones de exportación no cubren esa brecha.

## Matriz de correspondencia del archivo aislado

| Modelo modlock | Evidencia del candidato | Decisión conservadora |
|---|---|---|
| Nombre original | Nombre textual | Conservar, nunca identidad por nombre |
| Activación | Prefijos + / -; * señala foreign | No equiparar foreign a prueba de instalación |
| Posición | Secuencia almacenada / prioridad inversa del escritor | No confundir con orden de carga de plugins |
| ID de página/archivo | No campos emitidos por ese escritor | unknown, sin matching por suposición |
| Versión/variante instalada | No campos emitidos | unknown |
| Hash, juego, procedencia | No evidencia verificada | unknown |
| Separador/sección | Nombre sin campo tipado equivalente | No inferir por sufijo |
| Plugins/tags/metadata general | No equivalentes completos | No fabricar arrays vacíos como datos conocidos |

## Casos reproducibles propios

Seis textos UTF-8/CRLF sintéticos: dos iguales con escenarios de variante
distintos, reordenación, renombre, Unicode/sufijo y lista sin entradas. No fueron
emitidos por MO2 ni prueban su aceptación; son casos de pérdida de información y
límites, inventados para la investigación. scenarios.json es descripción del
experimento, no un nuevo formato de producto. IDs/versiones de esos escenarios
son ficticios, no referencias comprobadas ni hashes inventados.

Los dos archivos idénticos pueden representar versiones/fileids distintos en
el mismo juego/linaje sintético. Sin datos adicionales no se puede distinguir
ese cambio, ni convertir un nombre en referencias exactas. El script solo
comprueba igualdad de bytes, escenarios distintos, hashes reales de fixtures y
rechazo por la CLI JSON actual; **no parsea ni convierte el candidato**.

```powershell
& .\.venv\Scripts\python.exe docs/research/issue-20/probe.py
& .\.venv\Scripts\python.exe -m pytest -q -rs
& .\.venv\Scripts\python.exe -m ruff check src tests
& .\.venv\Scripts\python.exe -m ruff format --check src tests
& .\.venv\Scripts\python.exe -m mypy src/modlock
```

Salida ejecutada en results.json, sin rutas privadas. La suite se registra en
la PR; no presentar rechazo de modlock como validación del productor ni un PASS
de GUI. No hay prueba manual de usuario necesaria para decidir no implementar.

## Decisión y mantenimiento

No continuar con un parser de modlist.txt **aislado**: aporta nombres/activación
pero no identidad suficiente para comparación conservadora ni evidencia de una
necesidad de auditoría concreta. Enriquecerlo leyendo meta.ini, perfiles u otros
archivos ampliaría el alcance, acceso a filesystem, licencias y matriz de
compatibilidad; no se hace como atajo. Fuzzy/nombres no resuelven esa ausencia.

Riesgos: formato interno sin contrato propio de exportación para modlock,
prioridades invertidas/entradas omitidas, semántica foreign y separadores,
versiones MO2 futuras, corpus de usuarios privado y reutilización indebida de
código GPL. Coste adicional obligatorio 0 €, solo lectura/documentación local.

Reabrir investigación solo con petición de auditoría específica, muestra con
permiso y datos verificables suficientes para una matriz útil, más revisión de
licencias/alcance. No se rechazan todas las alternativas ni se afirma ausencia
de demanda mundial. No se añade parser, dependencia, estándar, release o soporte
ficticio. La tarea termina en esta decisión trazable.
