from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests
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


    def contracts_with_valid_greeks(self, ticker: str, contracts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Enrich contracts with Greeks data in parallel and return only those with valid Greeks.
        """
        valid_contracts: list[dict[str, Any]] = []

        def fetch_greeks(contract: dict[str, Any]) -> dict[str, Any] | None:
            greeks_data = self.analyze_option_contract(ticker, contract["ticker"])
            if greeks_data and greeks_data.get("greeks"):
                contract["greeks"] = greeks_data
                return contract
            return None

        with ThreadPoolExecutor(max_workers=10) as executor: 
            futures = [executor.submit(fetch_greeks, c) for c in contracts]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    valid_contracts.append(result)

        return valid_contracts

    def get_option_contracts(
        self,
        ticker: str,
        limit: int = 1000,
        min_days: int = 20,
        max_days: int = 120,
    ) -> pd.DataFrame:
        """
        Fetch, filter, and enrich option contracts for a given ticker.
        Returns a pandas DataFrame instead of a list.
        """
        raw_contracts = self.fetch_raw_option_contracts(ticker, limit)
        filtered_contracts = self.filter_contracts_by_expiration(raw_contracts, min_days, max_days)
        valid_contracts = self.contracts_with_valid_greeks(ticker, filtered_contracts)

        if not valid_contracts:
            return pd.DataFrame()  

        return pd.json_normalize(valid_contracts)

    def get_price_history(
        self,
        ticker: str,
        from_date: str | None = None,
        to_date: str | None = None,
        multiplier: int = 1,
        timespan: str = "day",
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV data for a ticker as a DataFrame.
        - Default range: last 2 years up to today.
        - Returns DataFrame with columns: timestamp, open, high, low, close, volume.
        """
        # Default range = last 2 years
        if from_date is None or to_date is None:
            today = date.today()
            to_date = today.strftime("%Y-%m-%d")
            from_date = (today - relativedelta(years=2)).strftime("%Y-%m-%d")

        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        params = {"adjusted": "true", "sort": "asc", "limit": 50000}

        data = self._make_request(url, params)
        if not data or "results" not in data or not data["results"]:
            print(f"[WARN] No OHLCV data for {ticker} between {from_date} and {to_date}")
            return pd.DataFrame()

        results = pd.DataFrame(data["results"])
        results = results.rename(columns={
            "o": "open",
            "h": "high",
            "l": "low",
            "c": "close",
            "v": "volume",
            "t": "timestamp"
        })
        results["timestamp"] = pd.to_datetime(results["timestamp"], unit="ms")

        return results
