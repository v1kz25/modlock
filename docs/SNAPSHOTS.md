# Exportaciones guardadas como snapshots — #13

Un snapshot aquí es el archivo Meteoric JSON ya exportado, conservado localmente
por el usuario. `compare ANTES.json DESPUES.json` ya admite dos snapshots; no
requiere formato nuevo, base de datos ni comando simulado `snapshot`. El alcance
de #13 es verificar ese uso real, no copiar perfiles o crear un gestor de copias.
No se añade manifiesto: no aporta evidencia de contenido instalado y timestamps,
rutas o nombres de usuario perjudicarían privacidad y determinismo sin resolver
la falta de juego/procedencia del formato.

```powershell
& .\.venv\Scripts\modlock.exe compare ANTES.json DESPUES.json --context JUEGO:LINAJE --audit --output NUEVO.json
```

El usuario debe conocer mismo juego y linaje para declarar contexto. Guardar dos
archivos no demuestra ese contexto ni convierte referencias en contenido igual.
Puede omitirlo: habrá ambigüedad explícita. `--audit` es opcional.

## Repetibilidad y reversibilidad

Con los mismos bytes, opciones y versión, el informe es determinista y no incluye
fecha de ejecución ni ruta de los snapshots. JSON/Markdown conservan todos los
registros raw decodificados. No preservan la serialización original (espacios,
BOM, escapes, representación numérica); conservar los originales si se necesita
reproducir sus bytes. El informe no es otro formato de importación.

Invertir BASE/HEAD intercambia evidencia y añadido/eliminado. Cambios de metadata
y versiones conservan sus campos; reglas conservadoras pueden seguir marcando
ambigüedad. Esto permite revisar la comparación inversa, **no** restaurar una
instalación, aplicar un parche o deshacer cambios del sistema. No se instala nada.

Cada entrada mantiene el límite de 16 MiB (incluido BOM), UTF-8 y validación del
lector. Si alguna falla no se crea informe ni se altera la otra. Destinos ya
existentes nunca se sobrescriben; no se abren rutas nombradas dentro de metadata.
Los informes raw pueden contener nombres/rutas privadas del export; el hecho de
no insertar rutas de entrada no anonimiza esos campos. Mantenerlos locales.

## Evidencia #13

Tests de procesos reales `python -m modlock` desde otro directorio, rutas con
espacios/Unicode, datos Unicode/BOM, JSON/Markdown con/sin audit, bytes repetibles,
SHA-256 de entradas intactos, comparación inversa, ausente/malformado y entrada
de 16 MiB + 1 rechazada antes de parsear. Ese caso comprueba el límite, no es un
benchmark. Suite/lint completos y resultados constan en la PR. No hay prueba
manual obligatoria del propietario ni dependencia nueva.
