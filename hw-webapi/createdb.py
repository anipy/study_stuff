"""Script for database initialization"""

import os
import sqlite3

from config import DB


def init_database(file_name):
    """Create SQLite database with two tables: quotes and images"""
    if not os.path.exists(file_name):
        db_connection = sqlite3.connect(file_name)

        with db_connection as db:
            db.execute(
                "CREATE TABLE quotes (id integer primary key autoincrement, txt text)"
            )
            db.execute(
                "CREATE TABLE images (id integer primary key autoincrement, txt text)"
            )


if __name__ == "__main__":
    init_database(DB)
