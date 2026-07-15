from __future__ import annotations

import json
from pathlib import Path

from spaceflow.bootstrap import Container
from spaceflow.domain.errors import SpaceFlowError
from spaceflow.presentation.output import print_space
from spaceflow.presentation.style import (
    BOLD,
    BRIGHT_CYAN,
    CYAN,
    DIM,
    GREEN,
    RED,
    YELLOW,
    error,
    paint,
    success,
    warning,
)


def _ask(prompt: str) -> str:
    return input(paint(prompt, BOLD, CYAN)).strip()


def _option(number: str, label: str, color: str) -> None:
    print(f"  {paint(number, BOLD, color)}  {label}")


def _draw_menu() -> None:
    print()
    print(paint("╭────────────────────────────╮", BRIGHT_CYAN))
    print(paint("│       ◆  SPACEFLOW         │", BOLD, BRIGHT_CYAN))
    print(paint("╰────────────────────────────╯", BRIGHT_CYAN))
    print(paint("  ESCUCHAR Y GUARDAR", BOLD, DIM, CYAN))
    _option("1", "Ver información de un Space", GREEN)
    _option("2", "Escuchar ahora", GREEN)
    _option("3", "Descargar grabación", GREEN)
    _option("4", "Grabar un Space en vivo", GREEN)
    _option("5", "Ver biblioteca", GREEN)
    print(paint("  HERRAMIENTAS", BOLD, DIM, YELLOW))
    _option("6", "Importar cookies de X (opcional)", YELLOW)
    _option("7", "Buscar actualizaciones", YELLOW)
    _option("8", "Configuración", YELLOW)
    _option("0", "Salir", RED)


def run_menu(container: Container) -> int:
    while True:
        _draw_menu()
        try:
            choice = _ask("\nElige una opción: ")
            if choice == "0":
                return 0
            if choice == "1":
                print_space(container.service.info(_ask("Pega el enlace: ")))
            elif choice == "2":
                container.service.play_url(_ask("Pega el enlace: "))
                print(success("Reproductor abierto. Para guardar el audio usa la opción 3."))
            elif choice == "3":
                url = _ask("Pega el enlace: ")
                audio_format = _ask("Formato [m4a/mp3] (m4a): ").lower() or "m4a"
                asset, fallback = container.service.download(url, audio_format)
                print(success(f"Descarga terminada: {asset.path}"))
                if fallback:
                    print(warning("X no permitió empezar desde el inicio; se capturó desde el momento disponible."))
            elif choice == "4":
                url = _ask("Pega el enlace del directo: ")
                asset, fallback = container.service.download(url, container.config.default_format, live_from_start=True)
                print(success(f"Grabación guardada: {asset.path}"))
                if fallback:
                    print(warning("La grabación comenzó desde el momento actual."))
            elif choice == "5":
                assets = container.library.list_assets()
                if not assets:
                    print(warning("La biblioteca está vacía."))
                for index, asset in enumerate(assets, 1):
                    print(f"{index}. {asset.path.name}")
            elif choice == "6":
                destination = container.cookies.import_file(Path(_ask("Ruta de cookies.txt: ")))
                print(success(f"Cookies protegidas en: {destination}"))
            elif choice == "7":
                release = container.updates.check(force=True)
                if not release:
                    print(success("Ya tienes la versión más reciente."))
                else:
                    print(warning(f"Nueva versión disponible: {release.version}"))
                    if _ask("¿Actualizar ahora? [s/N]: ").lower() in {"s", "si", "sí", "y", "yes"}:
                        container.updates.install(release)
                        print(success("Actualización instalada. Reinicia SpaceFlow."))
            elif choice == "8":
                print(json.dumps(container.config_store.public_dict(), ensure_ascii=False, indent=2))
            else:
                print(warning("Opción no válida."))
        except (EOFError, KeyboardInterrupt):
            print("\n" + warning("Operación cancelada."))
            return 130
        except SpaceFlowError as exc:
            print(error(exc))
        except ValueError as exc:
            print(error(exc))
