"""Execute each notebook's shared-loader setup cell in a fresh process."""

import json
import os
from pathlib import Path
import subprocess
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = REPOSITORY_ROOT / "notebooks"

for notebook_path in sorted(NOTEBOOKS_DIR.glob("*.ipynb")):
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    setup_cells = [
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
        and "load_numerics" in "".join(cell.get("source", []))
    ]
    if len(setup_cells) != 1:
        raise AssertionError(
            f"{notebook_path.name}: expected one shared-loader setup cell, "
            f"found {len(setup_cells)}"
        )
    subprocess.run(
        [sys.executable, "-c", setup_cells[0]],
        cwd=NOTEBOOKS_DIR,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=True,
        timeout=120,
    )
    print(f"setup-ok={notebook_path.name}")
