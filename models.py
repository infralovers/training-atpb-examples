import sqlite3
from flask import g
from contextlib import closing

def dict_factory(cursor, row):
    row_data = {}
    for idx, col in enumerate(cursor.description):
        row_data[col[0]] = row[idx]
    return row_data


class ArticleModel():
    def __init__(self, db):
        if "db" not in g:
            g.conn = self.connect_db(db)

    def connect_db(self, db):
        conn = sqlite3.connect(db)
        conn.row_factory = dict_factory
        self.init_db(conn)
        return conn

    def init_db(self, conn):
        self.create_article_table(conn)
        conn.commit()

    def create_article_table(self, db):
        query = """
        CREATE TABLE IF NOT EXISTS "article" (
          id INTEGER PRIMARY KEY,
          title TEXT,
          content TEXT,
          _is_deleted boolean DEFAULT(false)
        ) ;
        """
        db.execute(query)

    def create(self, title, content):
        cursor = g.conn.cursor()
        cursor.execute(
            "INSERT INTO article(title, content) VALUES(?, ?)", (title, content))
        g.conn.commit()
        last_id = cursor.lastrowid
        return self.get(str(last_id))

    def list_items(self):
        cursor = g.conn.execute("SELECT * from article")
        result = cursor.fetchall()
        return result

    def get(self, content_id):
        cur = g.conn.execute(
            "SELECT id,title,content from article WHERE id=?", (content_id))
        result = cur.fetchone()
        return result
