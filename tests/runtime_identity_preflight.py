"""Verify wrong assembly identities are rejected before AddReference."""

import os
from pathlib import Path
import subprocess
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PROJECT = REPOSITORY_ROOT / "tests" / "fixtures" / "AssemblyFixture" / "AssemblyFixture.csproj"
FIXTURE_OUTPUT = REPOSITORY_ROOT / "artifacts" / "runtime-identity-fixtures"
FIXTURE_ASSETS = FIXTURE_PROJECT.parent / "obj" / "project.assets.json"

if not FIXTURE_ASSETS.is_file():
    raise FileNotFoundError(
        "Restore the identity fixture first with: dotnet restore "
        "tests/fixtures/AssemblyFixture/AssemblyFixture.csproj "
        "--configfile NuGet.config"
    )


def build_fixture(case, assembly_name, assembly_version):
    output = FIXTURE_OUTPUT / case
    subprocess.run(
        [
            "dotnet",
            "build",
            str(FIXTURE_PROJECT),
            "--configuration",
            "Release",
            "--no-restore",
            f"-p:FixtureAssemblyName={assembly_name}",
            f"-p:FixtureAssemblyVersion={assembly_version}",
            "--output",
            str(output),
            "--nologo",
            "--verbosity",
            "quiet",
        ],
        cwd=REPOSITORY_ROOT,
        check=True,
        timeout=120,
    )
    return output / f"{assembly_name}.dll"


def assert_rejected_before_load(dll_path, expected_message):
    child = """
import os
from pathlib import Path
import sys

repository_root = Path(os.environ['TEST_REPOSITORY_ROOT'])
sys.path.insert(0, str(repository_root / 'notebooks'))
from helper_functions import load_numerics

target = Path(os.environ['NUMERICS_DLL']).resolve()
try:
    load_numerics()
except RuntimeError as error:
    assert os.environ['TEST_EXPECTED_MESSAGE'] in str(error), error
else:
    raise AssertionError('Invalid assembly was accepted.')

from System import AppDomain
loaded_paths = {
    Path(str(assembly.Location)).resolve()
    for assembly in AppDomain.CurrentDomain.GetAssemblies()
    if str(assembly.Location)
}
assert target not in loaded_paths, f'Invalid assembly was loaded: {target}'
print(f'preflight-rejected={target.name}')
"""
    env = {
        **os.environ,
        "NUMERICS_DLL": str(dll_path),
        "TEST_REPOSITORY_ROOT": str(REPOSITORY_ROOT),
        "TEST_EXPECTED_MESSAGE": expected_message,
        "PYTHONIOENCODING": "utf-8",
    }
    subprocess.run([sys.executable, "-c", child], env=env, check=True, timeout=120)


wrong_name = build_fixture("wrong-name", "NotNumerics", "2.2.0.0")
assert_rejected_before_load(wrong_name, "contains NotNumerics 2.2.0.0")

wrong_version = build_fixture("wrong-version", "Numerics", "2.1.4.0")
assert_rejected_before_load(wrong_version, "contains Numerics 2.1.4.0")
