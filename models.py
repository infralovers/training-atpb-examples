import sqlite3
from flask import g


def dict_factory(cursor, row):
    row_data = {}
    for idx, col in enumerate(cursor.description):
        row_data[col[0]] = row[idx]
    return row_data

def create_article_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS "article" (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT,
        _is_deleted boolean DEFAULT(false)
    ) ;
    """
    connection.execute(query)

def connect_db(database):
    conn = sqlite3.connect(database)
    conn.row_factory = dict_factory
    init_db(conn)
    return conn

def init_db(conn):
    create_article_table(conn)
    conn.commit()

class ArticleModel():
    def __init__(self, database):
        if "db" not in g:
            g.conn = connect_db(database)
        self.conn = g.conn

    def create(self, title, content):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO article(title, content) VALUES(?, ?)", (title, content))
        g.conn.commit()
        last_id = cursor.lastrowid
        return self.get(str(last_id))

    def list_items(self):
        cursor = self.conn.execute("SELECT * from article")
        result = cursor.fetchall()
        return result

    def get(self, content_id):
        cur = self.conn.execute(
            "SELECT id,title,content from article WHERE id=?", (content_id))
        result = cur.fetchone()
        return result
