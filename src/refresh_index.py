import hashlib
import sqlite3
from pathlib import Path

STATUS_DB = "index_status.db"


def init_status_db():
    conn = sqlite3.connect(STATUS_DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS file_status (
        file_hash TEXT PRIMARY KEY,
        file_path TEXT,
        status TEXT
    )""")
    conn.commit()
    conn.close()


def hash_file(file_path):
    return hashlib.sha256(open(file_path, "rb").read()).hexdigest()


def get_status(file_hash):
    conn = sqlite3.connect(STATUS_DB)
    row = conn.execute("SELECT status FROM file_status WHERE file_hash = ?", (file_hash,)).fetchone()
    conn.close()
    return row[0] if row else None


def mark_status(file_hash, file_path, status):
    conn = sqlite3.connect(STATUS_DB)
    conn.execute(
        "INSERT INTO file_status (file_hash, file_path, status) VALUES (?, ?, ?) "
        "ON CONFLICT(file_hash) DO UPDATE SET status = excluded.status",
        (file_hash, str(file_path), status)
    )
    conn.commit()
    conn.close()


def refresh_index(new_file_path):
    init_status_db()
    file_hash = hash_file(new_file_path)
    status = get_status(file_hash)

    if status in ("processing", "indexed"):
        return {"status": "skipped", "reason": status, "file": str(new_file_path)}

    mark_status(file_hash, new_file_path, "processing")
    try:
        # placeholder: real ingest/chunk/embed/store calls go here next
        mark_status(file_hash, new_file_path, "indexed")
        return {"status": "indexed", "file": str(new_file_path)}
    except Exception as e:
        mark_status(file_hash, new_file_path, "failed")
        raise