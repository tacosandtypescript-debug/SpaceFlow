from __future__ import annotations

import argparse
import shutil
import tempfile
import zipapp
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build(output: Path) -> Path:
    source = ROOT / "src" / "spaceflow"
    if not source.is_dir():
        raise SystemExit("No se encontró src/spaceflow")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="spaceflow-build-") as directory:
        stage = Path(directory)
        shutil.copytree(source, stage / "spaceflow")
        zipapp.create_archive(
            stage,
            target=output,
            interpreter="/usr/bin/env python3",
            main="spaceflow.presentation.cli:main",
            compressed=True,
        )
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "spaceflow.pyz")
    args = parser.parse_args()
    print(build(args.output))
