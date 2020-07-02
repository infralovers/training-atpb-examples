import sqlite3

def dict_factory(cursor, row):
    row_data = {}
    for idx, col in enumerate(cursor.description):
        row_data[col[0]] = row[idx]
    return row_data


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('blog.db')
        self.create_article_table()

    def create_article_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "article" (
          id INTEGER PRIMARY KEY,
          title TEXT,
          content TEXT,
          _is_deleted boolean DEFAULT(false)
        ) ;
        """
        self.conn.execute(query)


class ArticleModel():
    def __init__(self):
        self.conn = sqlite3.connect("blog.db")
        self.conn.row_factory = dict_factory


    def create(self, title, content):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO article(title, content) VALUES(?, ?)", (title, content))
        self.conn.commit()
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
