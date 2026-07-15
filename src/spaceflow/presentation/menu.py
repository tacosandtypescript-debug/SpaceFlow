from __future__ import annotations

import json
from pathlib import Path

from spaceflow.bootstrap import Container
from spaceflow.domain.errors import SpaceFlowError
from spaceflow.presentation.output import print_space


def _ask(prompt: str) -> str:
    return input(prompt).strip()


def run_menu(container: Container) -> int:
    while True:
        print("\n╭──────────────────────────╮")
        print("│       SpaceFlow          │")
        print("╰──────────────────────────╯")
        print("1. Ver información de un Space")
        print("2. Escuchar ahora (sin descargar)")
        print("3. Descargar")
        print("4. Grabar un Space en vivo")
        print("5. Ver biblioteca")
        print("6. Importar cookies de X (opcional)")
        print("7. Buscar actualizaciones")
        print("8. Configuración")
        print("0. Salir")
        try:
            choice = _ask("\nElige una opción: ")
            if choice == "0":
                return 0
            if choice == "1":
                print_space(container.service.info(_ask("Pega el enlace: ")))
            elif choice == "2":
                container.service.play_url(_ask("Pega el enlace: "))
                print("Reproductor abierto. Para guardar el audio usa la opción 3.")
            elif choice == "3":
                url = _ask("Pega el enlace: ")
                audio_format = _ask("Formato [m4a/mp3] (m4a): ").lower() or "m4a"
                asset, fallback = container.service.download(url, audio_format)
                print(f"Descarga terminada: {asset.path}")
                if fallback:
                    print("X no permitió empezar desde el inicio; se capturó desde el momento disponible.")
            elif choice == "4":
                url = _ask("Pega el enlace del directo: ")
                asset, fallback = container.service.download(url, container.config.default_format, live_from_start=True)
                print(f"Grabación guardada: {asset.path}")
                if fallback:
                    print("La grabación comenzó desde el momento actual.")
            elif choice == "5":
                assets = container.library.list_assets()
                if not assets:
                    print("La biblioteca está vacía.")
                for index, asset in enumerate(assets, 1):
                    print(f"{index}. {asset.path.name}")
            elif choice == "6":
                destination = container.cookies.import_file(Path(_ask("Ruta de cookies.txt: ")))
                print(f"Cookies protegidas en: {destination}")
            elif choice == "7":
                release = container.updates.check(force=True)
                if not release:
                    print("Ya tienes la versión más reciente.")
                else:
                    print(f"Nueva versión disponible: {release.version}")
                    if _ask("¿Actualizar ahora? [s/N]: ").lower() in {"s", "si", "sí", "y", "yes"}:
                        container.updates.install(release)
                        print("Actualización instalada. Reinicia SpaceFlow.")
            elif choice == "8":
                print(json.dumps(container.config_store.public_dict(), ensure_ascii=False, indent=2))
            else:
                print("Opción no válida.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada.")
            return 130
        except SpaceFlowError as exc:
            print(f"Error: {exc}")
        except ValueError as exc:
            print(f"Error: {exc}")
