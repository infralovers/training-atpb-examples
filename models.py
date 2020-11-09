"""
model representation of databsae object
"""
import sqlite3
from flask import g


def dict_factory(cursor, row):
    """
    map row data to a dictionary
    args:
        cursor: database cursor
        row: current row
    returns:
        row representation as dictionary
    """
    row_data = {}
    for idx, col in enumerate(cursor.description):
        row_data[col[0]] = row[idx]
    return row_data

def create_article_table(connection):
    """
    create an article table in database
    """
    query = """
    CREATE TABLE IF NOT EXISTS "article" (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT
    ) ;
    """
    connection.execute(query)

def connect_db(database):
    """
    connect database based on argument string
    args:
        database: file to open as database
    returns:
        sqlite database connection
    """
    conn = sqlite3.connect(database)
    conn.row_factory = dict_factory
    init_db(conn)
    return conn

def init_db(conn):
    """
    init database and commit change
    args:
        conn: current connection
    """
    create_article_table(conn)
    conn.commit()


class Article():
    """
    Article class to interact with article model
    """
    def __init__(self, db):
        """
        create article with model object
        """
        self.model = ArticleModel(db)

    def create(self, json):
        """
        create a new article based on json data object
        args:
            json: json object with 'title' and 'content' objects
        returns:
            database representation of new article
        """
        result = self.model.create(
            json['title'],
            json['content'])
        return result

    def get(self, article_id):
        """
        get an article by id
        args:
            article_id: id of article
        returns:
            article based on article_id
        """
        result = self.model.get(article_id)
        return result

    def list(self):
        """
        list all articles
        returns:
            list of articles
        """
        result = self.model.list_items()
        return result

class ArticleModel():
    """
    Article Model to interact with database
    """
    def __init__(self, database):
        """
        init model and database
        args:
            database: database file to open as sqlite
        """
        if "db" not in g:
            g.conn = connect_db(database)
        self.conn = g.conn

    def create(self, title, content):
        """
        create an article
        args:
            title: title of article
            content: content of article
        returns:
            database represenstation of article
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO article(title, content) VALUES(?, ?)", (title, content))
        g.conn.commit()
        last_id = cursor.lastrowid
        return self.get(str(last_id))

    def list_items(self):
        """
        list all articles
        returns:
            list of articles
        """
        cursor = self.conn.execute("SELECT * from article")
        result = cursor.fetchall()
        return result

    def get(self, content_id):
        """
        get article based on content_id
        args:
            content_id: id of article
        returns:
            article from database
        """
        cur = self.conn.execute(
            "SELECT id,title,content from article WHERE id=?", (content_id))
        result = cur.fetchone()
        return result
