# Guía de uso

## Menú interactivo

Ejecuta:

```sh
spaceflow
```

El menú actual contiene:

| Opción | Acción |
|---|---|
| `1` | Ver información de un Space |
| `2` | Escuchar ahora |
| `3` | Pausar audio en Termux |
| `4` | Continuar audio en Termux |
| `5` | Bajar volumen en Termux |
| `6` | Subir volumen en Termux |
| `7` | Detener audio en Termux |
| `8` | Descargar una grabación |
| `9` | Grabar un Space en vivo |
| `B` | Ver la biblioteca |
| `C` | Importar cookies opcionales |
| `U` | Buscar actualizaciones |
| `A` | Ver la configuración |
| `0` | Salir |

Los controles `3` a `7` pertenecen al reproductor MPV de Termux. En a-Shell y
Windows se utilizan los controles del sistema operativo.

## Enlaces aceptados

Puedes pegar:

- `https://x.com/i/spaces/ID`
- `https://twitter.com/i/spaces/ID`
- Una publicación de `x.com` o `twitter.com` que incluya el Space.

Los parámetros como `?s=46` no necesitan eliminarse.

## Información

```sh
spaceflow info URL
spaceflow info URL --json
```

SpaceFlow muestra título, identificador, estado, duración, anfitrión, hablantes,
reproducciones y enlace cuando X conserva esos datos. No inventa participantes
que X no entrega públicamente.

## Escuchar

```sh
spaceflow play URL
```

- **Termux:** reproduce HLS mediante MPV en segundo plano.
- **a-Shell:** abre el reproductor nativo de iOS.
- **iSH:** no tiene salida de audio; descarga el archivo.
- **Windows:** abre el reproductor asociado por el sistema.

Controles directos de Termux:

```sh
spaceflow playback pause
spaceflow playback resume
spaceflow playback volume-down
spaceflow playback volume-up
spaceflow playback stop
```

## Descargar

```sh
spaceflow download URL
spaceflow download URL --format m4a
spaceflow download URL --format mp3
spaceflow download URL --output /ruta/de/salida
```

M4A es el formato predeterminado y suele evitar conversiones innecesarias. MP3
requiere una conversión adicional con FFmpeg.

## Grabar un directo

```sh
spaceflow record URL --from-start
spaceflow record URL --now
```

`--from-start` intenta recuperar el directo desde el comienzo. Si X no lo
permite, SpaceFlow avisa y comienza desde el punto disponible. `--now` inicia
desde el momento actual.

## Biblioteca

```sh
spaceflow library list
spaceflow library play ID_O_NOMBRE
spaceflow library delete ID_O_NOMBRE
```

Cada audio guardado tiene metadatos JSON asociados. La eliminación desde la
biblioteca borra tanto el audio como esos metadatos.

## Cookies

```sh
spaceflow auth import /ruta/cookies.txt
```

No son necesarias para Spaces públicos. Úsalas únicamente cuando X indique que
debes iniciar sesión. Consulta [COOKIES.md](COOKIES.md).

## Actualizaciones y configuración

```sh
spaceflow update --check
spaceflow update
spaceflow config show
spaceflow config set default_format m4a
spaceflow config set library_dir /ruta/biblioteca
```
