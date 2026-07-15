# Changelog

Todos los cambios relevantes de SpaceFlow se documentan aquí.

## [0.1.4] - 2026-07-15

- El instalador omite paquetes, entorno Python y `yt-dlp` cuando ya existen.
- Se oculta el aviso de obsolescencia de Python 3.9 emitido por `yt-dlp` en iSH.
- `SPACEFLOW_UPDATE_DEPS=1` permite actualizar dependencias de forma explícita.

## [0.1.3] - 2026-07-15

- Los Spaces públicos ya no exigen cookies antes de consultar, escuchar o descargar.
- Las cookies solo se envían a X cuando el usuario las ha importado.
- Mensaje específico cuando un Space concreto sí requiere iniciar sesión.

## [0.1.2] - 2026-07-15

- Compatibilidad con Python 3.9, incluido en versiones antiguas de Alpine/iSH.
- El instalador de iSH actualiza `pip` dentro del entorno aislado.

## [0.1.1] - 2026-07-15

- Instalación compatible con iSH y Alpine mediante `apk` y un entorno Python aislado.
- Corregida la detección de a-Shell para no confundirla con iSH.

## [0.1.0] - 2026-07-15

- Primera versión con menú y CLI.
- Información, reproducción, descarga y grabación de X Spaces.
- Cookies Netscape protegidas fuera del repositorio.
- Biblioteca M4A/MP3 con metadatos JSON.
- Instaladores para a-Shell, Termux y Windows.
- Actualizaciones verificadas desde GitHub Releases.
- Arquitectura DDD con adaptadores intercambiables.
