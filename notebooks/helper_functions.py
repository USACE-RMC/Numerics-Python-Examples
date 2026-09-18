"""Helper functions used by notebooks in this repository."""

import math
import os
from pathlib import Path


NUMERICS_PACKAGE_VERSION = "2.2.0"
NUMERICS_ASSEMBLY_VERSION = "2.2.0.0"
NUMERICS_TARGET_FRAMEWORK = ".NETCoreApp,Version=v10.0"
_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_RUNTIME_CONFIG = _REPOSITORY_ROOT / "dotnet" / "numerics.runtimeconfig.json"


def _package_dll():
    return (
        _REPOSITORY_ROOT
        / "packages"
        / "rmc.numerics"
        / NUMERICS_PACKAGE_VERSION
        / "lib"
        / "net10.0"
        / "Numerics.dll"
    )


def resolve_numerics_dll():
    """Return the exact Numerics 2.2.0 net10.0 DLL path.

    Resolution order:
      1. NUMERICS_DLL environment variable (explicit development override)
      2. The repository-local package restored by the checked-in .NET project

    Assembly identity/version preflight and target-framework validation happen
    in load_numerics() after the explicitly configured CoreCLR has started.
    """
    env = os.environ.get("NUMERICS_DLL")
    if env:
        override = Path(env).expanduser().resolve()
        if not override.is_file():
            raise FileNotFoundError(
                f"NUMERICS_DLL does not point to a file: {override}"
            )
        return override

    package_dll = _package_dll()
    if package_dll.is_file():
        return package_dll

    raise FileNotFoundError(
        f"RMC.Numerics {NUMERICS_PACKAGE_VERSION} net10.0 DLL not found at "
        f"{package_dll}. Restore the exact package from the repository root with:\n"
        "  dotnet restore dotnet/NumericsRuntime.csproj "
        "--configfile NuGet.config --no-cache\n"
        "Alternatively set NUMERICS_DLL to a net10.0 development build of "
        f"Numerics {NUMERICS_ASSEMBLY_VERSION}."
    )


def _target_framework(assembly):
    """Return an assembly's TargetFrameworkAttribute value, if present."""
    for attribute in assembly.GetCustomAttributesData():
        if (
            attribute.AttributeType.FullName
            == "System.Runtime.Versioning.TargetFrameworkAttribute"
        ):
            return str(attribute.ConstructorArguments[0].Value)
    return None


def _validate_numerics_identity(identity, dll_path):
    """Validate assembly metadata before loading the candidate DLL."""
    version = str(identity.Version)
    if identity.Name != "Numerics" or version != NUMERICS_ASSEMBLY_VERSION:
        raise RuntimeError(
            f"Expected Numerics assembly version {NUMERICS_ASSEMBLY_VERSION}, "
            f"but {dll_path} contains {identity.Name} {version}."
        )


def _validate_numerics_assembly(assembly, dll_path):
    """Validate the target framework of the loaded Numerics assembly."""
    target_framework = _target_framework(assembly)
    if target_framework != NUMERICS_TARGET_FRAMEWORK:
        raise RuntimeError(
            f"Expected a net10.0 Numerics assembly ({NUMERICS_TARGET_FRAMEWORK}), "
            f"but {dll_path} targets {target_framework or 'an unknown framework'}. "
            "Target-framework metadata is available only after loading; this process "
            "now contains the rejected assembly. Restart Python before loading Numerics."
        )


def load_numerics():
    """Start .NET 10 explicitly, validate, and load Numerics 2.2.0.

    Returns the resolved DLL path for provenance and diagnostics. Calling this
    function repeatedly in the same process is safe when the same assembly is
    already loaded.
    """
    dll_path = resolve_numerics_dll()
    if not _RUNTIME_CONFIG.is_file():
        raise FileNotFoundError(f".NET runtime configuration not found: {_RUNTIME_CONFIG}")

    import pythonnet

    pythonnet.load("coreclr", runtime_config=str(_RUNTIME_CONFIG))

    from System import AppDomain, Environment
    from System.Reflection import AssemblyName

    if Environment.Version.Major != 10:
        raise RuntimeError(
            f"Expected .NET 10 CoreCLR, but the active runtime is {Environment.Version}. "
            "Start a fresh Python process and call load_numerics() before importing clr."
        )

    requested_identity = AssemblyName.GetAssemblyName(str(dll_path))
    _validate_numerics_identity(requested_identity, dll_path)

    loaded = [
        assembly
        for assembly in AppDomain.CurrentDomain.GetAssemblies()
        if assembly.GetName().Name == "Numerics"
    ]
    if loaded:
        assembly = loaded[0]
        loaded_path = Path(str(assembly.Location)).resolve()
        if loaded_path != dll_path.resolve():
            raise RuntimeError(
                f"Numerics is already loaded from {loaded_path}; requested {dll_path}. "
                "Start a fresh Python process to change assemblies."
            )
    else:
        import clr

        assembly = clr.AddReference(str(dll_path))

    _validate_numerics_assembly(assembly, dll_path)
    return dll_path


def convert_to_dotnet_array(python_list):
    """Convert a Python list into a 1D .NET array of doubles.

    Requires that load_numerics() has already been called.
    """
    from System import Array, Double

    dotnet_array = Array.CreateInstance(Double, len(python_list))
    for i, val in enumerate(python_list):
        dotnet_array[i] = float(val)
    return dotnet_array


def convert_to_dotnet_2d_array(matrix):
    """Convert a 2D NumPy array into a .NET 2D array of doubles.

    Requires that load_numerics() has already been called.
    """
    from System import Array, Double

    rows, cols = matrix.shape
    net_array = Array.CreateInstance(Double, rows, cols)
    for i in range(rows):
        for j in range(cols):
            net_array[i, j] = float(matrix[i, j])
    return net_array


def create_comparison_table(
    numerics_results,
    comparison_package,
    comparison_results,
    parameter_names,
    numerics_time=float("nan"),
    comparison_time=float("nan"),
):
    """Create a comparison table between Numerics and another package."""
    import pandas as pd

    table = []
    for i, param_name in enumerate(parameter_names):
        pct_diff = (
            (numerics_results[i] - comparison_results[i]) / comparison_results[i] * 100
            if comparison_results[i] != 0
            else 0
        )
        table.append(
            {
                "Parameter": param_name,
                "Numerics Result": numerics_results[i],
                f"{comparison_package} Result": comparison_results[i],
                "Difference": f"{pct_diff:.4f}%",
            }
        )

    if not math.isnan(numerics_time) and not math.isnan(comparison_time):
        time_diff = (numerics_time - comparison_time) if comparison_time != 0 else 0
        table.append(
            {
                "Parameter": "Runtime (secs)",
                "Numerics Result": f"{numerics_time:.4f}",
                f"{comparison_package} Result": f"{comparison_time:.4f}",
                "Difference": f"{time_diff:.4f}",
            }
        )

    return pd.DataFrame(table)
