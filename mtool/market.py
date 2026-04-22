import json
from typing import Annotated

import typer

from mtool.core.market import get_ticker_info, get_ticker_history

app = typer.Typer(help="Fetch market data from Yahoo Finance.")


@app.command("ticker")
def cmd_ticker(
    symbols: Annotated[
        list[str],
        typer.Option("--ticker", "-t", help="Ticker symbol (e.g. -t AAPL -t MSFT)"),
    ],
):
    """Fetch ticker data from Yahoo Finance and print as JSON."""
    typer.echo(json.dumps(get_ticker_info(symbols), indent=2))


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
    typer.echo(json.dumps(get_ticker_history(symbols, period), indent=2))
