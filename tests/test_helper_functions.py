import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = REPOSITORY_ROOT / "notebooks"
sys.path.insert(0, str(NOTEBOOKS_DIR))

import helper_functions


class ResolveNumericsDllTests(unittest.TestCase):
    def test_missing_override_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "Numerics.dll"
            with mock.patch.dict(os.environ, {"NUMERICS_DLL": str(missing)}, clear=True):
                with self.assertRaisesRegex(FileNotFoundError, "NUMERICS_DLL"):
                    helper_functions.resolve_numerics_dll()

    def test_exact_project_local_net10_package_is_resolved(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository_root = Path(temp_dir)
            expected = (
                repository_root
                / "packages"
                / "rmc.numerics"
                / "2.2.0"
                / "lib"
                / "net10.0"
                / "Numerics.dll"
            )
            expected.parent.mkdir(parents=True)
            expected.touch()

            with (
                mock.patch.dict(os.environ, {}, clear=True),
                mock.patch.object(
                    helper_functions, "_REPOSITORY_ROOT", repository_root, create=True
                ),
                mock.patch.object(Path, "home", return_value=repository_root / "empty-home"),
                mock.patch.object(Path, "cwd", return_value=repository_root),
            ):
                self.assertEqual(helper_functions.resolve_numerics_dll(), expected)

    def test_newer_package_does_not_replace_exact_version(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository_root = Path(temp_dir)
            wrong = (
                repository_root
                / "packages"
                / "rmc.numerics"
                / "2.2.1"
                / "lib"
                / "net10.0"
                / "Numerics.dll"
            )
            wrong.parent.mkdir(parents=True)
            wrong.touch()

            with (
                mock.patch.dict(os.environ, {}, clear=True),
                mock.patch.object(
                    helper_functions, "_REPOSITORY_ROOT", repository_root, create=True
                ),
                mock.patch.object(Path, "home", return_value=repository_root / "empty-home"),
                mock.patch.object(Path, "cwd", return_value=repository_root),
            ):
                with self.assertRaisesRegex(FileNotFoundError, "2.2.0"):
                    helper_functions.resolve_numerics_dll()


if __name__ == "__main__":
    unittest.main()
