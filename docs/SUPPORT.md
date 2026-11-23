# Distribución y mantenimiento Windows — #18

## Estrategia elegida y límites

Wheel + sdist en GitHub Releases, con SHA256SUMS y avisos, sin PyPI, intérprete
empaquetado, ejecutable congelado o instalador. Continúa la estrategia gratuita
ya autorizada en #10/#15; no introduce servicio, tarjeta, credenciales o API.
Licencia propia MIT decidida por el propietario; no se elige otra ni se relicencia
el código ajeno. Dependencias se instalan de sus wheels upstream separadas.

Perfil comprobado: CPython 3.12 / Windows 11 x64. Local 3.12.14; CI Windows
Server 3.12.10, con symlinks reales. No confundir el intérprete observado con el
parche mínimo ni prometer todo el rango de versiones/plataformas. La wheel
py3-none-any es código Python, no una certificación multiplataforma.

0.2.0a2 distribuye la corrección de symlink roto detectada realmente en #17:
lstat rechaza la entrada final existente antes de open(x). Mantiene el límite
de concurrencia documentado, sin afirmar un sandbox de filesystem. Las releases
0.1.0a1/0.2.0a1 conservan sus bytes/hashes y nota del límite; se recomienda a2
para la política de no crear targets de enlaces de salida ya existentes.

La distribución 1.x mantiene esta estrategia. #16 tiene feedback y contrato
registrados; #19 exige revisar el candidato concreto antes de tag. La existencia
de paquetes locales no acredita una publicación: consultar la PR/release.

## Instalar y verificar sin cambios globales

Seguir [RELEASE-1.0.md](RELEASE-1.0.md): comprobar todos los hashes, venv nuevo,
lock runtime de 13 wheels, instalación no editable y pip check. Ejecutar ayuda,
versión, comparación de ejemplo JSON/Markdown/audit y errores 0/1/2. Descargar
dependencias una vez desde PyPI; la comparación funciona offline. No activar
scripts ni cambiar PATH, políticas de ejecución o Windows.

Tests de distribución construyen una wheel offline, inspeccionan todos sus
módulos/metadata/entrypoint/licencias y prueban dos builds idénticos. El lock
runtime debe ser exactamente el cierre de dependencias activas en este entorno,
sin incorporar pytest/Ruff/Mypy/backend al runtime. Tests no sustituyen instalar
los bytes publicados: PR/release registra venv desde cero, hash y smoke reales,
sdist extraído y posterior descarga de assets.

## Mantener

- Actualizar Python solo dentro de una familia comprobada y parche mantenido;
  ampliar rango requiere repetir compatibilidad/instalación/corpus y documentar.
- Cambiar dependencias en issue/PR independiente: necesidad, licencias/avisos,
  Requires-Python/Requires-Dist, wheels Windows y hashes antes de instalar.
  Repetir instalación limpia, pip check, tests, Ruff, Mypy y build reproducible.
- Runtime y dev separados; no activar extras innecesarios. Avisos de MIT,
  BSD/ISC/PSF/Apache/MPL upstream se conservan donde corresponda. No copiar código
  GPL de productores. No se audita todo el árbol Rust/C de bins upstream.
- CI solo runner estándar gratuito en repo público, permisos mínimos y sin
  publicación automática. Si el repo se vuelve privado, el job se omite por
  política de coste: no confundir ausencia de checks con PASS ni habilitar cobro.
- Gitflow, PR por issue, sin force push/borrado/auto-merge. Tags/releases solo
  según autorización y puertas de revisión. Nunca reemplazar assets de un tag
  publicado; corregir con otra versión y notas de migración.

## Diagnóstico seguro

Versiones y comando mínimo, código de salida y fixture sintético bastan para
un issue. No adjuntar listas privadas, credenciales, rutas personales, perfiles
o trazas con datos sensibles. Informes raw pueden contener metadata privada;
no se envían automáticamente. Revisar localmente antes de compartir.

Unknown y diferencias salen con 0: no equivalen a instalación reproducible.
Error 1 indica entrada/salida/contexto; 2 uso de CLI. Límites de formato y
filesystem en [COMPATIBILITY.md](COMPATIBILITY.md); no restauración de perfiles
ni resolución de conflictos. Coste adicional obligatorio 0 €.
