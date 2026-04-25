import sys

import typer

from plutus import expenses
from plutus import setup
from plutus.update import update

app = typer.Typer()
app.add_typer(setup.app, name="setup")
app.add_typer(expenses.app, name="expenses")
app.command()(update)

# market imports yfinance/pandas which are heavy — lazy load for commands that don't need them
if len(sys.argv) < 2 or sys.argv[1] not in ("setup", "update", "serve"):
    from plutus import market

    app.add_typer(market.app, name="market")


@app.command()
def serve(
    port: int = typer.Option(8000, help="Port to serve on"),
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
):
    """Start the plutus web UI."""
    import uvicorn

    from plutus.serve import app as fastapi_app

    uvicorn.run(fastapi_app, host=host, port=port)


if __name__ == "__main__":
    app()
