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

## Deploy on Vercel

Trenda is configured to run as a Python serverless app on Vercel.

1. Push this repository to GitHub.
2. Import the repo into Vercel.
3. Keep the default framework detection off and let Vercel use `vercel.json`.
4. Deploy the project using the Python runtime.

The deployment uses `api/index.py` as the entrypoint and rewrites all routes to the FastAPI app, so the dashboard still loads at `/` and the API remains available under the same paths.

## Endpoints

- `GET /health`
- `GET /`
- `GET /market/{symbol}`
- `GET /market/live/{symbol}`
- `GET /signals/{symbol}`
- `GET /signals/live/{symbol}`
- `POST /portfolio/analyze`
- `POST /backtest`
