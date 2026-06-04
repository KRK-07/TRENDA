from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import yfinance as yf


@dataclass(slots=True)
class MarketDataService:
    lookback_period: str = "6mo"
    live_period: str = "1d"
    live_interval: str = "5m"

    def history(self, symbol: str, period: str | None = None, interval: str | None = None) -> pd.DataFrame:
        ticker = self._normalize_symbol(symbol)
        history_kwargs: dict[str, object] = {
            "period": period or self.lookback_period,
            "auto_adjust": True,
        }
        if interval is not None:
            history_kwargs["interval"] = interval

        frame = yf.Ticker(ticker).history(**history_kwargs)
        if frame.empty:
            raise ValueError(f"No market data found for {ticker}")
        return frame

    def live_history(self, symbol: str) -> pd.DataFrame:
        return self.history(symbol, period=self.live_period, interval=self.live_interval)

    def snapshot(self, symbol: str, live: bool = False) -> dict[str, object]:
        frame = self.live_history(symbol) if live else self.history(symbol)
        close = frame["Close"].dropna()
        if close.empty:
            raise ValueError(f"No close prices found for {symbol}")

        return {
            "symbol": self._normalize_symbol(symbol),
            "last_price": float(close.iloc[-1]),
            "change_pct": float((close.iloc[-1] / close.iloc[-2] - 1) * 100) if len(close) > 1 else 0.0,
            "volume": float(frame["Volume"].dropna().iloc[-1]) if "Volume" in frame and not frame["Volume"].dropna().empty else None,
            "history_points": int(len(close)),
            "live": live,
        }

    def live_snapshot(self, symbol: str) -> dict[str, object]:
        return self.snapshot(symbol, live=True)

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        normalized = symbol.strip().upper()
        if not normalized:
            raise ValueError("Symbol cannot be empty")
        return normalized
