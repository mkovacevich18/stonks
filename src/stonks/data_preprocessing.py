from __future__ import annotations

import requests
from datetime import datetime, timedelta, timezone
from typing import Any


class Client:
    """Polygon.io API client for fetching stock and options data."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def _make_request(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
        """Internal helper to make GET requests with error handling."""
        if params is None:
            params = {}
        params["apiKey"] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            print(f"[WARN] Request failed for {url}: {exc}")
            return None

    def analyze_option_contract(self, underlying: str, ticker: str) -> dict[str, Any] | None:
        """Fetch Greeks and implied volatility for a specific option contract."""
        url = f"https://api.polygon.io/v3/snapshot/options/{underlying}/{ticker}"
        data = self._make_request(url)
        if not data:
            return None

        results = data.get("results", {})
        if not results:
            print(f"[WARN] No results for option {ticker}")
            return None

        return results

    def get_current_stock_price(self, ticker: str) -> float | None:
        """Fetch the latest stock price."""
        url = f"https://api.polygon.io/v2/last/trade/{ticker}"
        data = self._make_request(url)
        if data and "last" in data:
            return data["last"]["price"]
        return None

    def fetch_raw_option_contracts(self, ticker: str, limit: int = 1000) -> list[dict[str, Any]]:
        """Fetch raw option contracts."""
        base_url = "https://api.polygon.io/v3/reference/options/contracts"
        params = {"underlying_ticker": ticker, "limit": limit}

        contracts: list[dict[str, Any]] = []
        url: str | None = base_url

        while url:
            data = self._make_request(url, params)
            if not data:
                break

            results = data.get("results", [])
            if not results:
                break

            contracts.extend(results)
            url = data.get("next_url")
            params = {}  # Next URL already includes params

        return contracts

    def filter_contracts_by_expiration(
        self, contracts: list[dict[str, Any]], min_days: int = 20, max_days: int = 120
    ) -> list[dict[str, Any]]:
        """Filter option contracts by expiration date range."""
        today = datetime.now(timezone.utc).date()
        min_exp = today + timedelta(days=min_days)
        max_exp = today + timedelta(days=max_days)

        filtered: list[dict[str, Any]] = []
        for contract in contracts:
            exp_date = datetime.strptime(contract["expiration_date"], "%Y-%m-%d").date()
            if min_exp <= exp_date <= max_exp:
                filtered.append(contract)

        return filtered

    def contracts_with_greeks(self, ticker: str, contracts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Enrich contracts with Greeks data."""
        enriched: list[dict[str, Any]] = []
        for contract in contracts:
            greeks_data = self.analyze_option_contract(ticker, contract["ticker"])
            if greeks_data:
                contract["greeks"] = greeks_data
                enriched.append(contract)
        return enriched

    def get_option_contracts(
        self,
        ticker: str,
        limit: int = 1000,
        min_days: int = 20,
        max_days: int = 120,
    ) -> list[dict[str, Any]]:
        """Fetch, filter, and enrich option contracts for a given ticker."""
        raw_contracts = self.fetch_raw_option_contracts(ticker, limit)
        filtered_contracts = self.filter_contracts_by_expiration(raw_contracts, min_days, max_days)
        enriched_contracts = self.contracts_with_greeks(ticker, filtered_contracts)
        return enriched_contracts

    def get_latest_closing_price(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        multiplier: int = 1,
        timespan: str = "day",
    ) -> float | None:
        """Return the latest closing price for the given ticker within a date range."""
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        params = {"adjusted": "true", "sort": "desc", "limit": 1}

        data = self._make_request(url, params)
        if data and "results" in data and data["results"]:
            latest = data["results"][0]
            return latest["c"]

        print(f"[WARN] No closing price data for {symbol} between {from_date} and {to_date}")
        return None
