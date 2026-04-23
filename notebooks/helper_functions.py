"""Helper functions used by notebooks in this repository."""

import math
import os
from pathlib import Path

import pandas as pd


def resolve_numerics_dll():
    """Return the path to the Numerics .NET DLL.

    Resolution order:
      1. NUMERICS_DLL environment variable (explicit override)
      2. Global NuGet cache: ~/.nuget/packages/rmc.numerics/*/lib/net8.0/Numerics.dll
         (populated by `dotnet add package RMC.Numerics`)
      3. Local packages folder: ./packages/RMC.Numerics.*/lib/net8.0/Numerics.dll
         (populated by `nuget install RMC.Numerics -OutputDirectory packages`)

    Raises FileNotFoundError with install instructions if none of these resolve.
    """
    env = os.environ.get("NUMERICS_DLL")
    if env:
        return Path(env)

    cache = Path.home() / ".nuget" / "packages" / "rmc.numerics"
    if cache.exists():
        hits = sorted(cache.glob("*/lib/net8.0/Numerics.dll"), reverse=True)
        if hits:
            return hits[0]

    for search_root in (Path.cwd(), Path.cwd().parent):
        local = sorted(
            (search_root / "packages").glob("RMC.Numerics.*/lib/net8.0/Numerics.dll"),
            reverse=True,
        )
        if local:
            return local[0]

    raise FileNotFoundError(
        "Numerics DLL not found. Install via one of:\n"
        "  dotnet add package RMC.Numerics --version 2.0.1\n"
        "  nuget install RMC.Numerics -Version 2.0.1 -OutputDirectory packages\n"
        "Or set the NUMERICS_DLL environment variable to a local build."
    )


def convert_to_dotnet_array(python_list):
    """Convert a Python list into a 1D .NET array of doubles.

    Requires that the Numerics .NET runtime has already been loaded
    (i.e., clr.AddReference has been called).
    """
    from System import Array, Double

    dotnet_array = Array.CreateInstance(Double, len(python_list))
    for i, val in enumerate(python_list):
        dotnet_array[i] = float(val)
    return dotnet_array


def convert_to_dotnet_2d_array(matrix):
    """Convert a 2D NumPy array into a .NET 2D array of doubles.

    Requires that the Numerics .NET runtime has already been loaded
    (i.e., clr.AddReference has been called).
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
