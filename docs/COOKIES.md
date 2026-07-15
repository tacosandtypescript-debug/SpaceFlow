# Exportar cookies de X

Las cookies son opcionales para los Spaces públicos. Si X exige iniciar sesión
para un Space concreto, SpaceFlow recibe un archivo Netscape `cookies.txt` de
una sesión propia y lo usa localmente para obtener el audio y los metadatos.

1. Exporta únicamente las cookies de `x.com`/`twitter.com` con una herramienta
   de confianza.
2. Transfiere el archivo al dispositivo sin publicarlo ni enviarlo por chats.
3. Ejecuta `spaceflow auth import /ruta/cookies.txt`.
4. Borra la copia original si ya no la necesitas.

En iOS no se extraen cookies automáticamente. En Android y Windows también se
prefiere la importación explícita para no acceder silenciosamente al perfil del
navegador. Si X responde que la sesión caducó, exporta un archivo nuevo.

Comprueba que el archivo comienza con una cabecera Netscape válida y nunca lo
añadas al repositorio. SpaceFlow copia únicamente el archivo que indiques; no
lee automáticamente cookies de Safari, Chrome, Firefox ni otras aplicaciones.

Para errores que no estén relacionados con autenticación, consulta
[TROUBLESHOOTING.md](TROUBLESHOOTING.md).
