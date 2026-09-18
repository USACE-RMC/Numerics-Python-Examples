"""Execute notebooks in fresh kernels and scripts in separate processes.

Run with the repository virtual environment. Executed copies and logs go to
ignored artifacts/. The --update-outputs switch copies only generated code-cell
outputs, execution counts, and kernel-reported language metadata into the
explicitly selected notebooks.
"""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import nbformat
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpec
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


class EnvironmentKernelManager(KernelManager):
    """Use this validator's Python without changing the user's kernel registry."""

    @property
    def kernel_spec(self):
        return KernelSpec(argv=[sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                          display_name="Validation Python", language="python")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebooks", nargs="*", help="Notebook numbers such as 00 05 11; defaults to all")
    parser.add_argument("--scripts", action="store_true", help="Also execute all three standalone scripts")
    parser.add_argument("--update-outputs", action="store_true", help="Retain outputs for selected notebooks")
    parser.add_argument("--schema-only", action="store_true")
    args = parser.parse_args()
    artifacts = ROOT / "artifacts" / "validation"
    artifacts.mkdir(parents=True, exist_ok=True)
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if args.notebooks is not None:
        unknown = set(args.notebooks) - {p.name[:2] for p in notebooks}
        if unknown:
            parser.error("Unknown notebook numbers: " + ", ".join(sorted(unknown)))
        notebooks = [p for p in notebooks if p.name[:2] in args.notebooks]
    results = []
    for path in notebooks:
        original = json.loads(path.read_text(encoding="utf-8"))
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        if args.schema_only:
            print(f"SCHEMA PASS {path.name}", flush=True)
            continue
        print(f"RUN {path.name}", flush=True)
        for cell in nb.cells:
            cell.metadata.pop("execution", None)
        start = time.perf_counter()
        client = NotebookClient(nb, timeout=1800, kernel_manager_class=EnvironmentKernelManager,
                                resources={"metadata": {"path": str(path.parent)}},
                                record_timing=False, allow_errors=False,
                                on_cell_start=lambda cell, cell_index: print(
                                    f"  CELL {cell_index}: {cell.cell_type}", flush=True))
        try:
            client.execute(env=dict(os.environ, IPYTHONDIR=str(artifacts / "ipython")))
        except Exception:
            nbformat.write(nb, artifacts / path.name)
            raise
        elapsed = time.perf_counter() - start
        nbformat.validate(nb)
        nbformat.write(nb, artifacts / path.name)
        if args.update_outputs:
            original["metadata"]["language_info"] = nb.metadata["language_info"]
            for before, after in zip(original["cells"], nb.cells, strict=True):
                if before["cell_type"] == "code":
                    before["metadata"].pop("execution", None)
                    before["outputs"] = after.outputs
                    before["execution_count"] = after.execution_count
            path.write_text(json.dumps(original, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        results.append({"file": path.name, "seconds": elapsed, "status": "passed"})
        print(f"PASS {path.name} ({elapsed:.1f}s)", flush=True)
    if args.schema_only and not args.scripts:
        return  # Structural checks must not replace execution evidence with [].
    if args.scripts:
        for path in sorted((ROOT / "examples").glob("*.py")):
            start = time.perf_counter()
            env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
            completed = subprocess.run([sys.executable, str(path)], cwd=ROOT, env=env,
                                       capture_output=True, text=True, encoding="utf-8", timeout=1800)
            (artifacts / (path.stem + ".log")).write_text(completed.stdout + completed.stderr, encoding="utf-8")
            if completed.returncode:
                raise RuntimeError(f"{path.name} failed; see artifacts/validation/{path.stem}.log")
            elapsed = time.perf_counter() - start
            results.append({"file": path.name, "seconds": elapsed, "status": "passed"})
            print(f"PASS {path.name} ({elapsed:.1f}s)", flush=True)
    name = "results-" + ("-".join(args.notebooks) if args.notebooks else "all") + ".json"
    (artifacts / name).write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
