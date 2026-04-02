# Numerics Python Demos - Project Scope

## Overview

This document defines the scope for a PythonNet demo repository that showcases the Numerics library for Python users.

---

## Repository

**Name:** `numerics-python-examples`

**Rationale:** Clear, searchable name that communicates these are examples/demos rather than a full wrapper.

**Location:** Separate from the core Numerics repo to:
- Keep demos independent from core library release cycles
- Make it easier for Python users to discover and clone
- Allow different contribution guidelines

---

## Repository Structure

```
numerics-python-examples/
|-- README.md                      # Overview, installation, getting started
|-- LICENSE                        # Same as Numerics (BSD-style USACE-RMC)
|-- notebook-requirements.txt      # Necessary Python packages to install
|-- CONTRIBUTING.md                # How to contribute
|-- CODE_OF_CONDUCT.md             # Community guidelines
|
|-- notebooks/
|   |-- 00_getting_started.ipynb
|   |-- 01_distributions.ipynb
|   |-- 02_distribution_fitting.ipynb
|   |-- 03_mcmc_basics.ipynb
|   |-- 04_mcmc_bayesian_inference.ipynb
|   |-- 05_mcmc_adaptive.ipynb
|   |-- 06_mcmc_diagnostics.ipynb
|   |-- 07_integration_and_root_finding.ipynb
|   |-- 08_optimization.ipynb
|   |-- 09_statistics.ipynb
|   |-- 10_time_series.ipynb
|   |-- 11_machine_learning.ipynb
|   |-- 12_linear_models.ipynb
|   `-- helper_functions.py        # Shared helper functions
|
`-- examples/
    |-- bayesian_regression.py      # Classic Bayesian example
    |-- flood_frequency_analysis.py # Real-world hydrology example
    `-- reliability_analysis.py     # Engineering reliability example
```

---

## Jupyter Notebooks

### 00. Getting Started
**Purpose:** Environment setup and "Hello World"

**Content:**
- Installing .NET runtime (Windows/Linux/Mac)
- Installing PythonNet via pip
- Loading the Numerics DLL
- First example: create a Normal distribution, compute PDF/CDF
- Troubleshooting common issues

**Code Preview:**
```python
import clr
clr.AddReference("Numerics")
from Numerics.Distributions import Normal

dist = Normal(100, 15)
print(f"Mean: {dist.Mean}, Std: {dist.StandardDeviation}")
print(f"P(X < 120) = {dist.CDF(120):.4f}")
```

---

### 01. Distributions
**Purpose:** Tour of the 40+ univariate distributions

**Content:**
- Creating distributions (Normal, LogNormal, Gamma, Weibull, GEV, etc.)
- PDF, CDF, InverseCDF (quantiles)
- Generating random samples
- Statistical properties (mean, std, skew, kurtosis)
- Plotting distributions with matplotlib
- Discrete distributions (Poisson, Binomial)
- Special distributions (PERT, Triangular, Mixture)

**Real-world context:** "Which distribution fits my data?"

---

### 02. Distribution Fitting
**Purpose:** Parameter estimation from data

**Content:**
- Method of Moments (MOM)
- Maximum Likelihood Estimation (MLE)
- L-Moments (Linear Moments)
- Comparing estimation methods
- Goodness-of-fit tests (KS, Anderson-Darling, Chi-squared)
- Plotting fitted vs empirical CDF
- Bootstrap confidence intervals on parameters
- Plotting positions (Weibull, Gringorten)

**Real-world context:** Flood frequency analysis - fitting annual peak flows

---

### 03. MCMC Basics
**Purpose:** Introduction to Bayesian inference with Numerics

**Content:**
- What is MCMC and why use it?
- Simple example: estimating mean of a Normal distribution
- Setting priors
- Defining log-likelihood
- Running RWMH sampler
- Interpreting results (trace plots, posterior distributions)
- Burn-in and thinning

**Code Preview:**
```python
from Numerics.Sampling.MCMC import RWMH
from Numerics.Distributions import Normal, Uniform
from System import Func, Double
from System.Collections.Generic import List

priors = List[UnivariateDistributionBase]()
priors.Add(Uniform(0, 200))
priors.Add(Uniform(1, 50))

def log_likelihood(params):
    mu, sigma = params[0], params[1]
    dist = Normal(mu, sigma)
    return sum(dist.LogPDF(x) for x in data)

sampler = RWMH(priors, Func[List[Double], Double](log_likelihood))
sampler.Sample()
```

---

### 04. MCMC Bayesian Inference
**Purpose:** Practical Bayesian modeling workflows

**Content:**
- Linear regression with uncertainty
- Comparing different samplers (RWMH vs DEMCz vs HMC)
- Performance benchmark: Numerics vs PyMC (key selling point)
- Posterior predictive checks
- Credible intervals
- Model comparison

**Real-world context:** Estimating a rating curve with uncertainty

---

### 05. MCMC Adaptive
**Purpose:** Adaptive MCMC techniques and performance

**Content:**
- Adaptive Random Walk Metropolis (ARWMH)
- Differential Evolution MCMC (DEMCz, DEMCzs)
- Efficiency comparisons and ESS
- Practical tuning guidance

---

### 06. MCMC Diagnostics
**Purpose:** Diagnosing convergence and mixing

**Content:**
- Multiple chains and convergence checks
- Effective sample size (ESS)
- Autocorrelation diagnostics
- Handling multimodal posteriors

---

### 07. Integration and Root Finding
**Purpose:** Numerical integration and root finding

**Content:**
- Quadrature methods
- Root-finding algorithms
- Practical examples and error checks

---

### 08. Optimization
**Purpose:** Finding minima/maxima

**Content:**
- Local optimization (Nelder-Mead, BFGS, Powell)
- Global optimization (PSO, Simulated Annealing)
- Constrained optimization
- Practical tips: bounds and initialization

**Real-world context:** Calibrating a model to observed data

---

### 09. Statistics
**Purpose:** Statistical analysis toolkit

**Content:**
- Descriptive statistics
- Correlation (Pearson, Spearman, Kendall)
- Hypothesis tests (t-test, Mann-Whitney)
- Bootstrap resampling
- Outlier detection (Multiple Grubbs-Beck)
- Box-Cox and Yeo-Johnson transformations
- Histogram and kernel density estimation

---

### 10. Time Series
**Purpose:** Working with temporal data

**Content:**
- Creating TimeSeries objects
- Smoothing (moving average, exponential, Gaussian)
- Block operations (annual max, monthly mean)
- Interpolation and resampling
- USGS data download integration
- Plotting time series

**Real-world context:** Analyzing streamflow records

---

### 11. Machine Learning
**Purpose:** ML capabilities in Numerics

**Content:**
- Random Forest (classification and regression)
- K-Means clustering
- Gaussian Mixture Models
- K-Nearest Neighbors
- Decision Trees
- When to use Numerics ML vs scikit-learn

---

### 12. Linear Models
**Purpose:** Regression workflows

**Content:**
- Generalized Linear Models and link functions
- Linear regression (identity link)
- Logistic regression (logit link) for binary outcomes
- Poisson regression (log link) for count data
- Alternative link functions (probit, complementary log-log)

---

## Standalone Python Examples

### bayesian_regression.py
Classic statistics example:
- Linear regression with Bayesian inference
- Compare to frequentist results
- Posterior predictive distribution

### flood_frequency_analysis.py
Hydrologic frequency analysis workflow:
- Load annual peak flow data
- Fit multiple distributions (Weibull, GEV, LogNormal)
- Compare using goodness-of-fit
- Compute design flows with confidence intervals
- Generate flood frequency curve plot

### reliability_analysis.py
Engineering reliability example:
- Define limit state function
- Monte Carlo simulation
- MCMC for parameter uncertainty
- Compute probability of failure

---

## Helper Module

**File:** `notebooks/helper_functions.py`

Utility functions to reduce boilerplate in demos:

```python
from System import Array, Double

def convert_to_dotnet_array(python_list):
    dotnet_array = Array.CreateInstance(Double, len(python_list))
    for i, val in enumerate(python_list):
        dotnet_array[i] = float(val)
    return dotnet_array
```

---

## Documentation Files

### README.md
- Project overview and purpose
- Quick start (5 minutes to first plot)
- Link to full Numerics documentation
- Performance comparison highlights
- Contributing guidelines

---

## Dependencies

### Python Requirements
```
pythonnet>=3.0.0
numpy>=1.20.0
matplotlib>=3.5.0
jupyter>=1.0.0
pandas>=1.3.0  # optional, for data handling examples
```

### .NET Requirements
- .NET 6.0+ Runtime (or .NET Framework 4.8.1 on Windows)
- Numerics.dll (from NuGet or built from source)

---

## Notes

- All demos should work on Windows, Linux, and macOS
- Test on both .NET 6/8 and .NET Framework where applicable
- Include sample datasets for reproducible examples
- Each notebook should be self-contained (run independently)
- Code should be well-commented for educational purposes
