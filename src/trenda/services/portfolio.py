from __future__ import annotations

from dataclasses import dataclass

from trenda.schemas import PortfolioRequest
from trenda.services.market_data import MarketDataService


@dataclass(slots=True)
class PortfolioService:
    market_data_service: MarketDataService

    def analyze(self, request: PortfolioRequest) -> dict[str, object]:
        positions: list[dict[str, object]] = []
        portfolio_value = float(request.cash)
        total_cost = float(request.cash)

        for holding in request.holdings:
            snapshot = self.market_data_service.snapshot(holding.symbol)
            market_value = float(snapshot["last_price"]) * holding.quantity
            cost_basis = holding.average_cost * holding.quantity
            unrealized_pnl = market_value - cost_basis

            positions.append(
                {
                    "symbol": snapshot["symbol"],
                    "quantity": holding.quantity,
                    "last_price": snapshot["last_price"],
                    "market_value": round(market_value, 2),
                    "cost_basis": round(cost_basis, 2),
                    "unrealized_pnl": round(unrealized_pnl, 2),
                }
            )

            portfolio_value += market_value
            total_cost += cost_basis

        return {
            "portfolio_value": round(portfolio_value, 2),
            "total_cost": round(total_cost, 2),
            "unrealized_pnl": round(portfolio_value - total_cost, 2),
            "positions": positions,
        }
