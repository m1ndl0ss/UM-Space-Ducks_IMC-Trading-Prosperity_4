"""Sanity tests for the Black-Scholes pricing used in the round 3 options work."""

import pytest

import deltaNeutral as dn


def test_norm_cdf_symmetry():
    assert dn.norm_cdf(0.0) == pytest.approx(0.5)
    assert dn.norm_cdf(2.0) + dn.norm_cdf(-2.0) == pytest.approx(1.0)


def test_bs_call_price_above_intrinsic():
    price, delta = dn.bs_call(S=5000.0, K=4500.0, T=0.02, r=0.0, vol=0.2)
    assert price >= 5000.0 - 4500.0
    assert 0.0 <= delta <= 1.0


def test_bs_call_increases_with_volatility():
    lo, _ = dn.bs_call(S=5000.0, K=5000.0, T=0.02, r=0.0, vol=0.1)
    hi, _ = dn.bs_call(S=5000.0, K=5000.0, T=0.02, r=0.0, vol=0.4)
    assert hi > lo


def test_bs_call_deep_itm_delta_near_one():
    _price, delta = dn.bs_call(S=5000.0, K=1000.0, T=0.02, r=0.0, vol=0.2)
    assert delta == pytest.approx(1.0, abs=1e-3)
