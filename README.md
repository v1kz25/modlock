# modlock

> Estado: planificación inicial. **Aún no hay MVP implementado**.

El [spike del issue #1](docs/research/issue-1/REPORT.md) propone **CONTRIBUIR** a Meteoric, pendiente de revisión. Incluye diez comparaciones sintéticas ejecutadas y dos métricas de auditoría. No se inicia el MVP ni se comprometen las versiones propuestas sin una decisión posterior.

Auditoría read-only de modlists: diferencias semánticas y riesgos de reproducibilidad.

## Objetivo

Comparar exportaciones existentes de listas de mods, preservando incertidumbre en coincidencias y generando reportes reproducibles.

## Stack provisional

Python + Typer (verificar licencia de dependencias y versión de Python). La versión concreta y la idoneidad se validarán en el primer spike técnico.

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
