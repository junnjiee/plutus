import json
from typing import Annotated

import typer
import yfinance as yf

app = typer.Typer(help="Fetch market data from Yahoo Finance.")


@app.command("ticker")
def cmd_ticker(
    symbols: Annotated[
        list[str],
        typer.Option("--ticker", "-t", help="Ticker symbol (e.g. -t AAPL -t MSFT)"),
    ],
):
    """Fetch ticker data from Yahoo Finance and print as JSON."""
    results = {}
    for symbol in symbols:
        t = yf.Ticker(symbol)
        info = t.info
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        if price is None:
            results[symbol.upper()] = {"error": "No price available"}
            continue
        results[symbol.upper()] = {
            "name": info.get("shortName"),
            "price": price,
            "currency": info.get("currency"),
            "market_cap": info.get("marketCap"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "pe_ratio": info.get("trailingPE"),
            "dividend_yield": info.get("dividendYield"),
            "sector": info.get("sector"),
        }
    typer.echo(json.dumps(results, indent=2))


@app.command("history")
def cmd_history(
    symbols: Annotated[
        list[str],
        typer.Option("--ticker", "-t", help="Ticker symbol (e.g. -t AAPL -t MSFT)"),
    ],
    period: Annotated[
        str,
        typer.Option("--period", "-p", help="Period: 1mo, 3mo, 6mo, 1y, 2y, 5y"),
    ] = "1y",
):
    """Fetch historical performance for tickers over a given period."""
    results = {}
    for symbol in symbols:
        t = yf.Ticker(symbol)
        hist = t.history(period=period)
        if hist.empty:
            results[symbol.upper()] = {"error": "No data available"}
            continue
        start_price = hist["Close"].iloc[0]
        end_price = hist["Close"].iloc[-1]

        total_return = (end_price - start_price) / start_price
        trading_days = len(hist)
        annualized_return = (1 + total_return) ** (252 / trading_days) - 1

        results[symbol.upper()] = {
            "period": period,
            "start_date": str(hist.index[0].date()),
            "end_date": str(hist.index[-1].date()),
            "start_price": round(float(start_price), 2),
            "end_price": round(float(end_price), 2),
            "total_return_pct": round(total_return * 100, 2),
            "annualized_return_pct": round(annualized_return * 100, 2),
        }
    typer.echo(json.dumps(results, indent=2))
