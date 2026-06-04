import pandas as pd
from fastapi.testclient import TestClient

from trenda.main import app
from trenda.schemas import BacktestRequest, Holding, PortfolioRequest, SignalResponse
from trenda.services.backtest import BacktestService
from trenda.services.market_data import MarketDataService
from trenda.services.signals import SignalService


def test_holding_requires_positive_quantity() -> None:
    try:
        Holding(symbol="AAPL", quantity=0, average_cost=100)
    except Exception as exc:
        assert "greater than 0" in str(exc)
    else:
        raise AssertionError("Expected validation to fail")


def test_portfolio_request_accepts_cash_and_holdings() -> None:
    request = PortfolioRequest(holdings=[Holding(symbol="AAPL", quantity=2, average_cost=100)], cash=50)
    assert request.cash == 50
    assert request.holdings[0].symbol == "AAPL"


class StubMarketDataService(MarketDataService):
    def __init__(self, frame: pd.DataFrame) -> None:
        super().__init__()
        self._frame = frame

    def history(self, symbol: str, period: str | None = None, interval: str | None = None) -> pd.DataFrame:
        return self._frame


def test_signal_service_produces_buy_signal_on_uptrend() -> None:
    frame = pd.DataFrame({"Close": list(range(1, 61)), "Volume": [1_000] * 60})
    service = SignalService(StubMarketDataService(frame))

    signal = service.build_signal("aapl")

    assert signal.symbol == "AAPL"
    assert signal.action == "buy"
    assert signal.confidence > 0.5
    assert signal.rsi >= 50


def test_backtest_service_runs_with_synthetic_prices() -> None:
    frame = pd.DataFrame({"Close": [100 + index for index in range(80)]})
    service = BacktestService(StubMarketDataService(frame))

    response = service.run(BacktestRequest(symbol="msft", initial_cash=1_000, short_window=5, long_window=20))

    assert response.symbol == "MSFT"
    assert response.initial_cash == 1_000
    assert response.trades >= 1
    assert len(response.strategy_curve) == len(frame)


def test_dashboard_page_is_served() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "Trenda Control Center" in response.text
    assert "signal-form" in response.text
    assert "Live polling" in response.text
    assert "Poll interval" in response.text
    assert "Watchlist" in response.text


def test_vercel_entrypoint_exposes_app() -> None:
    from api.index import app as vercel_app

    assert vercel_app is app


def test_live_market_endpoint_uses_live_snapshot(monkeypatch) -> None:
    client = TestClient(app)

    monkeypatch.setattr(
        MarketDataService,
        "live_snapshot",
        lambda self, symbol: {"symbol": symbol.upper(), "last_price": 123.45, "change_pct": 1.2, "volume": 999, "history_points": 2, "live": True},
    )

    response = client.get("/market/live/aapl")

    assert response.status_code == 200
    assert response.json()["live"] is True
    assert response.json()["symbol"] == "AAPL"


def test_live_signal_endpoint_uses_live_signal(monkeypatch) -> None:
    client = TestClient(app)

    monkeypatch.setattr(
        SignalService,
        "build_live_signal",
        lambda self, symbol: SignalResponse(
            symbol=symbol.upper(),
            action="hold",
            confidence=0.5,
            last_price=10.0,
            short_sma=9.0,
            long_sma=9.5,
            rsi=50.0,
            volatility=0.2,
            trend_strength=0.0,
            rationale="stub",
        ),
    )

    response = client.get("/signals/live/aapl")

    assert response.status_code == 200
    assert response.json()["symbol"] == "AAPL"
    assert response.json()["action"] == "hold"
