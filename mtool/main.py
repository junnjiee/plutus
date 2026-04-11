import typer

from mtool import expenses
from mtool import market

app = typer.Typer()
app.add_typer(expenses.app, name="expenses")
app.add_typer(market.app, name="market")


if __name__ == "__main__":
    app()
