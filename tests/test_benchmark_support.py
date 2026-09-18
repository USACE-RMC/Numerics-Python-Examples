"""Guard the chain boundaries and warmup convention used in timing reports."""

from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "notebooks"))
from benchmark_support import posterior_chains, posterior_diagnostics


def test_retained_draws_exclude_warmup_and_append_output_per_chain():
    # Deliberately separated ranges expose flattening, dropped Output, and
    # off-by-one warmup errors independently of any random sampler result.
    def states(values):
        return [SimpleNamespace(Values=[value, -value]) for value in values]

    sampler = SimpleNamespace(
        ThinningInterval=1, WarmupIterations=2,
        MarkovChains=[states([90, 91, 1, 2]), states([92, 93, 11, 12])],
        Output=[states([3, 4]), states([13, 14])],
    )
    expected = [[[1, -1], [2, -2], [3, -3], [4, -4]],
                [[11, -11], [12, -12], [13, -13], [14, -14]]]
    np.testing.assert_array_equal(posterior_chains(sampler), expected)
    sampler.ThinningInterval = 2
    with pytest.raises(ValueError, match="ThinningInterval=1"):
        posterior_chains(sampler)


@pytest.mark.parametrize("shape", [(1, 100, 2), (4, 3, 2), (0, 100, 2)])
def test_diagnostics_reject_too_few_chains_or_draws(shape):
    with pytest.raises(ValueError, match="at least two chains and four draws"):
        posterior_diagnostics(np.zeros(shape), ["mu", "sigma"])


def test_diagnostics_preserve_chains_and_parameter_columns():
    # One parameter has chains stuck in separated locations: flattening would
    # hide this failure. The other is stationary independent Normal noise.
    rng = np.random.default_rng(97531)
    values = rng.normal(size=(4, 1000, 2))
    values[:, :, 1] += np.arange(4)[:, None] * 10
    report = posterior_diagnostics(values, ["stationary", "stuck"]).set_index("Parameter")
    assert report.loc["stationary", "R-hat"] < 1.01
    assert report.loc["stuck", "R-hat"] > 1.5
    assert report.loc["stationary", "ESS conservative"] > 1000
    assert report.loc["stuck", "ESS conservative"] < 20
    np.testing.assert_allclose(report["Mean"], values.mean(axis=(0, 1)))
    np.testing.assert_allclose(report["ESS conservative"], report[["ESS bulk", "ESS tail"]].min(axis=1))


def test_diagnostics_reject_nonfinite_draws_and_wrong_parameter_count():
    values = np.ones((4, 100, 2))
    with pytest.raises(ValueError, match="matching names"):
        posterior_diagnostics(values, ["only_one"])
    values[0, 0, 0] = np.nan
    with pytest.raises(ValueError, match="non-finite"):
        posterior_diagnostics(values, ["mu", "sigma"])
