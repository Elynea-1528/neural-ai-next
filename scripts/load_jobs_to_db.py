#!/usr/bin/env python3
"""Load historical jobs from historical_jobs.txt into the database."""

import re
import sqlite3
from datetime import datetime


def parse_jobs_from_file(filename):
    """Parse jobs from the historical_jobs.txt file."""
    jobs = []

    with open(filename, encoding="utf-8") as f:
        content = f.read()

    # Find all job sections
    job_pattern = (
        r"Job ID: (\w+)\s+Symbol: (\w+)\s+Timeframe: (\w+)\s+Start: ([\d-]+)\s+End: ([\d-]+)"
    )
    matches = re.findall(job_pattern, content)

    for match in matches:
        job_id, symbol, timeframe, start_date, end_date = match
        jobs.append(
            {
                "job_id": job_id,
                "symbol": symbol,
                "timeframe": timeframe,
                "start_date": start_date,
                "end_date": end_date,
                "batch_size": 99000,  # Default batch size
                "priority": "normal",  # Default priority
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
        )

    return jobs


def insert_jobs_to_db(jobs, db_path):
    """Insert jobs into the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_jobs (
            job_id TEXT PRIMARY KEY,
            symbol TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            batch_size INTEGER NOT NULL,
            priority TEXT NOT NULL DEFAULT 'normal',
            status TEXT NOT NULL,
            progress REAL DEFAULT 0,
            total_batches INTEGER DEFAULT 0,
            completed_batches INTEGER DEFAULT 0,
            current_batch INTEGER DEFAULT 0,
            errors TEXT DEFAULT '[]',
            warnings TEXT DEFAULT '[]',
            created_at TEXT NOT NULL,
            started_at TEXT,
            completed_at TEXT,
            estimated_duration TEXT
        )
    """)

    # Insert jobs
    for job in jobs:
        cursor.execute(
            """
            INSERT OR REPLACE INTO historical_jobs
            (job_id, symbol, timeframe, start_date, end_date, batch_size, priority, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                job["job_id"],
                job["symbol"],
                job["timeframe"],
                job["start_date"],
                job["end_date"],
                job["batch_size"],
                job["priority"],
                job["status"],
                job["created_at"],
            ),
        )

    conn.commit()
    conn.close()

    print(f"Successfully inserted {len(jobs)} jobs into the database")


def main():
    # Parse jobs from file
    jobs = parse_jobs_from_file("historical_jobs.txt")
    print(f"Found {len(jobs)} jobs in historical_jobs.txt")

    # Insert jobs into database
    insert_jobs_to_db(jobs, "data/collectors/mt5/historical_jobs.db")

    # Verify insertion
    conn = sqlite3.connect("data/collectors/mt5/historical_jobs.db")
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM historical_jobs WHERE status = "pending"')
    count = cursor.fetchone()[0]
    conn.close()

    print(f"Verified: {count} pending jobs in database")

    # Show first 5 jobs
    print("\nFirst 5 jobs:")
    for i, job in enumerate(jobs[:5], 1):
        print(
            f"  {i}. {job['job_id']}: {job['symbol']} {job['timeframe']} from {job['start_date']} to {job['end_date']}"
        )


if __name__ == "__main__":
    main()
