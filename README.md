# Numerics Python Examples

This repository contains Python notebooks that demonstrate the Numerics .NET library through pythonnet. The goal is to provide practical, reproducible examples for distributions, MCMC, optimization, statistics, time series, machine learning, and linear models.

## Contents
- `notebooks/` Jupyter notebooks organized by topic
- `examples/` Focused scripts and end-to-end demos

## Notebooks Overview
- `00_getting_started.ipynb` Setup and first run
- `01_distributions.ipynb` Distribution basics and plotting
- `02_distribution_fitting.ipynb` MOM/MLE/L-moments + goodness-of-fit
- `03_mcmc_basics.ipynb` Intro Bayesian inference and RWMH
- `04_mcmc_bayesian_inference.ipynb` Practical workflows and comparisons
- `05_mcmc_adaptive.ipynb` Adaptive MCMC samplers
- `06_mcmc_diagnostics.ipynb` Diagnostics (ESS, mixing, multimodal)
- `07_integration_and_root_finding.ipynb` Numerical methods
- `08_optimization.ipynb` Local/global optimization
- `09_statistics.ipynb` Core statistics and tests
- `10_time_series.ipynb` Time series objects and analysis
- `11_machine_learning.ipynb` RF, KNN, trees, clustering
- `12_linear_models.ipynb` Linear/GLM workflows

## Prerequisites
- Windows with .NET installed (or .NET 6+ runtime on Linux/macOS)
- Python with pythonnet
- Numerics built locally so the DLL exists at the path used in notebooks

## Quick Start
1. Create and activate a Python environment.
2. Install notebook requirements: `pip install -r notebook-requirements.txt`.
3. Build Numerics and confirm the DLL path matches what the notebooks expect.
4. Open notebooks in Jupyter or VS Code and run cells top to bottom.

## Docs
- `docs/api_cheatsheet.md` Quick mapping of common Numerics tasks to PythonNet calls.

## Notes
- These notebooks compare Numerics to common Python libraries where relevant. When comparing MCMC chains, align warmup/thinning settings.
- Many examples use synthetic data to keep results consistent and easy to interpret.

## How To Update DLL Path
If your Numerics build output is in a different location, update the DLL path in the setup cell of each notebook. Search for `Numerics.dll` and replace the path with your local build output.

## License
See the Numerics project license for usage and distribution terms.
