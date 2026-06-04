from __future__ import annotations

import pandas as pd

from trenda.schemas import SignalResponse
from trenda.services.market_data import MarketDataService


class SignalService:
    def __init__(self, market_data_service: MarketDataService) -> None:
        self.market_data_service = market_data_service

    def build_signal(self, symbol: str, live: bool = False) -> SignalResponse:
        if live:
            frame = self.market_data_service.live_history(symbol)
            close = frame["Close"].dropna()
            if len(close) < 30:
                # fallback to longer history when intraday data is too short
                frame = self.market_data_service.history(symbol)
                close = frame["Close"].dropna()
        else:
            frame = self.market_data_service.history(symbol)
            close = frame["Close"].dropna()

        if len(close) < 30:
            raise ValueError("Not enough history to generate a signal")

        short_sma = float(close.rolling(window=10).mean().iloc[-1])
        long_sma = float(close.rolling(window=30).mean().iloc[-1])
        last_price = float(close.iloc[-1])
        returns = close.pct_change().dropna()
        volatility = float(returns.std() * (252**0.5)) if not returns.empty else 0.0
        rsi = self._calculate_rsi(close)
        trend_strength = (short_sma - long_sma) / long_sma if long_sma else 0.0

        momentum_score = self._score_from_rsi(rsi)
        trend_score = self._score_from_trend(trend_strength)
        volatility_penalty = min(0.2, volatility / 5)
        confidence = max(0.05, min(0.95, 0.5 + (0.4 * trend_score) + (0.1 * momentum_score) - volatility_penalty))

        if trend_score > 0.25:
            action = "buy"
            rationale = "Uptrend is intact; RSI is used as a confidence filter rather than a veto."
        elif trend_score < -0.25:
            action = "sell"
            rationale = "Downtrend is intact; momentum remains weak."
        else:
            action = "hold"
            rationale = "Trend is not strong enough to justify a directional trade."

        return SignalResponse(
            symbol=symbol.strip().upper(),
            action=action,
            confidence=round(float(confidence), 4),
            last_price=round(last_price, 4),
            short_sma=round(short_sma, 4),
            long_sma=round(long_sma, 4),
            rsi=round(float(rsi), 4),
            volatility=round(float(volatility), 4),
            trend_strength=round(float(trend_strength), 6),
            rationale=rationale,
        )

    def build_live_signal(self, symbol: str) -> SignalResponse:
        return self.build_signal(symbol, live=True)

    @staticmethod
    def _calculate_rsi(close: pd.Series, window: int = 14) -> float:
        delta = close.diff().dropna()
        if delta.empty:
            return 50.0

        gains = delta.clip(lower=0).rolling(window=window).mean()
        losses = (-delta.clip(upper=0)).rolling(window=window).mean()
        average_gain = gains.iloc[-1]
        average_loss = losses.iloc[-1]

        if pd.isna(average_gain) or pd.isna(average_loss):
            return 50.0
        if average_loss == 0:
            return 100.0

        relative_strength = average_gain / average_loss
        return float(100 - (100 / (1 + relative_strength)))

    @staticmethod
    def _score_from_rsi(rsi: float) -> float:
        if rsi < 30:
            return 1.0
        if rsi > 70:
            return -1.0
        return (50 - rsi) / 20

    @staticmethod
    def _score_from_trend(trend_strength: float) -> float:
        if trend_strength >= 0.05:
            return 1.0
        if trend_strength <= -0.05:
            return -1.0
        return trend_strength / 0.05
