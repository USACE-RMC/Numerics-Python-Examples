"""Fresh-process integration check for the published Numerics package."""

from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "notebooks"))

from helper_functions import load_numerics, resolve_numerics_dll


dll_path = load_numerics()
second_load_path = load_numerics()

from Numerics.Distributions import Normal
from System import AppDomain, Environment
from System.Reflection import AssemblyName


assert dll_path == resolve_numerics_dll()
assert second_load_path == dll_path
assert Environment.Version.Major == 10, Environment.Version
assert str(AssemblyName.GetAssemblyName(str(dll_path)).Version) == "2.2.0.0"
assert len([
    assembly
    for assembly in AppDomain.CurrentDomain.GetAssemblies()
    if assembly.GetName().Name == "Numerics"
]) == 1
assert Normal(0.0, 1.0).CDF(0.0) == 0.5

print(f"runtime={Environment.Version}")
print(f"assembly={AssemblyName.GetAssemblyName(str(dll_path)).Version}")
print(f"dll={dll_path}")
print("repeat-load=idempotent")
print("Normal(0,1).CDF(0)=0.5")
