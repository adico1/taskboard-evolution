import sqlite3
from contextlib import contextmanager

def _init_schema(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()

@contextmanager
def _get_conn(db_path):
    conn = sqlite3.connect(db_path)
    try:
        _init_schema(conn)
        yield conn
    finally:
        conn.close()

def insert_task(title, db_path):
    with _get_conn(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, 0)", (title,)
        )
        task_id = cur.lastrowid
        conn.commit()
        return {
            "id": task_id,
            "title": title,
            "completed": False
        }

def get_all_tasks(db_path):
    with _get_conn(db_path) as conn:
        cur = conn.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id ASC"
        )
        return [
            {"id": row[0], "title": row[1], "completed": bool(row[2])}
            for row in cur.fetchall()
        ]

def complete_task(task_id, db_path):
    with _get_conn(db_path) as conn:
        cur = conn.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,)
        )
        row = cur.fetchone()
        if not row:
            return None
        if not row[2]:
            conn.execute(
                "UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,)
            )
            conn.commit()
        return {"id": row[0], "title": row[1], "completed": True}
