import os
import sqlite3
import threading
import logging


# ==========================================
# DATABASE LOCATION
# ==========================================

DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "sportsnews.db")

os.makedirs(DATA_DIR, exist_ok=True)


# ==========================================
# DATABASE
# ==========================================

class Database:

    def __init__(self):

        self.lock = threading.Lock()

        self.conn = sqlite3.connect(
            DB_FILE,
            check_same_thread=False
        )

        self.conn.row_factory = sqlite3.Row

        self.create_tables()

    # ======================================
    # CREATE TABLES
    # ======================================

    def create_tables(self):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles(

                article_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                status TEXT NOT NULL,

                first_seen TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY(article_id, channel)

            )
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status
            ON articles(status)
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(

                user_id INTEGER PRIMARY KEY,

                joined_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

            )
            """)

            self.conn.commit()

    # ======================================
    # ARTICLE FUNCTIONS
    # ======================================

    def article_exists(self, article_id, channel):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                """
                SELECT 1
                FROM articles
                WHERE article_id=?
                AND channel=?
                LIMIT 1
                """,
                (
                    article_id,
                    channel
                )
            )

            return cursor.fetchone() is not None

    def mark_seen(self, article_id, channel):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                """
                INSERT OR IGNORE INTO articles
                (
                    article_id,
                    channel,
                    status
                )
                VALUES
                (
                    ?,
                    ?,
                    'seen'
                )
                """,
                (
                    article_id,
                    channel
                )
            )

            self.conn.commit()

    def mark_published(self, article_id, channel):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                """
                INSERT INTO articles
                (
                    article_id,
                    channel,
                    status
                )
                VALUES
                (
                    ?,
                    ?,
                    'published'
                )
                ON CONFLICT(article_id, channel)
                DO UPDATE SET
                status='published'
                """,
                (
                    article_id,
                    channel
                )
            )

            self.conn.commit()

    def is_published(self, article_id, channel):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                """
                SELECT status
                FROM articles
                WHERE article_id=?
                AND channel=?
                """,
                (
                    article_id,
                    channel
                )
            )

            row = cursor.fetchone()

            if row is None:
                return False

            return row["status"] == "published"

    # ======================================
    # USERS
    # ======================================

    def add_user(self, user_id):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                """
                INSERT OR IGNORE
                INTO users(user_id)
                VALUES(?)
                """,
                (user_id,)
            )

            self.conn.commit()

    def total_users(self):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM users
                """
            )

            return cursor.fetchone()[0]

    # ======================================
    # DEBUG
    # ======================================

    def total_articles(self):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM articles
                """
            )

            return cursor.fetchone()[0]

    def close(self):

        self.conn.close()


db = Database()

logging.info("SQLite database loaded successfully.")
