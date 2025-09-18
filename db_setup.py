#!/usr/bin/env python

import os
import sqlite3
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DB_BACKEND = os.getenv("DB_BACKEND", "sqlite").lower()
DB_FILE = os.getenv("SQLITE_FILE", "workloads.db")
DB_URL = os.getenv("DATABASE_URL")

SCHEMA = """
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
"""

def init_sqlite():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(SCHEMA)
    conn.commit()
    conn.close()
    print(f"✅ SQLite DB initialized: {DB_FILE}")

def init_postgres():
    if not DB_URL:
        raise ValueError("POSTGRES_URL not set in .env")
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(SCHEMA)
    conn.commit()
    conn.close()
    print("✅ Postgres DB initialized")

def init_db():
    if DB_BACKEND == "postgres":
        init_postgres()
    else:
        init_sqlite()

if __name__ == "__main__":
    init_db()