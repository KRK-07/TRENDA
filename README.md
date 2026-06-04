# Trenda

Trenda is an AI-assisted financial analysis and trading signal workspace.

It starts as a Python API for:

- market data ingestion
- technical signal generation
- portfolio analytics
- historical backtesting
- strategy-ready AI summaries

## Stack

- FastAPI for the HTTP API
- Pydantic for typed schemas
- pandas and numpy for analysis
- yfinance as the initial market-data adapter

## Run locally

1. Install dependencies.
2. Start the API with `uvicorn trenda.main:app --reload`.
3. Open `http://127.0.0.1:8000/` for the dashboard or `http://127.0.0.1:8000/docs` for the API docs.
4. Leave the dashboard open to let the live polling panel refresh market data every 30 seconds.

## Endpoints

- `GET /health`
- `GET /`
- `GET /market/{symbol}`
- `GET /market/live/{symbol}`
- `GET /signals/{symbol}`
- `GET /signals/live/{symbol}`
- `POST /portfolio/analyze`
- `POST /backtest`
