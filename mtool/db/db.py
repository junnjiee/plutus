import hashlib
import os
import sqlite3
from pathlib import Path


MIGRATIONS = [
    """
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY,
            date        TEXT NOT NULL,
            amount      REAL NOT NULL,
            currency    TEXT NOT NULL,
            category    TEXT,
            merchant    TEXT,
            description TEXT,
            account     TEXT,
            created_at  TEXT NOT NULL DEFAULT (date('now'))
        )
    """,
]


def _db_path() -> Path:
    default = Path.home() / ".config" / "finance_agent" / "data"
    data_dir = Path(os.environ.get("FINANCE_AGENT_DATA_DIR", default))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "finance_agent.db"


def _hash(sql: str) -> str:
    return hashlib.sha256(sql.strip().encode()).hexdigest()


def _migrate(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            version    INTEGER PRIMARY KEY,
            hash       TEXT NOT NULL,
            applied_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()

    applied = {
        row["version"]: row["hash"]
        for row in conn.execute("SELECT version, hash FROM _migrations")
    }

    for version, sql in enumerate(MIGRATIONS):
        current_hash = _hash(sql)
        if version in applied:
            if applied[version] != current_hash:
                raise RuntimeError(
                    f"Migration {version} has been edited after it was applied. "
                    "Add a new migration instead of modifying existing ones."
                )
        else:
            conn.execute(sql)
            conn.execute(
                "INSERT INTO _migrations (version, hash) VALUES (?, ?)",
                (version, current_hash),
            )
            conn.commit()


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        _migrate(conn)
    except Exception:
        conn.close()
        raise
    return conn
