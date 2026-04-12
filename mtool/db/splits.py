from datetime import date
from .db import get_db

VALID_SPLIT_TYPES = {"equal", "exact", "percentage", "shares"}


def add_split(
    name: str,
    total_amount: float,
    currency: str,
    split_type: str,
    *,
    split_date: str | None = None,
) -> dict:
    if split_type not in VALID_SPLIT_TYPES:
        raise ValueError(
            f"split_type must be one of: {', '.join(sorted(VALID_SPLIT_TYPES))}"
        )
    split_date = split_date or str(date.today())
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO splits (name, date, total_amount, currency, split_type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, split_date, total_amount, currency, split_type),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM splits WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return dict(row)


def add_participant(
    split_id: int,
    name: str,
    original_amount_owed: float,
    *,
    amount_owed: float | None = None,
) -> dict:
    actual_amount_owed = (
        amount_owed if amount_owed is not None else original_amount_owed
    )
    with get_db() as conn:
        split = conn.execute(
            "SELECT id FROM splits WHERE id = ?", (split_id,)
        ).fetchone()
        if not split:
            raise ValueError(f"No split found with id {split_id}")
        cursor = conn.execute(
            """
            INSERT INTO split_participants (split_id, name, original_amount_owed, amount_owed)
            VALUES (?, ?, ?, ?)
            """,
            (split_id, name, original_amount_owed, actual_amount_owed),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM split_participants WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return dict(row)


def _attach_participants(conn, splits: list[dict]) -> list[dict]:
    if not splits:
        return splits
    split_ids = [s["id"] for s in splits]
    placeholders = ",".join("?" * len(split_ids))
    rows = conn.execute(
        f"SELECT * FROM split_participants WHERE split_id IN ({placeholders}) ORDER BY split_id, id",
        split_ids,
    ).fetchall()
    participants_by_split: dict[int, list[dict]] = {}
    for row in rows:
        p = dict(row)
        participants_by_split.setdefault(p["split_id"], []).append(p)
    for s in splits:
        s["participants"] = participants_by_split.get(s["id"], [])
    return splits


def get_split(split_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM splits WHERE id = ?", (split_id,)).fetchone()
        if not row:
            return None
        splits = _attach_participants(conn, [dict(row)])
        return splits[0]


def list_splits(
    *,
    person: str | None = None,
    settled: bool | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    limit: int = 50,
) -> list[dict]:
    filters = []
    params: list = []

    if person:
        filters.append("id IN (SELECT split_id FROM split_participants WHERE name = ?)")
        params.append(person)
    if settled is True:
        filters.append(
            "id NOT IN (SELECT split_id FROM split_participants WHERE amount_owed > 0)"
        )
    elif settled is False:
        filters.append(
            "id IN (SELECT split_id FROM split_participants WHERE amount_owed > 0)"
        )
    if date_from:
        filters.append("date >= ?")
        params.append(date_from)
    if date_to:
        filters.append("date <= ?")
        params.append(date_to)

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    params.append(limit)

    with get_db() as conn:
        rows = conn.execute(
            f"SELECT * FROM splits {where} ORDER BY date DESC, id DESC LIMIT ?",
            params,
        ).fetchall()
        splits = [dict(r) for r in rows]
        return _attach_participants(conn, splits)


def get_balance(*, person: str | None = None) -> list[dict]:
    """Return all participant rows with outstanding balances (amount_owed > 0), joined with split info."""
    filters = ["p.amount_owed > 0"]
    params: list = []

    if person:
        filters.append("p.name = ?")
        params.append(person)

    where = f"WHERE {' AND '.join(filters)}"

    with get_db() as conn:
        rows = conn.execute(
            f"""
            SELECT p.id, p.split_id, p.name, p.original_amount_owed, p.amount_owed,
                   s.name AS split_name, s.date, s.currency
            FROM split_participants p
            JOIN splits s ON s.id = p.split_id
            {where}
            ORDER BY p.name, s.date, p.split_id
            """,
            params,
        ).fetchall()
        return [dict(r) for r in rows]


def update_participant(participant_id: int, **fields) -> dict | None:
    allowed = {"name", "original_amount_owed", "amount_owed"}
    updates = [(k, v) for k, v in fields.items() if k in allowed]
    if not updates:
        return None
    set_clause = ", ".join(f"{k} = ?" for k, _ in updates)
    params = [v for _, v in updates] + [participant_id]
    with get_db() as conn:
        conn.execute(f"UPDATE split_participants SET {set_clause} WHERE id = ?", params)
        conn.commit()
        row = conn.execute(
            "SELECT * FROM split_participants WHERE id = ?", (participant_id,)
        ).fetchone()
        return dict(row) if row else None


def delete_split(split_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM splits WHERE id = ?", (split_id,))
        conn.commit()
        return cursor.rowcount > 0
