"""Fresh-process check that a mismatched development override is rejected."""

import os
from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
wrong_target = (
    REPOSITORY_ROOT
    / "packages"
    / "rmc.numerics"
    / "2.2.0"
    / "lib"
    / "net9.0"
    / "Numerics.dll"
)
os.environ["NUMERICS_DLL"] = str(wrong_target)
sys.path.insert(0, str(REPOSITORY_ROOT / "notebooks"))

from helper_functions import load_numerics


try:
    load_numerics()
except RuntimeError as error:
    assert "net10.0" in str(error)
    assert ".NETCoreApp,Version=v9.0" in str(error)
    assert "restart" in str(error).lower()
    print(f"rejected={error}")
else:
    raise AssertionError("The net9.0 NUMERICS_DLL override was not rejected.")

from System import AppDomain

loaded_paths = {
    Path(str(assembly.Location)).resolve()
    for assembly in AppDomain.CurrentDomain.GetAssemblies()
    if str(assembly.Location)
}
assert wrong_target.resolve() in loaded_paths

os.environ.pop("NUMERICS_DLL")
try:
    load_numerics()
except RuntimeError as error:
    assert "already loaded" in str(error)
    assert "fresh Python process" in str(error)
    print(f"restart-required={error}")
else:
    raise AssertionError("The process accepted a different assembly after target rejection.")
