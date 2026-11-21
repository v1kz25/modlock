# Roadmap — modlock

No hay implementación aún. Este plan es orientativo; cada fase requiere validar la anterior.

1. **Validación técnica / PoC**: validar el hueco real y dependencias
2. **Configuración inicial**: crear base mínima verificable
3. **MVP incremental**: funcionalidad por issues pequeños
4. **Pruebas y estabilización**: pruebas, documentación y límites
5. **Primera versión pública**: release revisada y reproducible
6. **Ampliaciones**: funciones adicionales tras feedback

## Primeras tareas

- Validar diferenciación frente a Meteoric Modlist Tools
- Validar y documentar un formato de exportación inicial
- Inicializar CLI Python/Typer y suite de tests
- Implementar normalización y diff semántico read-only

## Principio de alcance

No desarrollar simultáneamente los cuatro repositorios; comenzar por openapi-contract-lab y abrir los demás sólo cuando se decida.

## Etiquetas de fase

1. Validación: `phase:validation`.
2. Preparación: `phase:setup`.
3. MVP: `phase:mvp`.
4. Estabilización: `phase:quality`.
5. Versión pública: `phase:release`.
6. Mejoras posteriores: `phase:future`.
