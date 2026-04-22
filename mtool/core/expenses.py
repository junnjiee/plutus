from datetime import date
from .db import get_db


def add_expense(
    amount: float,
    currency: str,
    name: str,
    *,
    expense_date: str | None = None,
    category: str | None = None,
    merchant: str | None = None,
    description: str | None = None,
    account: str | None = None,
    email_id: str | None = None,
) -> dict:
    expense_date = expense_date or str(date.today())
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO expenses (date, amount, currency, name, category, merchant, description, account, email_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (expense_date, amount, currency, name, category, merchant, description, account, email_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM expenses WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return dict(row)


def list_expenses(
    *,
    date_from: str | None = None,
    date_to: str | None = None,
    category: str | None = None,
    currency: str | None = None,
    merchant: str | None = None,
    amount_min: float | None = None,
    amount_max: float | None = None,
    limit: int = 50,
) -> list[dict]:
    filters = []
    params = []

    if date_from:
        filters.append("date >= ?")
        params.append(date_from)
    if date_to:
        filters.append("date <= ?")
        params.append(date_to)
    if amount_min is not None:
        filters.append("amount >= ?")
        params.append(amount_min)
    if amount_max is not None:
        filters.append("amount <= ?")
        params.append(amount_max)
    for col, val in [
        ("category", category),
        ("currency", currency),
        ("merchant", merchant),
    ]:
        if val:
            filters.append(f"{col} = ?")
            params.append(val)

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    params.append(limit)

    with get_db() as conn:
        rows = conn.execute(
            f"SELECT * FROM expenses {where} ORDER BY date DESC, id DESC LIMIT ?",
            params,
        ).fetchall()
        return [dict(r) for r in rows]


def get_expense_by_email_id(email_id: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM expenses WHERE email_id = ?", (email_id,)
        ).fetchone()
        return dict(row) if row else None


def update_expense(id: int, **fields) -> dict | None:
    allowed = {
        "date",
        "amount",
        "currency",
        "name",
        "category",
        "merchant",
        "description",
        "account",
        "email_id",
    }
    updates = [(k, v) for k, v in fields.items() if k in allowed]
    if not updates:
        return None

    set_clause = ", ".join(f"{k} = ?" for k, _ in updates)
    params = [v for _, v in updates] + [id]

    with get_db() as conn:
        conn.execute(f"UPDATE expenses SET {set_clause} WHERE id = ?", params)
        conn.commit()
        row = conn.execute("SELECT * FROM expenses WHERE id = ?", (id,)).fetchone()
        return dict(row) if row else None


def delete_expense(id: int) -> bool:
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0
