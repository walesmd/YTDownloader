import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_BACKEND = os.getenv("DB_BACKEND", "sqlite").lower()
DB_FILE = os.getenv("DB_FILE", "workloads.db")
DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if DB_BACKEND == "postgres":
        return psycopg2.connect(DATABASE_URL, cursor_factory = RealDictCursor)
    else:  # default: sqlite
        return sqlite3.connect(DB_FILE)


def insert_or_update_workload(metadata, started_at = None, completed_at = None):
    conn = get_connection()
    cur = conn.cursor()

    params = (
        metadata["id"],
        metadata["title"],
        metadata["author"],
        metadata["author_url"],
        metadata["duration_seconds"],
        metadata["video_url"],
        metadata["video_published_at"],
        started_at,
        completed_at
    )

    if DB_BACKEND == "postgres":
        value_str = "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    else:  # default: sqlite
        value_str = "(?, ?, ?, ?, ?, ?, ?, ?, ?)"

    query = f"""
    INSERT INTO workloads (
        id, title, author, author_url, duration_seconds,
        video_url, video_published_at, download_started_at, download_completed_at
    )
    VALUES {value_str}
    ON CONFLICT (id) DO UPDATE SET
        title = EXCLUDED.title,
        author = EXCLUDED.author,
        author_url = EXCLUDED.author_url,
        duration_seconds = EXCLUDED.duration_seconds,
        video_url = EXCLUDED.video_url,
        video_published_at = EXCLUDED.video_published_at,
        download_started_at = COALESCE(EXCLUDED.download_started_at, workloads.download_started_at),
        download_completed_at = COALESCE(EXCLUDED.download_completed_at, workloads.download_completed_at)
    """

    cur.execute(query, params)
    conn.commit()

    cur.close()
    conn.close()
