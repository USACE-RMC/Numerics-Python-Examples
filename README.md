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
- Python **3.12** is the validated environment for this release; install the compatible versions in `notebook-requirements.txt`.
- The **.NET 10 SDK** (not only an older runtime). Install it from the [.NET download page](https://dotnet.microsoft.com/download/dotnet/10.0), then confirm `dotnet --list-sdks` includes a `10.0.x` SDK.
- The published [RMC.Numerics 2.2.0 package](https://www.nuget.org/packages/RMC.Numerics/2.2.0), restored by the checked-in project in the Quick Start.

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

3. Restore the exact `RMC.Numerics` package

   ```bash
   dotnet restore dotnet/NumericsRuntime.csproj --configfile NuGet.config --no-cache
   ```

   [`NuGet.config`](NuGet.config) clears inherited package sources and enables only NuGet.org. [`dotnet/NumericsRuntime.csproj`](dotnet/NumericsRuntime.csproj) pins `RMC.Numerics` to exact version `[2.2.0]` and restores it under the project-local ignored `packages/` directory.

4. Load Numerics in a notebook or script

   ```python
   from helper_functions import load_numerics
   dll_path = load_numerics()
   ```

   `load_numerics()` starts CoreCLR with the checked-in .NET 10 runtime configuration, verifies that the active runtime is .NET 10, and preflights the assembly name/version before loading. It validates target framework `net10.0` after loading because that attribute is exposed on the loaded assembly; if a development override fails that check, restart Python before selecting another DLL. `resolve_numerics_dll()` remains available when only the resolved path is needed.

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

Build the `net10.0` target, then point the examples at that DLL by setting `NUMERICS_DLL` before launching Jupyter:

```powershell
# PowerShell
$env:NUMERICS_DLL = "C:\path\to\Numerics\Numerics\bin\Release\net10.0\Numerics.dll"

# bash / zsh
export NUMERICS_DLL=/path/to/Numerics/Numerics/bin/Release/net10.0/Numerics.dll
```

The override is explicit and validated: it must exist and contain Numerics assembly version `2.2.0.0` targeting `net10.0`. Name/version mismatches are rejected before loading. A target-framework mismatch is detected after loading and requires a fresh Python process. Without the override, the loader uses only the exact project-local package path restored above; it does not select a newer package from a global cache.

## Notes
- These notebooks compare Numerics to common Python libraries where relevant. When comparing MCMC chains, align warmup/thinning settings.
- Many examples use synthetic data to keep results consistent and easy to interpret.

## Release benchmarks and validation

Notebook 05 includes an inline C# likelihood compiled with the .NET SDK's Roslyn
compiler, bound directly to a managed delegate. It compares Python/sequential,
C#/sequential, C#/parallel, and PyMC NUTS with matched transition counts and
chain-aware diagnostics. Compilation and sampling are reported separately.
Notebook 11 reports repeated Random Forest train/predict timings with explicit
model settings and prediction-aggregation differences.

Run benchmarks on an otherwise quiet machine. The environment tables identify
the runtime, dependencies, and whether PyTensor found a C++ compiler; Python
fallback PyMC timings do not represent an optimized compiled installation.
Small likelihoods may be faster sequentially because parallel scheduling has
overhead. Report observed ratios rather than assuming a speed advantage.

For a complete local check, from the repository root in the activated environment:

```powershell
python -m pip install -r validation-requirements.txt
dotnet restore dotnet/NumericsRuntime.csproj --configfile NuGet.config --no-cache
dotnet restore tests/fixtures/AssemblyFixture/AssemblyFixture.csproj --configfile NuGet.config
python -m pytest -q
python tests/runtime_smoke.py
python tests/runtime_identity_preflight.py
python tests/runtime_override_rejection.py
python tests/runtime_diagnostics.py
python scripts/validate_examples.py --notebooks 00 05 06 11 --update-outputs
python scripts/validate_examples.py --notebooks 01 02 03 04 07 08 09 10 12 --scripts
```

The validator uses this environment's Python in a fresh kernel per notebook,
without changing the user's kernel registry. Generated notebooks and script logs
are kept under ignored `artifacts/validation/`. The release output exception in
[CONTRIBUTING](CONTRIBUTING.md) applies to notebooks 00, 05, 06, and 11; the other
notebooks retain source only. Use `--schema-only` for a quick structural check.

See the [2.2 reference validation report](docs/validation/2026-09-18-numerics-2.2-validation.md)
for the measured environment, results, and limitations.

## License
This project is released under the [Zero-Clause BSD (0BSD) license](LICENSE).
