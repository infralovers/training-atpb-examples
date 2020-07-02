import sqlite3

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
          _is_deleted boolean
        );
        """
        self.conn.execute(query)

class ArticleModel():
    def __init__(self):
        self.conn = sqlite3.connect("blog.db")

    def create(self, title, content):
        result = self.conn.execute("INSERT INTO article(title, content) VALUES(?, ?)", (title, content))
        self.conn.commit()
        self.conn.close()
        return result

    def list_items(self):
        query = self.conn.execute("SELECT title, content from article")
        result_set = query.fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result
