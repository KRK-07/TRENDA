import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from trenda.schemas import BacktestRequest, BacktestResponse, PortfolioRequest, SignalResponse
from trenda.services.backtest import BacktestService
from trenda.services.market_data import MarketDataService
from trenda.services.portfolio import PortfolioService
from trenda.services.signals import SignalService

app = FastAPI(title="Trenda", version="0.1.0")

allowed_origins = [
    origin.strip()
    for origin in os.environ.get("TRRENDA_ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

market_data_service = MarketDataService()
signal_service = SignalService(market_data_service)
portfolio_service = PortfolioService(market_data_service)
backtest_service = BacktestService(market_data_service)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "trenda-api",
        "message": "Deploy the frontend separately on Vercel and point it at this API.",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/market/{symbol}")
def market_snapshot(symbol: str) -> dict[str, object]:
    try:
        return market_data_service.snapshot(symbol)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/market/live/{symbol}")
def live_market_snapshot(symbol: str) -> dict[str, object]:
    try:
        return market_data_service.live_snapshot(symbol)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/signals/{symbol}", response_model=SignalResponse)
def signal_snapshot(symbol: str) -> SignalResponse:
    try:
        return signal_service.build_signal(symbol)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/signals/live/{symbol}", response_model=SignalResponse)
def live_signal_snapshot(symbol: str) -> SignalResponse:
    try:
        return signal_service.build_live_signal(symbol)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/portfolio/analyze")
def analyze_portfolio(request: PortfolioRequest) -> dict[str, object]:
    try:
        return portfolio_service.analyze(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/backtest", response_model=BacktestResponse)
def run_backtest(request: BacktestRequest) -> BacktestResponse:
    try:
        return backtest_service.run(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
