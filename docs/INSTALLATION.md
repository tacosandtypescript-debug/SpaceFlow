# Instalación

## Requisitos generales

- Conexión a Internet durante la instalación.
- Acceso a GitHub Releases y a `raw.githubusercontent.com`.
- Espacio suficiente para Python, FFmpeg, yt-dlp y, en Termux, MPV.

El instalador es incremental: conserva la configuración y evita reinstalar las
herramientas que ya están disponibles.

## Termux en Android

Usa una versión actual de Termux procedente de F-Droid o de sus publicaciones
oficiales. La versión antigua de Google Play puede tener repositorios rotos.

Si quieres guardar audios en el almacenamiento compartido, ejecuta una vez:

```sh
termux-setup-storage
```

Instala SpaceFlow:

```sh
curl -fsSL https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.sh | sh
```

El instalador añade Python, FFmpeg, curl y MPV únicamente cuando faltan. Al
escuchar por primera vez, SpaceFlow configura los botones físicos para controlar
el volumen Android.

## a-Shell en iPhone o iPad

Abre a-Shell y ejecuta:

```sh
curl -fsSL https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.sh | sh
```

SpaceFlow se instala en `~/Documents/.spaceflow/app` y crea el comando en
`~/Documents/bin`. La reproducción se abre mediante el reproductor nativo de
iOS; no se utiliza MPV.

## iSH en iPhone o iPad

Abre iSH y ejecuta:

```sh
curl -fsSL https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.sh | sh
```

El instalador usa `apk`, crea un entorno aislado de Python e instala FFmpeg.
iSH permite consultar y descargar, pero no escuchar directamente. Abre el audio
descargado desde la aplicación Archivos o utiliza a-Shell.

No uses comandos de PowerShell como `irm ... | iex` dentro de iSH.

## Windows

Abre **PowerShell**, no CMD, y ejecuta:

```powershell
irm https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.ps1 | iex
```

Si faltan, el instalador obtiene Python y FFmpeg mediante `winget`, instala
yt-dlp y añade el comando `spaceflow` al PATH del usuario. Abre una terminal
nueva al terminar.

## Comprobación

```sh
spaceflow --version
spaceflow
```

La primera línea debe mostrar la versión instalada y la segunda debe abrir el
menú.

## Actualización

SpaceFlow avisa al abrirse cuando encuentra una versión nueva. Puedes actualizar
desde la opción `U` del menú o ejecutar:

```sh
spaceflow update
```

Para volver a comprobar sin instalar:

```sh
spaceflow update --check
```

En Termux, a-Shell e iSH se vuelve a ejecutar el instalador completo de forma
incremental. Para pedir también la actualización explícita de yt-dlp:

```sh
export SPACEFLOW_UPDATE_DEPS=1
curl -fsSL https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.sh | sh
```

## Rutas utilizadas

| Plataforma | Aplicación | Comando |
|---|---|---|
| Termux | `~/.local/share/spaceflow` | `~/.local/bin/spaceflow` |
| a-Shell | `~/Documents/.spaceflow/app` | `~/Documents/bin/spaceflow` |
| iSH como root | `/root/.local/share/spaceflow` | `/usr/local/bin/spaceflow` |
| Windows | `%LOCALAPPDATA%\SpaceFlow` | `%LOCALAPPDATA%\SpaceFlow\bin\spaceflow.cmd` |

Los datos y la biblioteca se configuran por separado. Reinstalar la aplicación
no requiere volver a importar cookies mientras permanezca su directorio privado.
