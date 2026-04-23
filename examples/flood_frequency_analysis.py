"""Flood frequency analysis demo using Numerics via PythonNet. Once this file runs you will have a popup window of graphs 
and tables will be output to the terminal.
"""

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pythonnet

pythonnet.load("coreclr")
import clr


def _resolve_numerics_dll():
    """Resolve Numerics.dll from NUMERICS_DLL env var, the NuGet cache, or a local packages/ folder."""
    env = os.environ.get("NUMERICS_DLL")
    if env:
        return Path(env)
    cache = Path.home() / ".nuget" / "packages" / "rmc.numerics"
    if cache.exists():
        hits = sorted(cache.glob("*/lib/net8.0/Numerics.dll"), reverse=True)
        if hits:
            return hits[0]
    for root in (Path.cwd(), Path(__file__).parent.parent):
        local = sorted((root / "packages").glob("RMC.Numerics.*/lib/net8.0/Numerics.dll"), reverse=True)
        if local:
            return local[0]
    raise FileNotFoundError(
        "Numerics DLL not found. Install via `dotnet add package RMC.Numerics --version 2.0.1` "
        "or set the NUMERICS_DLL environment variable."
    )


def load_numerics():
    dll_path = _resolve_numerics_dll()
    clr.AddReference(str(dll_path))


def main():
    load_numerics()

    from Numerics.Data.Statistics import GoodnessOfFit
    from Numerics.Distributions import (
        GeneralizedExtremeValue,
        LogNormal,
        ParameterEstimationMethod,
        Weibull,
    )
    from System import Array, Double

    peak_flows = np.array(
        [
            6290, 2700, 13100, 16900, 14600, 9600, 7740, 8490, 8130, 12000,
            17200, 15000, 12400, 6960, 6500, 5840, 10400, 18800, 21400, 22600,
            14200, 11000, 12800, 15700, 4740, 6950, 11800, 12100, 20600, 14600,
            14600, 8900, 10600, 14200, 14100, 14100, 12500, 7530, 13400, 17600,
            13400, 19200, 16900, 15500, 14500, 21900, 10400, 7460,
        ]
    )
    peak_flows_sorted = np.sort(peak_flows)

    # Convert Python data to .NET
    net_data = Array[Double]([float(v) for v in peak_flows])
    net_data_sorted = Array[Double]([float(v) for v in peak_flows_sorted])

    # Fit 3 different models
    ln = LogNormal()
    ln.Estimate(net_data, ParameterEstimationMethod.MaximumLikelihood)

    gev = GeneralizedExtremeValue()
    gev.Estimate(net_data, ParameterEstimationMethod.MethodOfLinearMoments)

    wb = Weibull()
    wb.Estimate(net_data, ParameterEstimationMethod.MaximumLikelihood)

    models = {"LogNormal": ln, "GEV": gev, "Weibull": wb}

    fit_rows = []
    for name, dist in models.items():
        kstest = GoodnessOfFit.KolmogorovSmirnov(net_data_sorted, dist) # Needs sorted data
        fit_rows.append(
            {
                "Model": name,
                "LogLikelihood": dist.LogLikelihood(net_data),
                "KS Statistic": kstest,
            }
        )
    fit_df = pd.DataFrame(fit_rows).sort_values("KS Statistic")
    print("Model fit summary (lower KS is better):")
    print(fit_df.to_string(index=False, float_format=lambda v: f"{v:,.4f}"))

    return_periods = np.array([2, 5, 10, 25, 50, 100], dtype=float)
    probs = 1.0 - 1.0 / return_periods

    quantile_rows = []
    for name, dist in models.items():
        q = [dist.InverseCDF(float(p)) for p in probs]
        for rp, qi in zip(return_periods, q):
            quantile_rows.append({"Model": name, "ReturnPeriod": int(rp), "DesignFlow": qi})
    quantile_df = pd.DataFrame(quantile_rows)
    print("\nDesign flow table:")
    print(
        quantile_df.pivot(index="ReturnPeriod", columns="Model", values="DesignFlow")
        .round(1)
        .to_string()
    )

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1) Histogram + fitted PDFs
    x_pdf = np.linspace(peak_flows.min() * 0.8, peak_flows.max() * 1.1, 500)
    axes[0, 0].hist(
        peak_flows,
        bins=16,
        density=True,
        alpha=0.5,
        color="gray",
        edgecolor="black",
        label="Observed",
    )
    for name, dist in models.items():
        axes[0, 0].plot(x_pdf, [dist.PDF(float(xi)) for xi in x_pdf], linewidth=2, label=name)
    axes[0, 0].set_title("Observed Data and Fitted PDFs")
    axes[0, 0].set_xlabel("Peak Flow (cfs)")
    axes[0, 0].set_ylabel("Density")
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()

    # 2) Empirical CDF + fitted CDFs
    sorted_flows = np.sort(peak_flows)
    ecdf = np.arange(1, len(sorted_flows) + 1) / len(sorted_flows)
    axes[0, 1].step(sorted_flows, ecdf, where="post", color="black", linewidth=2, label="ECDF")
    for name, dist in models.items():
        axes[0, 1].plot(
            sorted_flows,
            [dist.CDF(float(xi)) for xi in sorted_flows],
            linewidth=2,
            label=name,
        )
    axes[0, 1].set_title("Empirical vs Fitted CDFs")
    axes[0, 1].set_xlabel("Peak Flow (cfs)")
    axes[0, 1].set_ylabel("CDF")
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()

    # 3) Return period (frequency curve)
    for name, grp in quantile_df.groupby("Model"):
        axes[1, 0].plot(
            grp["ReturnPeriod"].values,
            grp["DesignFlow"].values,
            marker="o",
            linewidth=2,
            label=name,
        )
    axes[1, 0].set_xscale("log")
    axes[1, 0].set_title("Flood Frequency Curves")
    axes[1, 0].set_xlabel("Return Period (years)")
    axes[1, 0].set_ylabel("Design Flow (cfs)")
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()

    # 4) KS statistic bar chart
    axes[1, 1].bar(fit_df["Model"], fit_df["KS Statistic"], color=["steelblue", "coral", "seagreen"])
    axes[1, 1].set_title("Goodness of Fit (KS Statistic)")
    axes[1, 1].set_ylabel("KS Statistic")
    axes[1, 1].grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
