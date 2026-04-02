"""Bayesian linear regression demo with Numerics DEMCzs.
This file takes approximately 5 minutes to run. Once it is complete you will have a popup window of graphs 
and tables will be output to the terminal.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pythonnet

pythonnet.load("coreclr")
import clr


def load_numerics():
    dll_path = Path(r"C:\GIT\Numerics\Numerics\bin\Debug\net8.0\Numerics.dll")
    if not dll_path.exists():
        raise FileNotFoundError(
            f"Numerics DLL not found at {dll_path}. Update `dll_path` in this script."
        )
    clr.AddReference(str(dll_path))


def main(seed=123):
    load_numerics()

    from Numerics.Distributions import IUnivariateDistribution, Normal, Uniform
    from Numerics.Sampling.MCMC import DEMCzs, LogLikelihood, MCMCResults
    from System.Collections.Generic import List
    from System.Threading import ThreadPool
    import os
    
    ''' NOTE FOR DEMO USERS:
    When calling Numerics MCMC samplers from Python via pythonnet, the samplers'
    internal parallel chains (Parallel.For) contend for Python's Global Interpreter
    Lock (GIL). This makes parallel execution slower than sequential. Setting
    max thread pool workers to 1 forces sequential execution and removes that
    overhead. In pure C#, you can remove this line and parallelism will work as
    intended. 

    This is also why we set sampler.ParallelizeChains = False for every example.
    It defaults to True, which works well in C#, but it slows the sampler down 
    in Python'''
    ThreadPool.SetMaxThreads(1, 1)  # (workerThreads, completionPortThreads)

    x = np.linspace(0, 10, 80)
    true_a, true_b, true_sigma = 2.0, 1.4, 1.2
    y = true_a + true_b * x + np.asarray(Normal(0, true_sigma).GenerateRandomValues(len(x),seed))

    priors = List[IUnivariateDistribution]()
    # Flat priors - we assume we know very little
    priors.Add(Uniform(-10, 10))
    priors.Add(Uniform(0, 5))
    priors.Add(Uniform(0.1, 5))

    # Define likelihood
    def log_likelihood(params):
        a, b, sigma = params[0], params[1], params[2]
        residuals = y - (a + b * x)
        dist = Normal(0, sigma)
        return sum(dist.LogPDF(float(r)) for r in residuals)

    # Run sampler
    sampler = DEMCzs(priors, LogLikelihood(log_likelihood))
    sampler.ParallelizeChains = False
    sampler.Sample()
    results = MCMCResults(sampler)

    # Extract results
    a_stats = results.ParameterResults[0].SummaryStatistics
    b_stats = results.ParameterResults[1].SummaryStatistics
    s_stats = results.ParameterResults[2].SummaryStatistics

    posterior_df = pd.DataFrame(
        [
            {
                "Parameter": "a",
                "True": true_a,
                "PosteriorMean": a_stats.Mean,
                "Lower90": a_stats.LowerCI,
                "Upper90": a_stats.UpperCI,
            },
            {
                "Parameter": "b",
                "True": true_b,
                "PosteriorMean": b_stats.Mean,
                "Lower90": b_stats.LowerCI,
                "Upper90": b_stats.UpperCI,
            },
            {
                "Parameter": "sigma",
                "True": true_sigma,
                "PosteriorMean": s_stats.Mean,
                "Lower90": s_stats.LowerCI,
                "Upper90": s_stats.UpperCI,
            },
        ]
    )
    print("Bayesian regression (Numerics DEMCzs) parameter summary:")
    print(posterior_df.to_string(index=False, float_format=lambda v: f"{v:,.4f}"))

    chain = results.MarkovChains[0]
    a_samples = np.array([chain[i].Values[0] for i in range(len(chain))], dtype=float)
    b_samples = np.array([chain[i].Values[1] for i in range(len(chain))], dtype=float)
    sigma_samples = np.array([chain[i].Values[2] for i in range(len(chain))], dtype=float)

    # Mean-function credible band: E[y|x,theta] = a + b*x
    # mu_draws[i,j] = a_i + b_i*x_j
    mu_draws = a_samples[:, None] + b_samples[:, None] * x[None, :] # Model mean draws for every posterior sample at every x
    y_hat_mean = mu_draws.mean(axis=0) # Average accross posterior draws for each x_j
    y_hat_low, y_hat_up = np.quantile(mu_draws, [0.05, 0.95], axis=0) # 90% interval for each x_j


    fit_df = pd.DataFrame(
        {
            "x": x,
            "y_observed": y,
            "y_hat_mean": y_hat_mean,
            "y_hat_low": y_hat_low,
            "y_hat_up": y_hat_up,
        }
    )
    print("\nFirst 10 fitted rows:")
    print(fit_df.head(10).to_string(index=False, float_format=lambda v: f"{v:,.4f}"))

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Data + fit band
    axes[0, 0].scatter(x, y, color="black", s=20, alpha=0.6, label="Observed")
    axes[0, 0].plot(x, y_hat_mean, color="steelblue", linewidth=2.5, label="Posterior mean line")
    axes[0, 0].fill_between(x, y_hat_low, y_hat_up, color="steelblue", alpha=0.2, label="Approx 90% band")
    axes[0, 0].set_title("Bayesian Regression Fit")
    axes[0, 0].set_xlabel("x")
    axes[0, 0].set_ylabel("y")
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()

    # Residual plot
    residuals = y - y_hat_mean
    axes[0, 1].scatter(y_hat_mean, residuals, s=20, alpha=0.6, color="coral")
    axes[0, 1].axhline(0, color="black", linestyle="--", linewidth=1.5)
    axes[0, 1].set_title("Residuals vs Fitted")
    axes[0, 1].set_xlabel("Fitted")
    axes[0, 1].set_ylabel("Residual")
    axes[0, 1].grid(True, alpha=0.3)

    # Posterior histograms
    axes[1, 0].hist(a_samples, bins=40, alpha=0.6, label="a", color="slateblue", density=True)
    axes[1, 0].hist(b_samples, bins=40, alpha=0.6, label="b", color="seagreen", density=True)
    axes[1,0].axvline(true_a, color = 'blue', label = 'true a')
    axes[1,0].axvline(true_b, color = 'green', label = 'true b')
    axes[1, 0].set_title("Posterior Distributions: a and b")
    axes[1, 0].set_xlabel("Value")
    axes[1, 0].set_ylabel("Density")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].hist(sigma_samples, bins=40, alpha=0.75, color="darkorange", density=True)
    axes[1, 1].axvline(true_sigma, color="red", linestyle="--", linewidth=2, label="True sigma")
    axes[1, 1].set_title("Posterior Distribution: sigma")
    axes[1, 1].set_xlabel("sigma")
    axes[1, 1].set_ylabel("Density")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
