# Roadmap — modlock

No hay MVP implementado ni releases. Las versiones siguientes son hipótesis condicionadas a la validación y a decisiones del propietario, no compromisos de construir todas las funciones.

1. **Validación técnica / PoC**: validar el hueco real y dependencias
2. **Configuración inicial**: crear base mínima verificable
3. **MVP incremental**: funcionalidad por issues pequeños
4. **Pruebas y estabilización**: pruebas, documentación y límites
5. **Primera versión pública**: release revisada y reproducible
6. **Ampliaciones**: funciones adicionales tras feedback

## Puerta de decisión: issue #1

El [spike de diferenciación](research/issue-1/REPORT.md) propone **CONTRIBUIR** a Meteoric: hay brechas de auditoría reproducibles, pero no evidencia suficiente para justificar otro motor y producto. Incluye diez pares sintéticos, dos métricas y ejecuciones locales. La decisión está pendiente de revisión; no habilita la fase siguiente.

Con este veredicto no se inicia #2, la CLI ni el MVP. Si el propietario decide CONTINUAR con nueva evidencia, el siguiente issue sería #2 (formato); después #3 (setup). Cada tarea requiere su propia autorización y PR. La investigación de #1 no equivale a tener un parser o auditoría implementados.

## Versiones propuestas y condiciones de salida

| Hipótesis | Implementado | Previsto | Dependencias y salida de fase |
|---|---|---|---|
| v0.1.0 experimental | Documentación inicial; evidencia de #1 preparada para revisión. Sin CLI, parser ni paquete | #1–#4 y #6–#10: validar diferenciación y formato, setup, lectura, identidad, diff conservador, JSON/Markdown, calidad y prerelease revisable | Decisión explícita CONTINUAR en #1; #2→#3→#6→#7→#4→#8→#9→#10. Salida: un formato real, incertidumbre preservada, pruebas y smoke Windows ejecutados, licencias revisadas, instalación/artefactos reproducidos; publicación solo autorizada por el propietario |
| v0.2.0 experimental | Nada | #11–#15: señales de reproducibilidad, orden/metadatos, snapshots, informes y corpus ampliados | v0.1 validada con feedback y necesidad de cada incremento; #11 depende de #6–#10, #12 de #7/#4, #13 de #6–#8, #14 de #8, #15 de los demás v0.2. Salida: riesgos verificables con unknown, compatibilidad de informes, determinismo, corpus Windows y smoke del artefacto; segunda prerelease solo con aprobación |
| v1.0.0 estable | Nada | #16–#19: contrato estable de CLI/informes, exportaciones y seguridad read-only, distribución/mantenimiento, candidato estable | Feedback v0.2, matriz de formato y corpus, estrategia de distribución y todos los bloqueantes resueltos. Salida: contrato y pruebas de compatibilidad, entradas intactas y adversariales, instalación limpia, hashes reales, licencias/avisos, notas y revisión humana antes de tag/release |
| Posterior a v1.0, sin compromiso | Nada | #20: spike de segundo formato | Demanda, muestras y licencia comprobadas; decisión continuar/rechazar antes de cualquier parser |

Los issues están abiertos y no constituyen versiones publicadas. #5 fue una PR de documentación Gitflow, no una tarea del MVP. No se crean tags ni releases como parte del spike.

## Decisiones pendientes y riesgos

- Aprobar o revisar CONTRIBUIR. De aceptarse, #2–#4 y #6–#19 dejan de ser un plan autorizado de producto independiente; podrían aportar ideas o casos a Meteoric, pero requieren revisión de alcance. #20 también queda suspendido. No se cierran ni reescriben masivamente.
- La auditoría propuesta en #11 sería la diferenciación principal; posponerla hasta v0.2 mientras v0.1 replica comparación existente exige justificación si se retoma el producto.
- Delimitar #4/#12 (orden), #8/#13 (snapshots) y #8/#14 (informes) para evitar duplicación. Las puertas de distribución #10/#15/#18 verifican madurez distinta, sin garantizar la siguiente fase.
- Decidir licencia propia y dependencias reales solo cuando proceda; formatos cambiantes, matching ambiguo y GPL de terceros siguen siendo riesgos. Python/Typer continúa como evaluación provisional.
- Los casos sintéticos prueban límites técnicos; faltan demanda de usuarios y aceptación de una contribución upstream. Coste adicional obligatorio: 0 €, ejecución local por defecto.

## Principio de alcance

Esta tarea autoriza exclusivamente el issue #1 de modlock. No desarrollar fases siguientes ni otros repositorios. Toda integración requiere revisión explícita y Gitflow según DEVELOPMENT.md.

## Etiquetas de fase

1. Validación: `phase:validation`.
2. Preparación: `phase:setup`.
3. MVP: `phase:mvp`.
4. Estabilización: `phase:quality`.
5. Versión pública: `phase:release`.
6. Mejoras posteriores: `phase:future`.
