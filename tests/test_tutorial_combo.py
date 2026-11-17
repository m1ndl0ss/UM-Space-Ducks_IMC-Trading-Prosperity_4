"""Behavioural tests for the tutorial Trader on a synthetic book."""

import json

from datamodel import OrderDepth, TradingState

import tutorial_combo


def _state(trader_data=""):
    emeralds = OrderDepth()
    emeralds.buy_orders = {9995: 10, 9990: 5}
    emeralds.sell_orders = {10005: -10, 10010: -5}
    tomatoes = OrderDepth()
    tomatoes.buy_orders = {4998: 8}
    tomatoes.sell_orders = {5002: -8}
    return TradingState(
        traderData=trader_data,
        timestamp=0,
        listings={},
        order_depths={"EMERALDS": emeralds, "TOMATOES": tomatoes},
        own_trades={},
        market_trades={},
        position={},
        observations={},
    )


def test_run_returns_orders_conversions_and_state():
    result, conversions, trader_data = tutorial_combo.Trader().run(_state())
    assert isinstance(result, dict)
    assert isinstance(conversions, int)
    json.loads(trader_data)  # traderData must round-trip as JSON


def test_emerald_orders_within_position_limit():
    result, _conversions, _td = tutorial_combo.Trader().run(_state())
    orders = result.get("EMERALDS", [])
    limit = tutorial_combo.POSITION_LIMIT_EMERALDS
    buy_qty = sum(o.quantity for o in orders if o.quantity > 0)
    sell_qty = sum(-o.quantity for o in orders if o.quantity < 0)
    assert buy_qty <= limit
    assert sell_qty <= limit


def test_trader_state_accumulates_tomato_mids():
    trader = tutorial_combo.Trader()
    _result, _conversions, td1 = trader.run(_state())
    _result, _conversions, td2 = trader.run(_state(td1))
    mids1 = json.loads(td1).get("tomatoes", [])
    mids2 = json.loads(td2).get("tomatoes", [])
    assert len(mids2) >= len(mids1)
