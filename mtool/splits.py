import json
from typing import Annotated, Optional

import typer

from mtool.db.splits import (
    add_participant,
    add_split,
    delete_split,
    get_balance,
    get_split,
    list_splits,
    update_participant,
)

app = typer.Typer(help="Track shared expenses and what others owe you.")


@app.command("add")
def cmd_add(
    name: Annotated[str, typer.Argument(help="Split name (e.g. 'Tokyo dinner')")],
    total_amount: Annotated[float, typer.Argument(help="Total amount paid")],
    currency: Annotated[str, typer.Argument(help="Currency code (e.g. SGD, USD)")],
    split_type: Annotated[
        str,
        typer.Argument(help="How to split: equal, exact, percentage, shares"),
    ],
    date: Annotated[
        Optional[str],
        typer.Option("--date", "-d", help="Date (YYYY-MM-DD). Defaults to today."),
    ] = None,
):
    """Create a new split expense."""
    try:
        row = add_split(
            name,
            total_amount,
            currency,
            split_type,
            split_date=date,
        )
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    typer.echo(json.dumps(row, indent=2))


@app.command("add-participant")
def cmd_add_participant(
    split_id: Annotated[int, typer.Argument(help="Split ID to add participant to")],
    name: Annotated[str, typer.Argument(help="Participant name")],
    original_amount_owed: Annotated[float, typer.Argument(help="Their share of the split")],
    amount_owed: Annotated[
        Optional[float],
        typer.Option("--amount-owed", help="Current amount owed. Defaults to original_amount_owed. Pass 0 for the paying user."),
    ] = None,
):
    """Add a participant to an existing split."""
    try:
        row = add_participant(split_id, name, original_amount_owed, amount_owed=amount_owed)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    typer.echo(json.dumps(row, indent=2))


@app.command("show")
def cmd_show(
    split_id: Annotated[int, typer.Argument(help="Split ID to show")],
):
    """Show a single split with all its participants."""
    row = get_split(split_id)
    if row is None:
        typer.echo(f"No split found with id {split_id}.", err=True)
        raise typer.Exit(1)
    typer.echo(json.dumps(row, indent=2))


@app.command("list")
def cmd_list(
    person: Annotated[
        Optional[str], typer.Option("--person", "-p", help="Filter by participant name")
    ] = None,
    settled: Annotated[
        Optional[bool],
        typer.Option("--settled/--unsettled", help="Filter by settled status"),
    ] = None,
    date_from: Annotated[
        Optional[str], typer.Option("--from", help="Start date (YYYY-MM-DD)")
    ] = None,
    date_to: Annotated[
        Optional[str], typer.Option("--to", help="End date (YYYY-MM-DD)")
    ] = None,
    limit: Annotated[int, typer.Option("--limit", "-n")] = 50,
):
    """List splits with optional filters. Returns splits with nested participants."""
    rows = list_splits(
        person=person,
        settled=settled,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
    )
    typer.echo(json.dumps(rows, indent=2))


@app.command("balance")
def cmd_balance(
    person: Annotated[
        Optional[str],
        typer.Option("--person", "-p", help="Show balance for a specific person only"),
    ] = None,
):
    """Show outstanding balance per person (grouped by currency)."""
    rows = get_balance(person=person)
    typer.echo(json.dumps(rows, indent=2))


@app.command("edit-participant")
def cmd_edit_participant(
    participant_id: Annotated[int, typer.Argument(help="Participant ID to edit")],
    name: Annotated[Optional[str], typer.Option("--name", "-n")] = None,
    original_amount_owed: Annotated[
        Optional[float], typer.Option("--original-amount")
    ] = None,
    amount_owed: Annotated[Optional[float], typer.Option("--amount-owed")] = None,
):
    """Update a participant's fields."""
    fields = {
        k: v
        for k, v in {
            "name": name,
            "original_amount_owed": original_amount_owed,
            "amount_owed": amount_owed,
        }.items()
        if v is not None
    }
    if not fields:
        typer.echo("No fields to update.", err=True)
        raise typer.Exit(1)
    row = update_participant(participant_id, **fields)
    if row is None:
        typer.echo(f"No participant found with id {participant_id}.", err=True)
        raise typer.Exit(1)
    typer.echo(json.dumps(row, indent=2))


@app.command("delete")
def cmd_delete(
    split_id: Annotated[int, typer.Argument(help="Split ID to delete")],
    yes: Annotated[
        bool, typer.Option("--yes", "-y", help="Skip confirmation prompt")
    ] = False,
):
    """Delete a split and all its participants."""
    if not yes:
        typer.confirm(f"Delete split {split_id} and all its participants?", abort=True)
    deleted = delete_split(split_id)
    if not deleted:
        typer.echo(f"No split found with id {split_id}.", err=True)
        raise typer.Exit(1)
    typer.echo(f"Deleted split {split_id}.")
