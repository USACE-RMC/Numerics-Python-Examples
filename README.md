# Numerics Python Examples

This repository contains Python notebooks that demonstrate the Numerics .NET library through pythonnet. The goal is to give practical, reproducible examples for distributions, MCMC, optimization, statistics, time series, machine learning, and linear models.

## Contents
- `notebooks/` Jupyter notebooks organized by topic
- `examples/` Small focused scripts and helpers
- `src/` Supporting Python utilities

## Prerequisites
- Windows with .NET installed
- Python with pythonnet
- Numerics built locally so the DLL exists at the path used in notebooks

## Quick Start
1. Create and activate a Python environment.
2. Install notebook requirements: `pip install -r notebook-requirements.txt`.
3. Build Numerics and confirm the DLL path matches what the notebooks expect.
4. Open the notebooks in Jupyter or VS Code and run cells top to bottom.

## Notes
- These notebooks compare Numerics to common Python libraries where relevant. When comparing MCMC chains, pay attention to default thinning and warmup settings so the comparisons are aligned.
- Many examples use synthetic data to keep results consistent and easy to interpret.

## How To Update DLL Path
If your Numerics build output is in a different location, update the DLL path in the setup cell of each notebook. Search for `Numerics.dll` and replace the path with your local build output.

## License
See the Numerics project license for usage and distribution terms.
