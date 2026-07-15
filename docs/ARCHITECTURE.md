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

## Extensión

Un proveedor nuevo implementa `SpaceMediaProvider`; un reproductor nuevo,
`AudioPlayer`. El dominio y la interfaz no deben importar SDKs, comandos del
sistema ni formatos de respuesta externos. Los adaptadores traducen cualquier
respuesta a `Space` y `AudioAsset`.

Los contextos funcionales son Spaces, Biblioteca, Autenticación, Actualizaciones
y Plataformas. Si crecen, pueden separarse en paquetes sin cambiar las
interfaces públicas actuales.
