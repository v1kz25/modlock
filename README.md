# modlock

> Publicada **0.1.0a1 experimental**; desarrollo de v0.2 por issues, contrato todavía inestable.

El [spike del issue #1](docs/research/issue-1/REPORT.md) conserva el veredicto histórico **CONTRIBUIR**. El propietario decidió después seguir investigando modlock como auditor independiente y complementario a Meteoric. Tras integrar #7 autorizó completar **#4, #8, #9 y #10 y publicar v0.1.0 experimental**, con fusiones secuenciales y aviso si hace falta prueba manual. Es una decisión del propietario; no demuestra demanda ni valida el backlog. Las versiones propuestas siguen condicionadas a decisiones posteriores.

Auditoría read-only de modlists: diferencias semánticas y riesgos de reproducibilidad.

## Objetivo

Comparar exportaciones existentes de listas de mods, preservando incertidumbre en coincidencias y generando reportes reproducibles.

## Disponible ahora

CLI experimental de comparación read-only: [uso, contexto y límites](docs/CLI.md). JSON y Markdown deterministas, sin sobrescribir archivos existentes. Base comprobada: CPython 3.12 / Windows 11 x64.

```powershell
& .\.venv\Scripts\modlock.exe --help
& .\.venv\Scripts\modlock.exe compare BASE.json HEAD.json --context JUEGO:LINAJE
```

Solo declarar contexto cuando ambos exports comparten juego y linaje conocidos; sin contexto los mods quedan ambiguos. IDs de archivo cambiados no se emparejan por suponer actualización. APIs internas: lector Meteoric, modelo de identidad y motor conservador. No se verifica contenido instalado, hashes o compatibilidad. Instalación: [DEVELOPMENT.md](docs/DEVELOPMENT.md); licencias/dependencias: [DEPENDENCIES.md](docs/DEPENDENCIES.md).

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

MIT, elegida expresamente por el propietario para #10: [LICENSE](LICENSE). Dependencias y avisos: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Instalación del paquete y verificación de artefactos: [RELEASE.md](docs/RELEASE.md). No se redistribuyen intérprete ni dependencias dentro de la wheel.

Motor interno: [comparación conservadora](docs/COMPARISON.md), con contexto explícito y referencias exactas; sin heurística por nombre ni inferencia de actualizaciones por página.

Auditoría opcional en desarrollo: `compare BASE HEAD --audit` añade [señales verificables y unknown](docs/AUDIT.md), sin cambiar el informe predeterminado ni certificar contenido instalado.
