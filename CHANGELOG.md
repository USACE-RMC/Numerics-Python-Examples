# Changelog

## v1.0.1 - Unreleased

### Highlights

- Upgrade all 13 notebooks and three standalone examples to the exact published
  `RMC.Numerics 2.2.0` NuGet package and .NET 10.
- Add an inline C# likelihood compiled with Roslyn and bound directly to a managed
  delegate, enabling parallel MCMC chains without Python callback overhead.
- Compare Python/sequential, compiled-C#/sequential, compiled-C#/parallel, and PyMC
  NUTS, with a discussion of the analogous RStan compiled-model workflow.
- Refresh NUTS and Random Forest benchmarks using untimed warm-up, three measured
  repetitions, median/range reporting, and recorded environment information.

### Correctness and reproducibility

- Exclude warmup from posterior summaries and preserve chain boundaries when
  computing rank-normalized R-hat, bulk/tail ESS, and Monte Carlo standard errors.
- Report NUTS acceptance, step size, divergences, tree-depth behavior, and E-BFMI;
  distinguish retained draws from total transitions.
- Compare Random Forest mean regression predictions and document classification
  aggregation, split-criterion, and prediction-work differences between libraries.
- Centralize .NET loading, pin package resolution, validate assembly identity and
  target framework, and retain an explicit validated local-DLL override.
- Add fresh-kernel notebook/script validation, runtime checks, and helper tests.
  Refresh maintained benchmark outputs and clear stale outputs elsewhere.

### Reference results

Quiet-machine NUTS sampling medians for the included Normal model were:

| Mode | Sampling time |
| --- | --- |
| Python callback / sequential | 4.5966 s |
| Compiled C# / sequential | 0.0491 s |
| Compiled C# / parallel | 0.0698 s |

Compiled sequential sampling was about 94 times faster than the Python callback
on this workload. Parallel execution was slower than compiled sequential execution
for this small likelihood. Roslyn compilation plus assembly load took 0.4464 s
once and is excluded from sampling times. PyMC ran without its optional C++ compiler;
its timings do not represent an optimized compiled PyMC installation.

All 13 notebooks, all three scripts, 11 helper/CLI tests, and the runtime and
diagnostic checks passed during release preparation. Likelihood parity and
bitwise-identical seeded draws passed across the three Numerics modes. See the
[validation report](docs/validation/2026-09-18-numerics-2.2-validation.md) for
Random Forest results, timing ranges, diagnostics, environment, and limitations.

### Upgrade

Install the .NET 10 SDK and refresh the Python environment using
`notebook-requirements.txt`. Python 3.12 is the validated release environment.
Restore the pinned package from the repository root:

```powershell
dotnet restore dotnet/NumericsRuntime.csproj --configfile NuGet.config --no-cache
```

Restart existing notebook kernels before loading the new runtime or assembly.
Older .NET targets are no longer supported by these examples. No Numerics library
algorithms, priors, or tolerances were changed by this examples update.
