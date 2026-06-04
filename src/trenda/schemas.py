from __future__ import annotations

from pydantic import BaseModel, Field


class Holding(BaseModel):
    symbol: str
    quantity: float = Field(gt=0)
    average_cost: float = Field(gt=0)


class PortfolioRequest(BaseModel):
    holdings: list[Holding]
    cash: float = Field(default=0, ge=0)


class BacktestRequest(BaseModel):
    symbol: str
    initial_cash: float = Field(default=10_000, gt=0)
    short_window: int = Field(default=10, ge=2)
    long_window: int = Field(default=30, ge=3)
    transaction_cost_bps: float = Field(default=0, ge=0)


class SignalResponse(BaseModel):
    symbol: str
    action: str
    confidence: float
    last_price: float
    short_sma: float
    long_sma: float
    rsi: float
    volatility: float
    trend_strength: float
    rationale: str


class BacktestResponse(BaseModel):
    symbol: str
    initial_cash: float
    ending_value: float
    total_return_pct: float
    buy_and_hold_return_pct: float
    max_drawdown_pct: float
    trades: int
    strategy_curve: list[float]
    buy_and_hold_curve: list[float]
