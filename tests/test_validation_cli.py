from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def test_unknown_notebook_number_is_not_a_successful_empty_validation():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_examples.py"),
         "--notebooks", "99", "--schema-only"],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode != 0
    assert "Unknown notebook numbers: 99" in result.stderr


def test_schema_check_does_not_erase_existing_execution_receipt(monkeypatch):
    import nbformat
    from scripts import validate_examples

    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        notebooks = directory / "notebooks"
        notebooks.mkdir()
        nbformat.write(nbformat.v4.new_notebook(), notebooks / "00_sample.ipynb")
        artifacts = directory / "artifacts" / "validation"
        artifacts.mkdir(parents=True)
        receipt = artifacts / "results-all.json"
        receipt.write_text('[{"status": "passed", "seconds": 12.3}]', encoding="utf-8")
        monkeypatch.setattr(validate_examples, "ROOT", directory)
        monkeypatch.setattr(sys, "argv", ["validate_examples.py", "--schema-only"])
        validate_examples.main()
        assert receipt.read_text(encoding="utf-8") == '[{"status": "passed", "seconds": 12.3}]'
