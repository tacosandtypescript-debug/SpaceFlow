# Changelog

Todos los cambios relevantes de SpaceFlow se documentan aquí.

## [Sin publicar]

- README reorganizado con compatibilidad, instalación, uso, actualizaciones y enlaces.
- Nuevas guías de instalación, uso y solución de problemas por plataforma.
- Metadatos del paquete enlazados a la documentación y al changelog.

## [0.1.10] - 2026-07-15

- Configuración automática de `volume-keys = volume` en Termux al escuchar.
- Recarga inmediata de las preferencias para que los botones físicos controlen Android.
- Se conserva el resto de la configuración personal de `termux.properties`.

## [0.1.9] - 2026-07-15

- Controles de audio visibles directamente en el menú principal.
- Detención, pausa y continuación con respaldo mediante el proceso de MPV.
- Salida OpenSL ES explícita para que los botones de volumen de Android controlen el audio.
- Comprobación de nuevas versiones cada vez que se abre SpaceFlow.

## [0.1.8] - 2026-07-15

- Reproducción de Termux en segundo plano para devolver inmediatamente el menú.
- Panel para pausar, continuar, detener y subir o bajar el volumen.
- Comandos `spaceflow playback` para controlar el audio fuera del menú.
- La actualización móvil desde el menú ejecuta el instalador completo y añade dependencias faltantes.

## [0.1.7] - 2026-07-15

- Reproducción HLS dentro de Termux mediante `mpv` y OpenSL ES.
- El instalador añade `mpv` solo cuando no está instalado.
- Recuperación de nombres de hablantes desde los metadatos públicos entregados por X.

## [0.1.6] - 2026-07-15

- Menú reorganizado en acciones principales y herramientas.
- Colores accesibles para opciones, estados correctos, avisos y errores.
- Compatibilidad con `NO_COLOR` y salidas redirigidas sin códigos ANSI.

## [0.1.5] - 2026-07-15

- “Escuchar” abre inmediatamente el stream HLS en el reproductor del sistema sin descargarlo antes.
- En a-Shell se usa la integración `open` de iOS para reproducir el Space.
- iSH explica su limitación de audio y recomienda a-Shell o descargar el archivo.
- Una cancelación de FFmpeg ya no se presenta como una instalación defectuosa.

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
