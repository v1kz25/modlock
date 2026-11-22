# modlock

> Estado: inicialización experimental. **Aún no hay MVP implementado**.

El [spike del issue #1](docs/research/issue-1/REPORT.md) conserva el veredicto histórico **CONTRIBUIR**. Tras #2, el propietario decidió seguir investigando modlock como auditor independiente y complementario a Meteoric, y autorizó **solo #3: setup Python/Typer y pruebas**. Es una decisión del propietario; no demuestra demanda ni valida el backlog. Las versiones propuestas siguen condicionadas a decisiones posteriores.

Auditoría read-only de modlists: diferencias semánticas y riesgos de reproducibilidad.

## Objetivo

Comparar exportaciones existentes de listas de mods, preservando incertidumbre en coincidencias y generando reportes reproducibles.

## Disponible ahora

CLI de desarrollo con ayuda y versión `0.0.0.dev0`; sin comandos de lectura, comparación o auditoría. Base inicial comprobada: CPython 3.12, Windows 11 x64 y Typer 0.29.2.

Después de la [instalación local](docs/DEVELOPMENT.md):

```powershell
& .\.venv\Scripts\modlock.exe --help
& .\.venv\Scripts\modlock.exe --version
```

Sin argumentos muestra ayuda (código 0); ayuda y versión terminan con 0. Argumentos/opciones no disponibles terminan con 2. No se leen exportaciones. Versiones y licencias directas/transitivas: [DEPENDENCIES.md](docs/DEPENDENCIES.md).

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
