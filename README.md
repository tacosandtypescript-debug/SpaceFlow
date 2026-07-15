# SpaceFlow

SpaceFlow es una herramienta de Python para consultar, escuchar, descargar y
grabar X Spaces desde **Termux**, **a-Shell**, **iSH** y **Windows**. Acepta el
enlace directo de un Space o la publicación de X que contiene la grabación.

> Utiliza SpaceFlow únicamente con contenido que tengas derecho a escuchar o
> conservar. Respeta las condiciones de X y la legislación aplicable.

## Instalar desde la app móvil de GitHub

Toca el botón correspondiente a tu dispositivo. Se abrirá una página preparada
para el móvil donde podrás copiar el comando completo con un solo toque.

### iPhone o iPad · a-Shell/iSH

[![Copiar para Apple](https://img.shields.io/badge/APPLE-COPIAR_PARA_a--SHELL_O_iSH-0a84ff?style=for-the-badge&logo=apple&logoColor=white)](https://tacosandtypescript-debug.github.io/SpaceFlow/?device=apple)

### Android · Termux

[![Copiar para Android](https://img.shields.io/badge/ANDROID-COPIAR_PARA_TERMUX-3ddc84?style=for-the-badge&logo=android&logoColor=111111)](https://tacosandtypescript-debug.github.io/SpaceFlow/?device=android)

Si la app de GitHub no abre los botones, mantén pulsado este bloque y copia el
comando manualmente:

```sh
curl -fsSL https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.sh | sh
```

Después ejecuta `spaceflow`. El instalador reconoce automáticamente cuál de
los tres sistemas estás usando.

## Compatibilidad

| Plataforma | Información | Escuchar | Descargar/grabar | Control del audio |
|---|---:|---:|---:|---|
| Termux (Android) | Sí | Sí | Sí | Menú, comandos y botones físicos |
| a-Shell (iOS/iPadOS) | Sí | Sí | Sí | Reproductor y botones de iOS |
| iSH (iOS/iPadOS) | Sí | No | Sí | Abrir después desde Archivos |
| Windows | Sí | Sí | Sí | Reproductor de Windows |

iSH no expone una salida de audio del sistema. En iPhone y iPad se recomienda
**a-Shell** para escuchar directamente.

## Instalación rápida

### Termux, a-Shell o iSH

```sh
curl -fsSL https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.sh | sh
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/tacosandtypescript-debug/SpaceFlow/main/scripts/install.ps1 | iex
```

Comprueba la instalación:

```sh
spaceflow --version
spaceflow
```

El instalador detecta la plataforma, instala únicamente las dependencias que
faltan y descarga la versión estable más reciente con verificación SHA-256.
Consulta la [guía de instalación](docs/INSTALLATION.md) para requisitos,
actualización y pasos específicos de cada sistema.

## Uso rápido

Sin argumentos se abre el menú interactivo:

```sh
spaceflow
```

También puedes utilizar comandos directos:

```sh
spaceflow info "https://x.com/usuario/status/123"
spaceflow play "https://x.com/i/spaces/1example"
spaceflow download URL --format m4a
spaceflow record URL --from-start
spaceflow library list
spaceflow update --check
```

En Termux también están disponibles:

```sh
spaceflow playback pause
spaceflow playback resume
spaceflow playback volume-down
spaceflow playback volume-up
spaceflow playback stop
```

Al comenzar a escuchar en Termux, SpaceFlow configura `volume-keys = volume`
para que los botones físicos controlen el volumen multimedia de Android. Esos
botones dejan de actuar como `Ctrl` y tecla especial dentro de Termux.

En a-Shell, el audio se abre en el reproductor nativo de iOS. El volumen, la
pausa y la reproducción se controlan con los botones físicos, el Centro de
control o la pantalla bloqueada.

Lee la [guía de uso](docs/USAGE.md) para conocer todas las opciones del menú,
los formatos y los controles disponibles por plataforma.

## Cookies

Los Spaces públicos funcionan sin cookies. Solo necesitas importarlas si X
exige iniciar sesión para un Space concreto:

```sh
spaceflow auth import /ruta/cookies.txt
```

SpaceFlow guarda el archivo localmente, con permisos privados cuando el sistema
lo permite, y nunca lo sube al repositorio. Consulta la
[guía de cookies](docs/COOKIES.md).

## Actualizaciones

SpaceFlow comprueba si existe una versión nueva cada vez que se abre. Para
actualizar manualmente:

```sh
spaceflow update
```

En Termux, a-Shell e iSH la actualización ejecuta el instalador incremental para
incorporar también cualquier dependencia nueva.

## Ayuda y enlaces

- [Última versión estable](https://github.com/tacosandtypescript-debug/SpaceFlow/releases/latest)
- [Todas las versiones](https://github.com/tacosandtypescript-debug/SpaceFlow/releases)
- [Reportar un problema](https://github.com/tacosandtypescript-debug/SpaceFlow/issues)
- [Instalación detallada](docs/INSTALLATION.md)
- [Guía de uso](docs/USAGE.md)
- [Solución de problemas](docs/TROUBLESHOOTING.md)
- [Arquitectura DDD](docs/ARCHITECTURE.md)
- [Seguridad](SECURITY.md)
- [Cambios por versión](CHANGELOG.md)
- [Licencia MIT](LICENSE)

## Desarrollo

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/build_zipapp.py
```

SpaceFlow requiere Python 3.9 o superior. Las contribuciones deben conservar la
separación entre dominio, aplicación, infraestructura y presentación descrita
en la [arquitectura](docs/ARCHITECTURE.md).
