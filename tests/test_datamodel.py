"""Tests for the root datamodel.py (the official IMC data model)."""

import importlib.util
import json

from conftest import REPO_ROOT

_spec = importlib.util.spec_from_file_location("root_datamodel", REPO_ROOT / "datamodel.py")
dm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dm)


def _make_state():
    depth = dm.OrderDepth()
    depth.buy_orders = {9995: 10, 9990: 5}
    depth.sell_orders = {10005: -10, 10010: -5}
    return dm.TradingState(
        traderData="",
        timestamp=100,
        listings={"EMERALDS": dm.Listing("EMERALDS", "EMERALDS", "XIRECS")},
        order_depths={"EMERALDS": depth},
        own_trades={"EMERALDS": []},
        market_trades={"EMERALDS": []},
        position={"EMERALDS": 3},
        observations=dm.Observation({}, {}),
    )


def test_order_fields_and_repr():
    order = dm.Order("EMERALDS", 10000, -7)
    assert order.symbol == "EMERALDS"
    assert order.price == 10000
    assert order.quantity == -7
    assert "EMERALDS" in str(order)


def test_trading_state_construction():
    state = _make_state()
    assert state.timestamp == 100
    assert state.position["EMERALDS"] == 3
    best_bid = max(state.order_depths["EMERALDS"].buy_orders)
    best_ask = min(state.order_depths["EMERALDS"].sell_orders)
    assert best_bid == 9995
    assert best_ask == 10005


def test_prosperity_encoder_serializes_orders():
    order = dm.Order("TOMATOES", 4999, 5)
    payload = json.dumps({"orders": [order]}, cls=dm.ProsperityEncoder)
    decoded = json.loads(payload)
    assert decoded["orders"][0]["price"] == 4999
