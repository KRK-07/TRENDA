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
3. Open `http://127.0.0.1:8000/docs` for the API docs.
4. Open `frontend/index.html` in a browser and set the API base URL to `http://127.0.0.1:8000`.

## Deploy Frontend and Backend Separately

This repository now supports a split deployment:

- Backend on Render
- Frontend on Vercel

### Backend on Render

1. Push this repository to GitHub.
2. In Render, create a new Web Service from the repo.
3. Set the root directory to the repository root.
4. Use the build command `pip install .`.
5. Use the start command `uvicorn trenda.main:app --host 0.0.0.0 --port 10000`.
6. Deploy the service.

### Frontend on Vercel

1. In Vercel, create a new project from the same GitHub repo.
2. Set the root directory to `frontend`.
3. Deploy the project as a static site.
4. After deployment, open the site and paste your Render API URL into the `API base URL` field.
5. Save it once. The value is stored in the browser and reused for live polling.

### CORS

The backend allows cross-origin requests so the Vercel frontend can call the Render API. If you want to restrict it, set `TRRENDA_ALLOWED_ORIGINS` on Render to your Vercel domain.

## Endpoints

- `GET /`
- `GET /health`
- `GET /market/{symbol}`
- `GET /market/live/{symbol}`
- `GET /signals/{symbol}`
- `GET /signals/live/{symbol}`
- `POST /portfolio/analyze`
- `POST /backtest`
