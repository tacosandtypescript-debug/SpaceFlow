# Arquitectura

SpaceFlow sigue Domain-Driven Design en una escala apropiada para una CLI.

## Capas

- `domain`: entidades, value objects y errores. No importa infraestructura.
- `application`: casos de uso y puertos (`Protocol`).
- `infrastructure`: adaptadores de X/yt-dlp, almacenamiento, reproducción y GitHub.
- `presentation`: CLI, menú y representación de resultados.
- `bootstrap`: composición e inyección de dependencias.

El flujo principal es:

```text
CLI/Menu -> SpaceFlowService -> puertos de aplicación
                               |-> XSpaceUrlResolver
                               |-> YtDlpSpaceProvider
                               |-> JsonLibraryRepository
                               |-> SystemAudioPlayer
```

`SystemAudioPlayer` selecciona el comportamiento según la plataforma. En
Termux administra MPV, su socket de control y su proceso; en a-Shell delega la
reproducción al sistema iOS. `GitHubReleaseRepository` consulta Releases y, en
plataformas móviles, ejecuta el instalador incremental para incorporar nuevas
dependencias además del archivo `spaceflow.pyz`.

## Extensión

Un proveedor nuevo implementa `SpaceMediaProvider`; un reproductor nuevo,
`AudioPlayer`. El dominio y la interfaz no deben importar SDKs, comandos del
sistema ni formatos de respuesta externos. Los adaptadores traducen cualquier
respuesta a `Space` y `AudioAsset`.

Los contextos funcionales son Spaces, Reproducción, Biblioteca, Autenticación,
Actualizaciones y Plataformas. Si crecen, pueden separarse en paquetes sin
cambiar las interfaces públicas actuales.

## Reglas de dependencia

- `domain` no conoce yt-dlp, MPV, GitHub ni el sistema de archivos.
- `application` define los puertos y coordina casos de uso.
- `infrastructure` traduce herramientas externas a los modelos del dominio.
- `presentation` no ejecuta comandos del sistema directamente.
- `bootstrap` es el único lugar que construye y conecta los adaptadores.

Los detalles de instalación y uso pertenecen a
[INSTALLATION.md](INSTALLATION.md) y [USAGE.md](USAGE.md), no a las entidades del
dominio.
