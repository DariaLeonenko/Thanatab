import sqlite3
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "bookmarks.db"


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL DEFAULT '',
                raw_text TEXT NOT NULL DEFAULT '',
                category TEXT NOT NULL DEFAULT 'Без категории',
                date_added TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'broken'))
            )
            """
        )


def save_bookmark(
    url: str,
    title: str,
    raw_text: str,
    category: str = "Без категории",
    status: str = "active",
) -> int:
    init_database()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO bookmarks (url, title, raw_text, category, status)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                title = excluded.title,
                raw_text = excluded.raw_text,
                category = excluded.category,
                status = excluded.status
            """,
            (url, title, raw_text, category, status),
        )
        row = conn.execute(
            "SELECT id FROM bookmarks WHERE url = ?", (url,)
        ).fetchone()
        return int(row["id"])


def get_bookmarks(
    status: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
) -> list[dict]:
    init_database()
    query = "SELECT * FROM bookmarks WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if category:
        query += " AND category = ?"
        params.append(category)
    if search:
        query += " AND (title LIKE ? OR url LIKE ?)"
        pattern = f"%{search}%"
        params.extend([pattern, pattern])

    query += " ORDER BY date_added DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def get_categories() -> list[str]:
    init_database()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT category FROM bookmarks WHERE status = 'active' ORDER BY category"
        ).fetchall()
    return [row["category"] for row in rows]


def get_category_statistics() -> list[dict]:
    init_database()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT category, COUNT(*) as count 
            FROM bookmarks 
            WHERE status = 'active' 
            GROUP BY category 
            ORDER BY count DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def delete_broken_bookmarks() -> int:
    init_database()
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM bookmarks WHERE status = 'broken'")
        return cursor.rowcount