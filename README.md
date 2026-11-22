# modlock

> Estado: inicialización experimental. **Aún no hay MVP implementado**.

El [spike del issue #1](docs/research/issue-1/REPORT.md) conserva el veredicto histórico **CONTRIBUIR**. El propietario decidió después seguir investigando modlock como auditor independiente y complementario a Meteoric. Tras integrar #3 autorizó continuar con **#6: lector read-only**; la autorización no incluye identidad, comparación ni MVP. Es una decisión del propietario; no demuestra demanda ni valida el backlog. Las versiones propuestas siguen condicionadas a decisiones posteriores.

Auditoría read-only de modlists: diferencias semánticas y riesgos de reproducibilidad.

## Objetivo

Comparar exportaciones existentes de listas de mods, preservando incertidumbre en coincidencias y generando reportes reproducibles.

## Disponible ahora

CLI de desarrollo con ayuda y versión `0.0.0.dev0`; sin comandos de lectura, comparación o auditoría. Base inicial comprobada: CPython 3.12, Windows 11 x64 y Typer 0.29.2.

API interna `modlock.meteoric.read_meteoric`: lectura tipada del [formato Meteoric estudiado](docs/formats/meteoric-json-v1.md), con errores de estructura y advertencias por metadatos incompletos. Conserva orden, registros y campos originales sin decidir identidad. Todavía no está conectada a la CLI.

Después de la [instalación local](docs/DEVELOPMENT.md):

```powershell
& .\.venv\Scripts\modlock.exe --help
& .\.venv\Scripts\modlock.exe --version
```

Sin argumentos muestra ayuda (código 0); ayuda y versión terminan con 0. Argumentos/opciones no disponibles terminan con 2. La CLI aún no lee exportaciones. Versiones y licencias directas/transitivas: [DEPENDENCIES.md](docs/DEPENDENCIES.md); no se añaden dependencias para el lector.

## MVP previsto

- importar inicialmente un único formato existente y documentado, preferentemente export MO2/Meteoric
- validación del esquema y normalización interna
- clasificar añadidos, eliminados, actualizados, reordenados y ambiguos
- reportes JSON/Markdown deterministas y riesgos de reproducibilidad

### Fuera del MVP

- instalar o descargar mods
- autenticación Nexus
- resolver conflictos automáticamente
- diseñar estándar universal de modlists
- GUI en el MVP

## Desarrollo

- Ver [roadmap](docs/ROADMAP.md), [guía de desarrollo](docs/DEVELOPMENT.md) y [AGENTS.md](AGENTS.md).
- El punto de entrada son los GitHub Issues, no implementar el MVP de golpe.
- Desarrollo principalmente desde Windows 11; sin infraestructura de pago.

## Riesgos

Los algoritmos de identificación fuzzy pueden confundir mods; ecosistemas y formatos cambian; licencias GPL de herramientas de terceros.

## Referencias

- https://github.com/imightbemeteor/meteoric-modlist-tools
- https://github.com/ModOrganizer2/modorganizer
- https://github.com/wabbajack-tools/wabbajack

## Licencia

**Pendiente de decisión.** Este repositorio se publica sin archivo LICENSE por ahora. Ser público en GitHub no otorga automáticamente permiso para copiar, modificar o redistribuir su contenido.
