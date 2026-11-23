# Roadmap — modlock

v0.1.0a1 experimental publicada; #1–#4 y #6–#10 completados. v0.2 se desarrolla por tareas autorizadas y dependencias. Las versiones siguientes son hipótesis condicionadas a la validación y a decisiones del propietario, no compromisos de construir todas las funciones.

1. **Validación técnica / PoC**: validar el hueco real y dependencias
2. **Configuración inicial**: crear base mínima verificable
3. **MVP incremental**: funcionalidad por issues pequeños
4. **Pruebas y estabilización**: pruebas, documentación y límites
5. **Primera versión pública**: release revisada y reproducible
6. **Ampliaciones**: funciones adicionales tras feedback

## Puerta de decisión: issue #1

El [spike de diferenciación](research/issue-1/REPORT.md), integrado por la PR #21, propone **CONTRIBUIR** a Meteoric: hay brechas de auditoría reproducibles, pero no evidencia suficiente para justificar otro motor y producto. Incluye diez pares sintéticos, dos métricas y ejecuciones locales.

El 22-11-2026 el propietario autorizó #2 como investigación limitada; su [formato y fixtures](formats/meteoric-json-v1.md) se integraron por la PR #22. Los criterios de #1 y #2 se revisaron y sus resultados se reprodujeron antes de cerrarlos con evidencia.

Después, el propietario decidió continuar investigando modlock como herramienta independiente de auditoría read-only, complementaria a Meteoric, y autorizó #3 y después #6, pese a la condición heredada de CONTRIBUIR. Se integraron las PRs #23/#24 con su aprobación y se cerraron ambos issues con evidencia. Su instrucción posterior «sigue con la siguiente tarea» autoriza **#7: identidad e incertidumbre**. Estas decisiones no cambian el veredicto histórico ni afirman demanda o validación técnica del producto. El propietario autorizó posteriormente #4/#8/#9/#10 y su publicación experimental, según el apartado final. Esto no autoriza v0.2 ni auditorías de contenido.

## Versiones propuestas y condiciones de salida

| Hipótesis | Implementado | Previsto | Dependencias y salida de fase |
|---|---|---|---|
| v0.1.0 experimental | #1/#2/#3/#6/#7/#4/#8/#9 integrados: formato, lector, identidad, comparación conservadora, CLI/informes y CI. #10 completado, distribución MIT publicada | #1–#4 y #6–#10: validar diferenciación y formato, setup, lectura, identidad, diff conservador, JSON/Markdown, calidad y prerelease revisable | Autorizados #4/#8/#9/#10 y publicación experimental. Cadena #7→#4→#8→#9→#10. Salida: un formato real, incertidumbre preservada, pruebas y smoke Windows ejecutados, licencias revisadas, instalación/artefactos reproducidos; publicación solo autorizada por el propietario |
| v0.2.0 experimental | #11–#14 integrados (PRs #31–#34); #15 completado y 0.2.0a1 publicada; #18 completado y 0.2.0a2 corregida publicada | #11–#15: señales de reproducibilidad, orden/metadatos, snapshots, informes y corpus ampliados | v0.1 validada con feedback y necesidad de cada incremento; #11 depende de #6–#10, #12 de #7/#4, #13 de #6–#8, #14 de #8, #15 de los demás v0.2. Salida: riesgos verificables con unknown, compatibilidad de informes, determinismo, corpus Windows y smoke del artefacto; segunda prerelease solo con aprobación |
| v1.0.0 estable | #17 integrado: matriz y corrección read-only; #16 contrato definido y feedback del propietario recibido, #18 distribución completada; #19 pendiente de candidato/revisión humana. Sin versión estable | #16–#19: contrato estable de CLI/informes, exportaciones y seguridad read-only, distribución/mantenimiento, candidato estable | Feedback v0.2, matriz de formato y corpus, estrategia de distribución y todos los bloqueantes resueltos. Salida: contrato y pruebas de compatibilidad, entradas intactas y adversariales, instalación limpia, hashes reales, licencias/avisos, notas y revisión humana antes de tag/release |
| Posterior a v1.0, sin compromiso | Spike #20: [rechazado modlist.txt aislado por ahora](research/issue-20/REPORT.md), sin parser | #20: spike de segundo formato | Demanda, muestras y licencia comprobadas; decisión continuar/rechazar antes de cualquier parser |

Evidencia: PRs fusionadas #21–#28, issues #1/#2/#3/#6/#7/#4/#8/#9 completados. #5 fue una PR documental. #10 registra construcción, instalación de artefactos y publicación.

## Decisiones pendientes y riesgos

- La decisión del propietario permite investigar una herramienta complementaria, pero la autorización vigente completa v0.1 (#4/#8/#9/#10) y permite su prerelease. La instrucción posterior del propietario autoriza trabajar los issues posibles y fusionar/publicar tras controles; detener los pasos que requieran prueba manual o decisión pendiente. La recomendación técnica de contribuir permanece como antecedente, sin sustituirla por evidencia de demanda inexistente.
- La auditoría propuesta en #11 sería la diferenciación principal; posponerla hasta v0.2 mientras v0.1 replica comparación existente exige justificación si se retoma el producto.
- Delimitar #4/#12 (orden), #8/#13 (snapshots) y #8/#14 (informes) para evitar duplicación. Las puertas de distribución #10/#15/#18 verifican madurez distinta, sin garantizar la siguiente fase.
- La licencia propia MIT fue decidida expresamente por el propietario para #10. Las dependencias del setup y sus licencias se registran en [DEPENDENCIES.md](DEPENDENCIES.md); formatos cambiantes, matching ambiguo y GPL de terceros siguen siendo riesgos.
- Los casos sintéticos prueban límites técnicos; faltan demanda de usuarios y aceptación de una contribución upstream. Coste adicional obligatorio: 0 €, ejecución local por defecto.

## Principio de alcance

La tarea actual continúa desde #11 por dependencias, una rama/PR por issue, con fusiones/versiones autorizadas tras verificaciones. No trabajar otros repositorios; avisar ante prueba manual o decisión pendiente. No dar por satisfechas las puertas de feedback/revisión humana con datos inventados.

## Etiquetas de fase

1. Validación: `phase:validation`.
2. Preparación: `phase:setup`.
3. MVP: `phase:mvp`.
4. Estabilización: `phase:quality`.
5. Versión pública: `phase:release`.
6. Mejoras posteriores: `phase:future`.

## Autorización posterior para v0.1.0

El propietario autoriza completar #4, #8, #9 y #10, fusionar sus PRs tras verificaciones y publicar una prerelease experimental. Se avisa si aparece una prueba manual necesaria. CONTRIBUIR permanece como conclusión histórica; esto no valida demanda ni autoriza v0.2. El trabajo sigue secuencialmente en una rama/PR por issue y la publicación se prepara en release/0.1.0a1. El propietario decidió MIT expresamente para #10. Los párrafos anteriores registran autorizaciones históricas más limitadas, sustituidas solo para este alcance.

## Autorización posterior para continuar

El 23-11-2026 el propietario autorizó #11 y después todos los issues posibles, con fusiones/versiones tras controles mientras no necesite hacer pruebas manuales. #11 aporta señales opt-in; los criterios de cada issue y las puertas de feedback/revisión humana siguen vigentes. La autorización no equivale a evidencia de demanda, feedback de usuarios o validación estable.

## Cierre del spike #20

La autorización amplia permite investigarlo sin esperar a v1.0, sin comprometer un adaptador. Se inspeccionó MO2 modlist.txt con fuente/licencia fijadas y dos peticiones públicas de exportación, que no prueban demanda de auditoría. Seis casos sintéticos reproducibles muestran límites de información; decisión RECHAZAR el formato aislado por ahora. No implementar parser ni enriquecerlo leyendo perfiles por suposición. #16/PR #37 sigue pendiente de feedback v0.2; #19 no puede declarar estable sin esa dependencia y revisión humana.

## Feedback #16 recibido

El 23-11-2026 el propietario revisó el ejemplo v0.2 y confirmó que se entiende. Feedback limitado a presentación, no demanda ni prueba de perfiles reales. #16 fija contrato 1.x conservando IDs/JSON previos, con golden del artefacto v0.1. #19 sigue requiriendo revisión humana del candidato concreto antes de tag estable.
