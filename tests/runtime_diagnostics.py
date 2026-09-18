"""Fast real-assembly interop/oracle check for notebook 06 diagnostics."""

from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "notebooks"))
from helper_functions import load_numerics

load_numerics()

from System import Array, Double
from System.Collections.Generic import List
from Numerics.Mathematics.Optimization import ParameterSet
from Numerics.Sampling.MCMC import MCMCDiagnostics
from benchmark_support import posterior_diagnostics

draws = np.random.default_rng(7634).normal(size=(4, 512, 2))
chains = Array[List[ParameterSet]]([
    List[ParameterSet](Array[ParameterSet]([
        ParameterSet(Array[Double](values), 0.0) for values in chain
    ])) for chain in draws
])
ess, average_acf = MCMCDiagnostics.EffectiveSampleSize(chains)
rhat = MCMCDiagnostics.GelmanRubin(chains)
reference = posterior_diagnostics(draws, ["x", "y"])
np.testing.assert_allclose(list(ess), reference["ESS conservative"], rtol=0.02)
np.testing.assert_allclose(list(rhat), reference["R-hat"], rtol=1e-6)
assert len(average_acf) == 2
print("Numerics/ArviZ multi-chain ESS and R-hat agree; managed out-parameter binding passed.")
