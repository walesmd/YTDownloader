#!/usr/bin/env python

import sqlite3

DB_FILE = "workloads.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS workloads (
        id TEXT PRIMARY KEY,
        title TEXT,
        author TEXT,
        author_url TEXT,
        duration_seconds INTEGER,
        video_url TEXT,
        video_published_at TEXT,
        download_started_at TEXT,
        download_completed_at TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized and ready: {DB_FILE}")