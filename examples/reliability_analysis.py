"""Reliability analysis demo using Monte Carlo simulation. Once this file runs you will have a popup window of graphs 
and tables will be ouput to the terminal."""

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pythonnet
from scipy.stats import norm

pythonnet.load("coreclr")
import clr


def load_numerics():
    dll_path = Path(r"C:\GIT\Numerics\Numerics\bin\Debug\net8.0\Numerics.dll")
    if not dll_path.exists():
        raise FileNotFoundError(
            f"Numerics DLL not found at {dll_path}. Update `dll_path` in this script."
        )
    clr.AddReference(str(dll_path))


def main(n_samples=100_000, seed=42):
    load_numerics()

    from Numerics.Distributions import LogNormal, Normal

    # Numerics LogNormal expects log-space parameters (mu, sigma) for ln(X).
    # Convert target physical-space mean/std to avoid overflow (e.g., exp(500)).
    resistance_mean = 500.0
    resistance_std = 120.0
    sigma2_ln = np.log1p((resistance_std / resistance_mean) ** 2)
    sigma_ln = np.sqrt(sigma2_ln)
    mu_ln = np.log(resistance_mean) - 0.5 * sigma2_ln
    resistance_dist = LogNormal(float(mu_ln), float(sigma_ln))
    # Numerics uses base-10 log by default so we set it to use base e
    resistance_dist.Base = float(math.e)
    load_dist = Normal(380.0, 90.0)

    resistance = np.array(list(resistance_dist.GenerateRandomValues(int(n_samples), int(seed))))
    load = np.array(list(load_dist.GenerateRandomValues(int(n_samples), int(seed + 1))))

    g = resistance - load
    pf = np.mean(g <= 0.0)
    beta = -norm.ppf(pf) if 0 < pf < 1 else np.inf

    summary_df = pd.DataFrame(
        [
            {"Metric": "Samples", "Value": float(n_samples)},
            {"Metric": "Mean resistance", "Value": float(np.mean(resistance))},
            {"Metric": "Std resistance", "Value": float(np.std(resistance, ddof=1))},
            {"Metric": "Mean load", "Value": float(np.mean(load))},
            {"Metric": "Std load", "Value": float(np.std(load, ddof=1))},
            {"Metric": "Pf", "Value": float(pf)},
            {"Metric": "beta", "Value": float(beta)},
        ]
    )
    print("Reliability analysis summary:")
    print(summary_df.to_string(index=False, float_format=lambda v: f"{v:,.6f}"))

    sample_out = np.column_stack([resistance[:10], load[:10], g[:10]])
    sample_df = pd.DataFrame(sample_out, columns=["Resistance", "Load", "g = R - S"])
    print("\nFirst 10 simulated samples:")
    print(sample_df.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Distribution overlay
    x_min = min(resistance.min(), load.min())
    x_max = max(resistance.max(), load.max())
    x_grid = np.linspace(x_min, x_max, 600)
    axes[0, 0].hist(
        resistance,
        bins=40,
        density=True,
        alpha=0.5,
        color="steelblue",
        edgecolor="black",
        label="Resistance",
    )
    axes[0, 0].hist(
        load,
        bins=40,
        density=True,
        alpha=0.5,
        color="coral",
        edgecolor="black",
        label="Load",
    )
    axes[0, 0].set_title("Resistance and Load Distributions")
    axes[0, 0].set_xlabel("Value")
    axes[0, 0].set_ylabel("Density")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Limit-state histogram
    axes[0, 1].hist(g, bins=50, color="slategray", alpha=0.8, edgecolor="black")
    axes[0, 1].axvline(0, color="red", linestyle="--", linewidth=2, label="Failure boundary")
    axes[0, 1].set_title("Limit-State Distribution (g = R - S)")
    axes[0, 1].set_xlabel("g")
    axes[0, 1].set_ylabel("Count")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Scatter and failure highlighting
    fail_mask = g <= 0
    axes[1, 0].scatter(
        load[~fail_mask],
        resistance[~fail_mask],
        s=8,
        alpha=0.3,
        color="seagreen",
        label="Safe",
    )
    axes[1, 0].scatter(
        load[fail_mask],
        resistance[fail_mask],
        s=8,
        alpha=0.6,
        color="firebrick",
        label="Failure",
    )
    line = np.linspace(x_min, x_max, 200)
    axes[1, 0].plot(line, line, "k--", linewidth=1.5, label="R = S boundary")
    axes[1, 0].set_title("Monte Carlo Samples in (Load, Resistance) Space")
    axes[1, 0].set_xlabel("Load (S)")
    axes[1, 0].set_ylabel("Resistance (R)")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Empirical CDF of g
    g_sorted = np.sort(g)
    cdf = np.arange(1, len(g_sorted) + 1) / len(g_sorted)
    axes[1, 1].plot(g_sorted, cdf, color="purple", linewidth=2)
    axes[1, 1].axvline(0, color="red", linestyle="--", linewidth=2)
    axes[1, 1].set_title("Empirical CDF of g = R - S")
    axes[1, 1].set_xlabel("g")
    axes[1, 1].set_ylabel("CDF")
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
