import sys

import typer

from mtool import expenses
from mtool import setup
from mtool.update import update

app = typer.Typer()
app.add_typer(expenses.app, name="expenses")
app.add_typer(setup.app, name="setup")
app.command()(update)

# market imports yfinance/pandas which are heavy — lazy load for commands that don't need them
if len(sys.argv) < 2 or sys.argv[1] not in ("setup", "update"):
    from mtool import market

    app.add_typer(market.app, name="market")


if __name__ == "__main__":
    app()
