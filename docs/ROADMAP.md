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

El 22-11-2026 el propietario autorizó #2 como investigación limitada; su [formato y fixtures](formats/meteoric-json-v1.md) se integraron por la PR #22. Los criterios de #1 y #2 se revisaron y sus resultados se reprodujeron antes de cerrarlos con evidencia.

Después, el propietario decidió continuar investigando modlock como herramienta independiente de auditoría read-only, complementaria a Meteoric, y autorizó **únicamente #3: inicialización Python/Typer y pruebas**. Esta decisión no cambia el veredicto histórico CONTRIBUIR ni afirma demanda o validación técnica del producto. No autoriza lector, motor, auditorías ni MVP. Cada tarea posterior y cada fusión requieren su propia autorización y PR.

## Versiones propuestas y condiciones de salida

| Hipótesis | Implementado | Previsto | Dependencias y salida de fase |
|---|---|---|---|
| v0.1.0 experimental | Evidencia #1 y formato/corpus #2 integrados. #3 prepara paquete local, ayuda/versión y pruebas para revisión; sin parser, motor ni auditorías | #1–#4 y #6–#10: validar diferenciación y formato, setup, lectura, identidad, diff conservador, JSON/Markdown, calidad y prerelease revisable | Autorizado solo #3 por decisión posterior del propietario. Cadena técnica futura: #3→#6→#7→#4→#8→#9→#10, sujeta a autorización. Salida: un formato real, incertidumbre preservada, pruebas y smoke Windows ejecutados, licencias revisadas, instalación/artefactos reproducidos; publicación solo autorizada por el propietario |
| v0.2.0 experimental | Nada | #11–#15: señales de reproducibilidad, orden/metadatos, snapshots, informes y corpus ampliados | v0.1 validada con feedback y necesidad de cada incremento; #11 depende de #6–#10, #12 de #7/#4, #13 de #6–#8, #14 de #8, #15 de los demás v0.2. Salida: riesgos verificables con unknown, compatibilidad de informes, determinismo, corpus Windows y smoke del artefacto; segunda prerelease solo con aprobación |
| v1.0.0 estable | Nada | #16–#19: contrato estable de CLI/informes, exportaciones y seguridad read-only, distribución/mantenimiento, candidato estable | Feedback v0.2, matriz de formato y corpus, estrategia de distribución y todos los bloqueantes resueltos. Salida: contrato y pruebas de compatibilidad, entradas intactas y adversariales, instalación limpia, hashes reales, licencias/avisos, notas y revisión humana antes de tag/release |
| Posterior a v1.0, sin compromiso | Nada | #20: spike de segundo formato | Demanda, muestras y licencia comprobadas; decisión continuar/rechazar antes de cualquier parser |

Los issues #1/#2 están cerrados por criterios cumplidos, con evidencia en las PRs fusionadas #21/#22; no representan versiones publicadas. #5 fue una PR documental de Gitflow. #3 queda para revisión; no se crean tags ni releases en esta tarea.

## Decisiones pendientes y riesgos

- La decisión del propietario permite investigar una herramienta complementaria, pero la autorización vigente se limita a #3. #4 y #6–#20 no están autorizados. La recomendación técnica de contribuir permanece como antecedente, sin sustituirla por evidencia de demanda inexistente.
- La auditoría propuesta en #11 sería la diferenciación principal; posponerla hasta v0.2 mientras v0.1 replica comparación existente exige justificación si se retoma el producto.
- Delimitar #4/#12 (orden), #8/#13 (snapshots) y #8/#14 (informes) para evitar duplicación. Las puertas de distribución #10/#15/#18 verifican madurez distinta, sin garantizar la siguiente fase.
- La licencia propia sigue pendiente. Las dependencias del setup y sus licencias se registran en [DEPENDENCIES.md](DEPENDENCIES.md); formatos cambiantes, matching ambiguo y GPL de terceros siguen siendo riesgos.
- Los casos sintéticos prueban límites técnicos; faltan demanda de usuarios y aceptación de una contribución upstream. Coste adicional obligatorio: 0 €, ejecución local por defecto.

## Principio de alcance

La tarea actual autoriza exclusivamente el setup del issue #3 de modlock. No desarrollar fases siguientes ni otros repositorios. Toda integración requiere revisión explícita y Gitflow según DEVELOPMENT.md.

## Etiquetas de fase

1. Validación: `phase:validation`.
2. Preparación: `phase:setup`.
3. MVP: `phase:mvp`.
4. Estabilización: `phase:quality`.
5. Versión pública: `phase:release`.
6. Mejoras posteriores: `phase:future`.
