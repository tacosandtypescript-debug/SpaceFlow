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
spaceflow play "https://x.com/i/spaces/1example"
spaceflow download URL --format m4a
spaceflow record URL --from-start
spaceflow library list
spaceflow update --check
```

Sin argumentos se abre un menú pensado para pantallas táctiles. M4A es el
formato predeterminado porque evita conversiones innecesarias; MP3 está
disponible con `--format mp3`.

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
