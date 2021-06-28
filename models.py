"""
Interaction with sqlite database and abstraction into classes/model represantion

Indented usage:
database_file = 'database.sqlite'
article = Article.init(database_file)
all_items = article.list()

"""
import sqlite3


class Article():
    """
    Article class to interact with article model
    """
    @staticmethod
    def init(database_file):
        """
        create aricle class as static initializer
        """
        model = ArticleModel(database_file)
        return Article(model)

    def __init__(self, model):
        """
        create article with model object
        """
        self.model = model

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
    def __init__(self, database_file):
        """
        init model and database
        args:
            database_file: database file to open as sqlite
        """
        self.connect_db(database_file)
        self.create_article_table()

    def __del__(self):
        """
        destructor of the class
        """
        self.conn.close()

    def create_article_table(self):
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
        self.conn.execute(query)
        self.conn.commit()


    def connect_db(self, database_file):
        """
        connect database based on argument string
        args:
            database_file: file to open as database
        returns:
            sqlite database connection
        """
        self.conn = sqlite3.connect(database_file)
        self.conn.row_factory = self.dict_factory

    @staticmethod
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
        self.conn.commit()
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
