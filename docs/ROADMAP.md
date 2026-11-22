# Roadmap — modlock

No hay MVP implementado ni releases. Las versiones siguientes son hipótesis condicionadas a la validación y a decisiones del propietario, no compromisos de construir todas las funciones.

1. **Validación técnica / PoC**: validar el hueco real y dependencias
2. **Configuración inicial**: crear base mínima verificable
3. **MVP incremental**: funcionalidad por issues pequeños
4. **Pruebas y estabilización**: pruebas, documentación y límites
5. **Primera versión pública**: release revisada y reproducible
6. **Ampliaciones**: funciones adicionales tras feedback

## Puerta de decisión: issue #1

El [spike de diferenciación](research/issue-1/REPORT.md), integrado por la PR #21, propone **CONTRIBUIR** a Meteoric: hay brechas de auditoría reproducibles, pero no evidencia suficiente para justificar otro motor y producto. Incluye diez pares sintéticos, dos métricas y ejecuciones locales.

El 22-11-2026, tras revisar ese resultado, el propietario autorizó expresamente #2 como investigación limitada pese a CONTRIBUIR: [formato y fixtures](formats/meteoric-json-v1.md). La excepción permite documentar y validar el formato, sin cambiar el veredicto a CONTINUAR. No autoriza #3, CLI, parser ni MVP. Cada tarea posterior y cada fusión requieren su propia autorización y PR. La investigación de #1/#2 no equivale a tener un lector o auditoría implementados.

## Versiones propuestas y condiciones de salida

| Hipótesis | Implementado | Previsto | Dependencias y salida de fase |
|---|---|---|---|
| v0.1.0 experimental | Documentación inicial y evidencia de #1 integrada; documentación/corpus de #2 preparados para revisión. Sin CLI, parser ni paquete | #1–#4 y #6–#10: validar diferenciación y formato, setup, lectura, identidad, diff conservador, JSON/Markdown, calidad y prerelease revisable | Implementación suspendida con CONTRIBUIR; excepción autorizada solo para investigar #2. Si se autoriza retomar producto: #2→#3→#6→#7→#4→#8→#9→#10. Salida: un formato real, incertidumbre preservada, pruebas y smoke Windows ejecutados, licencias revisadas, instalación/artefactos reproducidos; publicación solo autorizada por el propietario |
| v0.2.0 experimental | Nada | #11–#15: señales de reproducibilidad, orden/metadatos, snapshots, informes y corpus ampliados | v0.1 validada con feedback y necesidad de cada incremento; #11 depende de #6–#10, #12 de #7/#4, #13 de #6–#8, #14 de #8, #15 de los demás v0.2. Salida: riesgos verificables con unknown, compatibilidad de informes, determinismo, corpus Windows y smoke del artefacto; segunda prerelease solo con aprobación |
| v1.0.0 estable | Nada | #16–#19: contrato estable de CLI/informes, exportaciones y seguridad read-only, distribución/mantenimiento, candidato estable | Feedback v0.2, matriz de formato y corpus, estrategia de distribución y todos los bloqueantes resueltos. Salida: contrato y pruebas de compatibilidad, entradas intactas y adversariales, instalación limpia, hashes reales, licencias/avisos, notas y revisión humana antes de tag/release |
| Posterior a v1.0, sin compromiso | Nada | #20: spike de segundo formato | Demanda, muestras y licencia comprobadas; decisión continuar/rechazar antes de cualquier parser |

Los issues están abiertos y no constituyen versiones publicadas. #5 fue una PR de documentación Gitflow, no una tarea del MVP. No se crean tags ni releases como parte del spike.

## Decisiones pendientes y riesgos

- Decidir si se contribuye a Meteoric o se aporta evidencia nueva para un producto independiente. La autorización excepcional de #2 no habilita #3–#4 ni #6–#20; los casos podrían ayudar a una contribución, cuyo alcance también requeriría autorización. No se cierran ni reescriben masivamente los issues.
- La auditoría propuesta en #11 sería la diferenciación principal; posponerla hasta v0.2 mientras v0.1 replica comparación existente exige justificación si se retoma el producto.
- Delimitar #4/#12 (orden), #8/#13 (snapshots) y #8/#14 (informes) para evitar duplicación. Las puertas de distribución #10/#15/#18 verifican madurez distinta, sin garantizar la siguiente fase.
- Decidir licencia propia y dependencias reales solo cuando proceda; formatos cambiantes, matching ambiguo y GPL de terceros siguen siendo riesgos. Python/Typer continúa como evaluación provisional.
- Los casos sintéticos prueban límites técnicos; faltan demanda de usuarios y aceptación de una contribución upstream. Coste adicional obligatorio: 0 €, ejecución local por defecto.

## Principio de alcance

La tarea actual autoriza exclusivamente la investigación del issue #2 de modlock. No desarrollar fases siguientes ni otros repositorios. Toda integración requiere revisión explícita y Gitflow según DEVELOPMENT.md.

## Etiquetas de fase

1. Validación: `phase:validation`.
2. Preparación: `phase:setup`.
3. MVP: `phase:mvp`.
4. Estabilización: `phase:quality`.
5. Versión pública: `phase:release`.
6. Mejoras posteriores: `phase:future`.
