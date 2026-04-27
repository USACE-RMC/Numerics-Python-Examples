# Numerics Python Examples

[![License: 0BSD](https://img.shields.io/badge/License-0BSD-blue.svg)](https://opensource.org/licenses/0BSD)
[![DOI](https://zenodo.org/badge/1135095276.svg)](https://doi.org/10.5281/zenodo.19715583)

This repository contains Python notebooks that demonstrate the Numerics .NET library through pythonnet. The notebooks provide practical, reproducible examples of Numerics applications, including distribution fitting, MCMC, optimization, statistical analysis, time series analysis, machine learning, and linear model fitting.

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
- Python **3.10–3.13** recommended. pythonnet does not yet support Python 3.14.
- .NET 6+ runtime (or .NET Framework 4.8.1 on Windows). Install the [.NET SDK](https://dotnet.microsoft.com/download) if you don't already have it.
- The [RMC.Numerics](https://www.nuget.org/packages/RMC.Numerics) NuGet package (see Quick Start).

## Quick Start
The quick start will walk you through creating a virtual Python environment, installing the notebook requirements, and pulling in the `RMC.Numerics` NuGet package. For a more in-depth walkthrough see notebook [`00_getting_started.ipynb`](notebooks/00_getting_started.ipynb).  
**NOTE:** The commands below assume Windows. See notebook `00` for macOS/Linux equivalents.

1. Create and activate a virtual Python environment

   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install ipykernel
   python -m ipykernel install --user --name=.venv --display-name "Python (.venv)"
   ```

2. Install the Python requirements

   ```bash
   pip install -r notebook-requirements.txt
   ```

3. Install the `RMC.Numerics` NuGet package

   ```bash
   # Option A — global NuGet cache (recommended; requires the .NET SDK):
   dotnet add package RMC.Numerics

   # Option B — local packages/ folder (requires nuget.exe on PATH):
   nuget install RMC.Numerics -OutputDirectory packages
   ```

   Both commands pull the **latest** published version by default. This demo was built against version `2.0.1`; to pin that version, append `--version 2.0.1` (Option A) or `-Version 2.0.1` (Option B).

   The notebooks auto-discover the DLL in either location via `resolve_numerics_dll()` in [`notebooks/helper_functions.py`](notebooks/helper_functions.py).

4. Load Numerics in a notebook or script

   ```python
   import pythonnet
   pythonnet.load("coreclr")

   import clr
   from helper_functions import resolve_numerics_dll
   clr.AddReference(str(resolve_numerics_dll()))
   ```

5. Create a Normal distribution

   ```python
   from Numerics.Distributions import Normal
   dist = Normal(100, 15)
   ```

## Using a local Numerics build instead of NuGet

If you prefer to build Numerics from source — for example, to develop against the latest `main` branch — clone the [Numerics](https://github.com/USACE-RMC/Numerics) repo and build it:

```bash
git clone https://github.com/USACE-RMC/Numerics.git
cd Numerics
dotnet build Numerics.sln --configuration Release
```

Then point the notebooks at your build by setting the `NUMERICS_DLL` environment variable before launching Jupyter:

```powershell
# PowerShell
$env:NUMERICS_DLL = "C:\path\to\Numerics\Numerics\bin\Release\net8.0\Numerics.dll"

# bash / zsh
export NUMERICS_DLL=/path/to/Numerics/Numerics/bin/Release/net8.0/Numerics.dll
```

`resolve_numerics_dll()` uses this variable first, then falls back to the NuGet cache and finally a local `packages/` folder.

## Notes
- These notebooks compare Numerics to common Python libraries where relevant. When comparing MCMC chains, align warmup/thinning settings.
- Many examples use synthetic data to keep results consistent and easy to interpret.

## License
This project is released under the [Zero-Clause BSD (0BSD) license](LICENSE).
