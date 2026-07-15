# Solución de problemas

## `spaceflow: not found`

Actualiza ejecutando de nuevo el instalador. Desde SpaceFlow 0.1.11, Termux crea
el comando directamente en `$PREFIX/bin` y queda disponible sin reiniciar:

```sh
curl -fsSL https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.sh | sh
spaceflow --version
```

En instalaciones antiguas también puedes cerrar y volver a abrir la terminal
para recargar el PATH.

## `pkg: not found` en iSH

iSH utiliza Alpine Linux y su gestor es `apk`. No pegues instrucciones de
Termux manualmente. Usa el instalador universal:

```sh
curl -fsSL https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.sh | sh
```

## `irm: not found` o `iex: not found`

Esos comandos pertenecen a Windows PowerShell. En Termux, a-Shell e iSH usa el
comando `curl ... | sh` de la guía de instalación.

## Los botones de volumen no funcionan en Termux

Desde SpaceFlow 0.1.10, al escuchar se añade automáticamente
`volume-keys = volume` a `~/.termux/termux.properties` y se recargan las
preferencias. Comprueba primero:

```sh
spaceflow --version
```

Si tienes una versión anterior, actualiza con `spaceflow update`. Si el teléfono
aún conserva el comportamiento anterior, cierra Termux completamente y vuelve a
abrirlo. Como reparación manual:

```sh
mkdir -p ~/.termux
echo 'volume-keys = volume' >> ~/.termux/termux.properties
termux-reload-settings
```

Esta preferencia hace que los botones dejen de actuar como `Ctrl` y tecla
especial dentro de Termux.

## No puedo detener el audio de Termux

Usa la opción `7` del menú o ejecuta:

```sh
spaceflow playback stop
```

SpaceFlow intenta primero el control de MPV y después termina el proceso de audio
guardado si la conexión interna no responde.

## No se escucha en a-Shell

a-Shell debe abrir el reproductor nativo de iOS. Revisa que el volumen multimedia
no esté al mínimo, que no exista una salida Bluetooth seleccionada y que iOS no
haya cerrado el reproductor. Vuelve a `Escuchar ahora` y utiliza los controles de
iOS, no las opciones MPV de Termux.

## No se escucha en iSH

Es una limitación de iSH: no expone salida de audio. Descarga en M4A y abre el
archivo desde Archivos, o utiliza a-Shell para escuchar.

## X solicita cookies

Los Spaces públicos normalmente no las necesitan. Si un Space requiere sesión,
importa un archivo Netscape actualizado:

```sh
spaceflow auth import /ruta/cookies.txt
```

No publiques el archivo ni lo envíes por un chat.

## FFmpeg termina con código 255

Si aparece después de pulsar `Ctrl+C`, la operación fue cancelada por el usuario;
no significa que FFmpeg esté mal instalado. Ejecuta de nuevo la acción y déjala
terminar. Si falla sin cancelarla, vuelve a ejecutar el instalador.

## X no muestra participantes o reproducciones

X no conserva ni publica todos los metadatos de cada Space. SpaceFlow muestra
`No disponible` cuando el proveedor no entrega un dato y recupera nombres de
hablantes únicamente cuando aparecen en los metadatos públicos.

## Todavía necesito ayuda

Abre un [issue de GitHub](https://github.com/tacosandtypescript-debug/SpaceFlow/issues)
e incluye:

- Plataforma y versión del sistema.
- Resultado de `spaceflow --version`.
- Acción realizada y mensaje de error completo.

No incluyas cookies, tokens ni datos privados.
