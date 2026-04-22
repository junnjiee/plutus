"""Tool handlers for the finance-agent Hermes plugin."""

import json

from core.expenses import (
    add_expense as core_add_expense,
    delete_expense as core_delete_expense,
    get_expense_by_email_id as core_get_expense_by_email_id,
    list_expenses as core_list_expenses,
    update_expense as core_update_expense,
)
from core.market import (
    get_ticker_data as core_get_ticker_data,
    get_ticker_history as core_get_ticker_history,
)


def _ok(data) -> str:
    return json.dumps({"ok": True, "data": data}, indent=2, default=str)


def _error(message: str, *, details=None) -> str:
    payload = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    return json.dumps(payload, indent=2, default=str)


def finance_agent_get_ticker_data(args: dict, **kwargs) -> str:
    """Return current quote data for one or more ticker symbols."""
    try:
        symbols = args.get("symbols")
        if not symbols:
            return _error("symbols is required")
        return _ok(core_get_ticker_data(symbols))
    except Exception as exc:
        return _error("Failed to get ticker data", details=str(exc))


def finance_agent_get_ticker_history(args: dict, **kwargs) -> str:
    """Return historical performance data for one or more ticker symbols."""
    try:
        symbols = args.get("symbols")
        if not symbols:
            return _error("symbols is required")
        return _ok(core_get_ticker_history(symbols, period=args.get("period", "1y")))
    except Exception as exc:
        return _error("Failed to get ticker history", details=str(exc))


def finance_agent_add_expense(args: dict, **kwargs) -> str:
    """Create a new expense record."""
    try:
        return _ok(
            core_add_expense(
                amount=args["amount"],
                currency=args["currency"],
                name=args["name"],
                date=args.get("date"),
                category=args.get("category"),
                merchant=args.get("merchant"),
                description=args.get("description"),
                account=args.get("account"),
                email_id=args.get("email_id"),
            )
        )
    except Exception as exc:
        return _error("Failed to add expense", details=str(exc))


def finance_agent_list_expenses(args: dict, **kwargs) -> str:
    """List expense records with optional filters."""
    try:
        expenses = core_list_expenses(
            date_from=args.get("date_from"),
            date_to=args.get("date_to"),
            category=args.get("category"),
            currency=args.get("currency"),
            merchant=args.get("merchant"),
            amount_min=args.get("amount_min"),
            amount_max=args.get("amount_max"),
            limit=args.get("limit", 50),
        )
        return _ok({"count": len(expenses), "expenses": expenses})
    except Exception as exc:
        return _error("Failed to list expenses", details=str(exc))


def finance_agent_get_expense_by_email_id(args: dict, **kwargs) -> str:
    """Look up an expense by source email identifier."""
    try:
        expense = core_get_expense_by_email_id(args["email_id"])
        return _ok({"found": expense is not None, "expense": expense})
    except Exception as exc:
        return _error("Failed to get expense by email id", details=str(exc))


def finance_agent_update_expense(args: dict, **kwargs) -> str:
    """Update an existing expense record by id."""
    try:
        expense_id = args["id"]
        update_fields = {
            key: args[key]
            for key in (
                "date",
                "amount",
                "currency",
                "name",
                "category",
                "merchant",
                "description",
                "account",
                "email_id",
            )
            if key in args
        }

        if not update_fields:
            return _error("No update fields were provided")

        expense = core_update_expense(expense_id, **update_fields)
        if expense is None:
            return _error(
                "Expense not found or no changes were applied",
                details={"id": expense_id},
            )
        return _ok(expense)
    except Exception as exc:
        return _error("Failed to update expense", details=str(exc))


def finance_agent_delete_expense(args: dict, **kwargs) -> str:
    """Delete an expense record by id."""
    try:
        expense_id = args["id"]
        deleted = core_delete_expense(expense_id)
        if not deleted:
            return _error("Expense not found", details={"id": expense_id})
        return _ok({"deleted": True, "id": expense_id})
    except Exception as exc:
        return _error("Failed to delete expense", details=str(exc))
