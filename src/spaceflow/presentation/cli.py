from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from spaceflow import __version__
from spaceflow.bootstrap import Container, build_container
from spaceflow.domain.errors import SpaceFlowError
from spaceflow.presentation.menu import run_menu
from spaceflow.presentation.output import print_space


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="spaceflow", description="Escucha y guarda X Spaces")
    root.add_argument("--version", action="version", version=f"SpaceFlow {__version__}")
    commands = root.add_subparsers(dest="command")

    info = commands.add_parser("info", help="Mostrar información de un Space")
    info.add_argument("url")
    info.add_argument("--json", action="store_true", dest="as_json")

    play = commands.add_parser("play", help="Escuchar un Space sin descargarlo")
    play.add_argument("url")

    download = commands.add_parser("download", help="Descargar una grabación")
    download.add_argument("url")
    download.add_argument("--format", choices=("m4a", "mp3"), default=None)
    download.add_argument("--output", type=Path)

    record = commands.add_parser("record", help="Grabar un Space en vivo")
    record.add_argument("url")
    start = record.add_mutually_exclusive_group()
    start.add_argument("--from-start", action="store_true", default=True)
    start.add_argument("--now", action="store_false", dest="from_start")
    record.add_argument("--format", choices=("m4a", "mp3"), default=None)
    record.add_argument("--output", type=Path)

    auth = commands.add_parser("auth", help="Administrar cookies")
    auth_sub = auth.add_subparsers(dest="auth_command", required=True)
    auth_import = auth_sub.add_parser("import", help="Importar cookies Netscape")
    auth_import.add_argument("file", type=Path)

    library = commands.add_parser("library", help="Administrar biblioteca")
    library_sub = library.add_subparsers(dest="library_command", required=True)
    library_sub.add_parser("list")
    library_play = library_sub.add_parser("play")
    library_play.add_argument("query")
    library_delete = library_sub.add_parser("delete")
    library_delete.add_argument("query")

    config = commands.add_parser("config", help="Ver o modificar configuración")
    config_sub = config.add_subparsers(dest="config_command", required=True)
    config_sub.add_parser("show")
    config_set = config_sub.add_parser("set")
    config_set.add_argument("key", choices=("library_dir", "default_format"))
    config_set.add_argument("value")

    update = commands.add_parser("update", help="Buscar o instalar actualizaciones")
    update.add_argument("--check", action="store_true", help="Solo comprobar")
    return root


def _asset(container: Container, query: str):
    matches = [
        item
        for item in container.library.list_assets()
        if query in {item.space_id.value, item.path.name, str(item.path)}
    ]
    if not matches:
        raise SpaceFlowError("No se encontró ese audio en la biblioteca")
    return matches[0]


def _notice_update(container: Container) -> None:
    release = container.updates.check(force=False)
    if release:
        print(
            f"Aviso: SpaceFlow {release.version} está disponible. "
            "Ejecuta 'spaceflow update' para instalarla.",
            file=sys.stderr,
        )


def execute(args: argparse.Namespace, container: Container) -> int:
    command = args.command
    if command != "update":
        _notice_update(container)
    if not command:
        return run_menu(container)
    audio_format = getattr(args, "format", None) or container.config.default_format
    if command == "info":
        space = container.service.info(args.url)
        if args.as_json:
            print(json.dumps(space.to_dict(), ensure_ascii=False, indent=2))
        else:
            print_space(space)
    elif command == "play":
        container.service.play_url(args.url)
        print("Reproductor abierto. Usa 'download' si también quieres guardar el audio.")
    elif command in {"download", "record"}:
        from_start = getattr(args, "from_start", True)
        asset, fallback = container.service.download(
            args.url, audio_format, args.output, live_from_start=from_start
        )
        print(asset.path)
        if fallback:
            print("Aviso: X no permitió empezar desde el inicio; se grabó desde el momento actual.")
    elif command == "auth":
        print(container.cookies.import_file(args.file))
    elif command == "library":
        if args.library_command == "list":
            for item in container.library.list_assets():
                print(f"{item.space_id.value}\t{item.format}\t{item.path}")
        elif args.library_command == "play":
            container.service.play_asset(_asset(container, args.query))
        elif args.library_command == "delete":
            if not container.library.delete(args.query):
                raise SpaceFlowError("No se encontró ese audio en la biblioteca")
            print("Audio y metadatos eliminados.")
    elif command == "config":
        if args.config_command == "show":
            print(json.dumps(container.config_store.public_dict(), ensure_ascii=False, indent=2))
        else:
            container.config_store.set_value(args.key, args.value)
            print("Configuración guardada. Se aplicará en el próximo inicio.")
    elif command == "update":
        release = container.updates.check(force=True)
        if not release:
            print("Ya tienes la versión más reciente o GitHub no está disponible.")
        elif args.check:
            print(f"Disponible: {release.version}\n{release.page_url}")
        else:
            print(f"Nueva versión: {release.version}")
            answer = input("¿Instalar ahora? [s/N]: ").strip().lower()
            if answer in {"s", "si", "sí", "y", "yes"}:
                container.updates.install(release)
                print("Actualización instalada. Reinicia SpaceFlow.")
            else:
                print("Actualización cancelada.")
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        return execute(args, build_container())
    except SpaceFlowError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nOperación cancelada.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
