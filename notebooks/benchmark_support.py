"""Shared provenance and chain-aware reporting for the release benchmarks."""

import importlib.metadata
import os
import platform
import subprocess
import time

import numpy as np
import pandas as pd


def environment_table():
    """Describe the process which produced a timing table (load Numerics first)."""
    from System import Environment
    from System.Reflection import AssemblyName
    from helper_functions import resolve_numerics_dll

    dll = resolve_numerics_dll()
    rows = {
        "Python": platform.python_version(),
        "OS": platform.platform(),
        "CPU": platform.processor() or platform.machine(),
        "Logical CPUs": os.cpu_count(),
        ".NET runtime": str(Environment.Version),
        "Numerics assembly": str(AssemblyName.GetAssemblyName(str(dll)).Version),
        "Numerics package": "RMC.Numerics 2.2.0 (net10.0)",
        "Assembly source": "NUMERICS_DLL override" if os.environ.get("NUMERICS_DLL") else "restored NuGet package",
        "UTC run time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
    }
    for package in ("pythonnet", "numpy", "pandas", "scipy", "pymc", "pytensor", "arviz", "scikit-learn"):
        rows[package] = importlib.metadata.version(package)
    from pytensor import config
    rows["PyTensor C++ compiler"] = "configured" if config.cxx else "unavailable (Python fallback)"
    rows["PyTensor BLAS flags"] = config.blas__ldflags or "none configured"
    rows[".NET SDK"] = subprocess.check_output(
        ["dotnet", "--version"], text=True, timeout=30
    ).strip()
    return pd.DataFrame(rows.items(), columns=["Component", "Version / value"])


def posterior_chains(sampler):
    """Return [chain, draw, parameter], including all post-warmup transitions.

    MarkovChains includes warmup; Output is a separate later sampling phase.
    With thinning=1, combining both retained segments avoids hiding sampling work.
    """
    if sampler.ThinningInterval != 1:
        raise ValueError("The benchmark requires ThinningInterval=1.")
    return np.asarray([
        [list(state.Values) for state in list(chain)[sampler.WarmupIterations:]]
        + [list(state.Values) for state in sampler.Output[index]]
        for index, chain in enumerate(sampler.MarkovChains)
    ], dtype=float)


def posterior_diagnostics(chains, names):
    """Compute identical rank-based diagnostics for each backend with ArviZ.

    The conservative ESS is min(bulk, tail); ArviZ tail is the minimum of
    lower/upper quantile ESS. Do not flatten chains before these calculations.
    """
    import arviz as az

    chains = np.asarray(chains, dtype=float)
    if chains.ndim != 3 or chains.shape[2] != len(names):
        raise ValueError("Expected [chain, draw, parameter] matching names.")
    if chains.shape[0] < 2 or chains.shape[1] < 4:
        raise ValueError("Diagnostics require at least two chains and four draws.")
    if not np.isfinite(chains).all():
        raise ValueError("Posterior samples contain non-finite values.")
    data = az.from_dict(posterior={name: chains[:, :, i] for i, name in enumerate(names)})
    rhat = az.rhat(data, method="rank")
    bulk = az.ess(data, method="bulk")
    tail = az.ess(data, method="tail")
    mcse = az.mcse(data, method="mean")
    return pd.DataFrame([
        {"Parameter": name, "Mean": chains[:, :, i].mean(),
         "MCSE mean": float(mcse[name]), "R-hat": float(rhat[name]),
         "ESS bulk": float(bulk[name]), "ESS tail": float(tail[name]),
         "ESS conservative": min(float(bulk[name]), float(tail[name]))}
        for i, name in enumerate(names)
    ])


def nuts_diagnostics(sampler):
    """Expose public Numerics 2.2 NUTS diagnostics with one row per chain."""
    return pd.DataFrame({
        "Chain": range(1, sampler.NumberOfChains + 1),
        "Transitions after warmup": list(sampler.DiagnosticSampleCounts),
        "Acceptance": list(sampler.HamiltonianAcceptanceRates),
        "Step size": list(sampler.StepSizes),
        "Divergences": list(sampler.DivergenceCounts),
        "Max-depth hits": list(sampler.MaxTreeDepthHitCounts),
        "Mean tree depth": list(sampler.MeanTreeDepths),
        "Mean leapfrog steps": list(sampler.MeanLeapfrogSteps),
        "E-BFMI": list(sampler.EnergyBayesianFractionOfMissingInformation),
    })
