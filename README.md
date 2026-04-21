# Numerics Python Examples

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
- Windows with .NET installed (or .NET 6+ runtime on Linux/macOS)
- Python with [pythonnet](https://github.com/pythonnet/pythonnet)
- Numerics built and compiled locally. The resulting DLL path must match the path referenced in the notebooks — see Quick Start and/or notebook 00 for setup instructions.

## Quick Start
The quick start will step through the creation of an active python environment, installing the notebook requirements & RMC-Numerics, and getting the methods ready to be used. For a more in depth walk through see notebook 00.      
**NOTE:** This set up is geared towards Windows users. For other operating systems see notebook 00.      

1. Create and activate a virtual Python environment
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install ipykernel
python -m ipykernel install --user --name=.venv --display-name "Python (.venv)"
```

2. Install notebook requirements 
```bash
pip install -r notebook-requirements.txt
```

3. Install and build Numerics
```bash
git clone https://github.com/USACE-RMC/Numerics.git
cd Numerics
dotnet build Numerics.sln --configuration Release
```

4. Load and confirm the DLL path
```bash
import pythonnet
pythonnet.load("coreclr")

import clr 
from pathlib import Path 

# Path to your Numerics.dll
# MODIFY THIS PATH to make your installation
dll_path = Path(r"C:\GIT\Numerics\Numerics\bin\Debug\net8.0\Numerics.dll")
clr.AddReference(str(dll_path))
```

5. Create a Normal Distribution
```bash
from Numerics.Distributions import Normal
dist = Normal(100,15)
```

## Notes
- These notebooks compare Numerics to common Python libraries where relevant. When comparing MCMC chains, align warmup/thinning settings.
- Many examples use synthetic data to keep results consistent and easy to interpret.

## How To Update DLL Path
If your Numerics build output is in a different location, update the DLL path in the setup cell of each notebook. Search for `Numerics.dll` and replace the path with your local build output.

## License
See the Numerics project license for usage and distribution terms.
