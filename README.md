# SpaceFlow

SpaceFlow permite consultar, escuchar, descargar y grabar X Spaces desde
a-Shell o iSH en iPhone/iPad, Termux en Android y Windows. Acepta el enlace directo
del Space o la publicación de X que contiene el botón **Reproducir grabación**.

> Usa SpaceFlow únicamente para contenido que tengas derecho a escuchar o
> conservar y respeta las condiciones de X y la legislación aplicable.

## Instalación rápida

### a-Shell, iSH y Termux

```sh
curl -fsSL https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.sh | sh
```

El instalador detecta cada terminal automáticamente. En iSH instala sus
dependencias con `apk` y aísla Python en un entorno propio. En Termux conviene
ejecutar antes `termux-setup-storage`. En a-Shell usa `~/Documents/bin`, una
ruta apropiada para comandos personales.

Las actualizaciones son incrementales: si Python, FFmpeg, curl y `yt-dlp` ya
están disponibles, el instalador no vuelve a instalarlos. Para actualizar
también las dependencias, usa `SPACEFLOW_UPDATE_DEPS=1` antes del comando.

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.ps1 | iex
```

Este comando es exclusivamente para Windows PowerShell; en iSH se usa el
comando `curl` de la sección anterior.

El instalador descarga Python y FFmpeg con `winget` cuando faltan, instala
`yt-dlp`, descarga `spaceflow.pyz` de la última Release y configura el comando.

## Primer inicio

Los Spaces públicos se pueden usar sin cookies. Si X exige iniciar sesión para
un Space concreto, importa cookies de una sesión propia en formato Netscape:

```sh
spaceflow auth import /ruta/al/cookies.txt
spaceflow
```

Las cookies se copian al directorio privado de SpaceFlow. No se suben a GitHub
ni se imprimen en pantalla. Consulta [la guía de cookies](docs/COOKIES.md).

## Uso

```sh
spaceflow info "https://x.com/usuario/status/123"
spaceflow play "https://x.com/i/spaces/1example"  # abre el stream sin descargar
spaceflow playback volume-down                    # baja el volumen en Termux
spaceflow playback pause                          # pausa el audio
spaceflow playback stop                           # detiene el audio
spaceflow download URL --format m4a
spaceflow record URL --from-start
spaceflow library list
spaceflow update --check
```

Sin argumentos se abre un menú pensado para pantallas táctiles. M4A es el
formato predeterminado porque evita conversiones innecesarias; MP3 está
disponible con `--format mp3`.

En a-Shell, `play` abre el stream en el reproductor de iOS. En Termux reproduce
el HLS mediante `mpv` y la salida OpenSL ES de Android. El menú incluye un panel
visible para pausar, continuar, detener y cambiar el volumen. Los botones físicos
de volumen del teléfono controlan el canal multimedia de Android. Al empezar a
escuchar, SpaceFlow configura automáticamente `volume-keys = volume` en Termux;
por eso esos botones dejan de funcionar como `Ctrl` y tecla especial dentro de la
terminal. iSH no expone una salida
de audio del sistema: allí puedes consultar y descargar, y después abrir el
archivo desde Archivos, o usar a-Shell para escuchar directamente.

SpaceFlow consulta GitHub cada vez que se abre y muestra un aviso cuando existe
una versión más reciente.

Al actualizar desde el menú en a-Shell, iSH o Termux, SpaceFlow vuelve a ejecutar
el instalador incremental. Así se añaden automáticamente herramientas nuevas que
falten sin reinstalar las que ya están disponibles.

## Información disponible

SpaceFlow muestra el título, anfitrión, hablantes, duración, estado y contador
cuando X los entrega. X no publica la identidad de todos los oyentes y puede
retirar metadatos cuando termina un Space; en esos casos se muestra
`No disponible` sin inventar datos.

## Desarrollo

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/build_zipapp.py
```

La arquitectura y las reglas para añadir proveedores están en
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
