import json
from typing import Annotated, Optional
import typer
from mtool.db.expenses import add_expense, list_expenses, update_expense, delete_expense

app = typer.Typer(help="Manage expenses in a local database.")


@app.command("add")
def cmd_add(
    amount: Annotated[float, typer.Argument(help="Expense amount")],
    currency: Annotated[str, typer.Argument(help="Currency code (e.g. USD, CAD)")],
    date: Annotated[
        Optional[str],
        typer.Option("--date", "-d", help="Date (YYYY-MM-DD). Defaults to today."),
    ] = None,
    category: Annotated[Optional[str], typer.Option("--category", "-c")] = None,
    merchant: Annotated[Optional[str], typer.Option("--merchant", "-m")] = None,
    description: Annotated[
        Optional[str], typer.Option("--description", "--desc")
    ] = None,
    account: Annotated[Optional[str], typer.Option("--account", "-a")] = None,
):
    """Add a new expense."""
    row = add_expense(
        amount,
        currency,
        expense_date=date,
        category=category,
        merchant=merchant,
        description=description,
        account=account,
    )
    typer.echo(json.dumps(row, indent=2))


@app.command("list")
def cmd_list(
    date_from: Annotated[
        Optional[str], typer.Option("--from", help="Start date (YYYY-MM-DD)")
    ] = None,
    date_to: Annotated[
        Optional[str], typer.Option("--to", help="End date (YYYY-MM-DD)")
    ] = None,
    category: Annotated[Optional[str], typer.Option("--category", "-c")] = None,
    currency: Annotated[Optional[str], typer.Option("--currency")] = None,
    merchant: Annotated[Optional[str], typer.Option("--merchant", "-m")] = None,
    amount_min: Annotated[Optional[float], typer.Option("--min")] = None,
    amount_max: Annotated[Optional[float], typer.Option("--max")] = None,
    limit: Annotated[int, typer.Option("--limit", "-n")] = 50,
):
    """List expenses with optional filters."""
    rows = list_expenses(
        date_from=date_from,
        date_to=date_to,
        category=category,
        currency=currency,
        merchant=merchant,
        amount_min=amount_min,
        amount_max=amount_max,
        limit=limit,
    )
    typer.echo(json.dumps(rows, indent=2))


@app.command("update")
def cmd_update(
    id: Annotated[int, typer.Argument(help="Expense ID to update")],
    amount: Annotated[Optional[float], typer.Option("--amount")] = None,
    currency: Annotated[Optional[str], typer.Option("--currency")] = None,
    date: Annotated[Optional[str], typer.Option("--date", "-d")] = None,
    category: Annotated[Optional[str], typer.Option("--category", "-c")] = None,
    merchant: Annotated[Optional[str], typer.Option("--merchant", "-m")] = None,
    description: Annotated[
        Optional[str], typer.Option("--description", "--desc")
    ] = None,
    account: Annotated[Optional[str], typer.Option("--account", "-a")] = None,
):
    """Update fields on an existing expense."""
    fields = {
        k: v
        for k, v in {
            "amount": amount,
            "currency": currency,
            "date": date,
            "category": category,
            "merchant": merchant,
            "description": description,
            "account": account,
        }.items()
        if v is not None
    }

    if not fields:
        typer.echo("No fields to update.", err=True)
        raise typer.Exit(1)

    row = update_expense(id, **fields)
    if row is None:
        typer.echo(f"No expense found with id {id}.", err=True)
        raise typer.Exit(1)
    typer.echo(json.dumps(row, indent=2))


@app.command("delete")
def cmd_delete(
    id: Annotated[int, typer.Argument(help="Expense ID to delete")],
    yes: Annotated[
        bool, typer.Option("--yes", "-y", help="Skip confirmation prompt")
    ] = False,
):
    """Delete an expense by ID."""
    if not yes:
        typer.confirm(f"Delete expense {id}?", abort=True)
    deleted = delete_expense(id)
    if not deleted:
        typer.echo(f"No expense found with id {id}.", err=True)
        raise typer.Exit(1)
    typer.echo(f"Deleted expense {id}.")
