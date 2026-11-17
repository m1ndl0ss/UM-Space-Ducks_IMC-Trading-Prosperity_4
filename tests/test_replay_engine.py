"""Tests for misc/replay_engine.py against real tutorial data."""

import pandas as pd
import pytest

from conftest import REPO_ROOT

import replay_engine as re_mod
import tutorial_combo

TUTORIAL_PRICES = REPO_ROOT / "Data" / "TUTORIAL" / "prices_round_0_day_-1.csv"
TUTORIAL_TRADES = REPO_ROOT / "Data" / "TUTORIAL" / "trades_round_0_day_-1.csv"


def test_row_to_depth_negates_ask_volumes():
    row = pd.Series(
        {
            "bid_price_1": 9995,
            "bid_volume_1": 10,
            "ask_price_1": 10005,
            "ask_volume_1": 7,
        }
    )
    depth = re_mod.row_to_depth(row)
    assert depth.buy_orders == {9995: 10}
    assert depth.sell_orders == {10005: -7}
    assert re_mod.best_bid_ask(depth) == (9995, 10005)


@pytest.fixture(scope="module")
def tutorial_prices():
    if not TUTORIAL_PRICES.is_file():
        pytest.skip("tutorial data not present")
    return re_mod.read_prices_csv(TUTORIAL_PRICES)


@pytest.fixture(scope="module")
def tutorial_trades():
    if not TUTORIAL_TRADES.is_file():
        pytest.skip("tutorial data not present")
    return re_mod.read_trades_csv(TUTORIAL_TRADES)


def test_read_prices_csv_shape(tutorial_prices):
    assert {"timestamp", "product", "mid_price"} <= set(tutorial_prices.columns)
    assert {"EMERALDS", "TOMATOES"} <= set(tutorial_prices["product"].unique())


def test_market_frame_sorted(tutorial_prices):
    frame = re_mod.market_frame(tutorial_prices, "EMERALDS")
    assert not frame.empty
    assert frame["timestamp"].is_monotonic_increasing


def test_replay_tutorial_trader_respects_position_limit(tutorial_prices, tutorial_trades):
    timestamps = sorted(tutorial_prices["timestamp"].unique())[:300]
    prices_slice = tutorial_prices[tutorial_prices["timestamp"].isin(timestamps)]
    df = re_mod.replay_to_dataframe(
        prices_slice, tutorial_trades, "EMERALDS", tutorial_combo.Trader
    )
    assert not df.empty
    assert {"pos", "cash", "equity", "mid"} <= set(df.columns)
    limit = tutorial_combo.POSITION_LIMIT_EMERALDS
    assert df["pos"].abs().max() <= limit

    summary = re_mod.replay_summary(df, initial_cash=0.0)
    assert set(summary) >= {"ending_pos", "cash", "equity", "pnl"}
    assert summary["ending_pos"] == int(df.iloc[-1]["pos"])
