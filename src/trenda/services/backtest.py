from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from trenda.schemas import BacktestRequest, BacktestResponse
from trenda.services.market_data import MarketDataService


@dataclass(slots=True)
class BacktestService:
    market_data_service: MarketDataService

    def run(self, request: BacktestRequest) -> BacktestResponse:
        if request.long_window <= request.short_window:
            raise ValueError("long_window must be greater than short_window")

        frame = self.market_data_service.history(request.symbol)
        close = frame["Close"].dropna()
        if len(close) < request.long_window + 1:
            raise ValueError("Not enough history to run the backtest")

        strategy_curve, buy_and_hold_curve, trades = self._simulate(
            close=close,
            initial_cash=request.initial_cash,
            short_window=request.short_window,
            long_window=request.long_window,
            transaction_cost_bps=request.transaction_cost_bps,
        )

        ending_value = strategy_curve[-1]
        buy_and_hold_ending_value = buy_and_hold_curve[-1]
        peak = strategy_curve[0]
        max_drawdown = 0.0
        for value in strategy_curve:
            peak = max(peak, value)
            drawdown = (peak - value) / peak if peak else 0.0
            max_drawdown = max(max_drawdown, drawdown)

        return BacktestResponse(
            symbol=request.symbol.strip().upper(),
            initial_cash=request.initial_cash,
            ending_value=round(float(ending_value), 2),
            total_return_pct=round(float((ending_value / request.initial_cash - 1) * 100), 4),
            buy_and_hold_return_pct=round(float((buy_and_hold_ending_value / request.initial_cash - 1) * 100), 4),
            max_drawdown_pct=round(float(max_drawdown * 100), 4),
            trades=trades,
            strategy_curve=[round(float(value), 2) for value in strategy_curve],
            buy_and_hold_curve=[round(float(value), 2) for value in buy_and_hold_curve],
        )

    def _simulate(
        self,
        *,
        close: pd.Series,
        initial_cash: float,
        short_window: int,
        long_window: int,
        transaction_cost_bps: float,
    ) -> tuple[list[float], list[float], int]:
        short_ma = close.rolling(window=short_window).mean()
        long_ma = close.rolling(window=long_window).mean()
        position = 0
        strategy_value = initial_cash
        buy_and_hold_value = initial_cash
        strategy_curve: list[float] = [initial_cash]
        buy_and_hold_curve: list[float] = [initial_cash]
        entry_price = float(close.iloc[0])
        trades = 0

        for index in range(1, len(close)):
            price = float(close.iloc[index])
            buy_and_hold_value = initial_cash * (price / entry_price)
            buy_and_hold_curve.append(buy_and_hold_value)

            if pd.isna(short_ma.iloc[index]) or pd.isna(long_ma.iloc[index]):
                strategy_curve.append(strategy_value)
                continue

            target_position = 1 if short_ma.iloc[index] > long_ma.iloc[index] else 0
            if target_position != position:
                trades += 1
                trade_cost = strategy_value * (transaction_cost_bps / 10_000)
                strategy_value -= trade_cost
                position = target_position

            if position == 1:
                previous_price = float(close.iloc[index - 1])
                strategy_value *= price / previous_price

            strategy_curve.append(strategy_value)

        return strategy_curve, buy_and_hold_curve, trades