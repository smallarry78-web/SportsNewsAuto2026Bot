import sqlite3
from contextlib import closing

DB_NAME = "sportsnews.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with closing(self.conn.cursor()) as cursor:

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS posted_news(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(article_id, channel)
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            self.conn.commit()

    def is_posted(self, article_id, channel):

        with closing(self.conn.cursor()) as cursor:

            cursor.execute(
                """
                SELECT 1
                FROM posted_news
                WHERE article_id=? AND channel=?
                """,
                (article_id, channel)
            )

            return cursor.fetchone() is not None

    def save_post(self, article_id, channel):

        with closing(self.conn.cursor()) as cursor:

            cursor.execute(
                """
                INSERT OR IGNORE INTO posted_news(article_id, channel)
                VALUES(?, ?)
                """,
                (article_id, channel)
            )

            self.conn.commit()

    def add_user(self, user_id):

        with closing(self.conn.cursor()) as cursor:

            cursor.execute(
                """
                INSERT OR IGNORE INTO users(user_id)
                VALUES(?)
                """,
                (user_id,)
            )

            self.conn.commit()

    def total_users(self):

        with closing(self.conn.cursor()) as cursor:

            cursor.execute(
                "SELECT COUNT(*) FROM users"
            )

            return cursor.fetchone()[0]


db = Database()
