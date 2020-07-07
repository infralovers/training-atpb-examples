"""
python blog base example for automated testing with selenium and behave
"""
from flask import (Flask, render_template, request, jsonify, g)
from models import ArticleModel

DATABASE = 'blog.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


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

def init_db():
    """
    init db based in config 'DATABASE'
    """
    g.article = Article(app.config['DATABASE'])

@app.before_request
def before_request():
    """
    before each request open the database connection
    """
    init_db()

@app.route('/')
def blog():
    """
    default root page
    returns:
        rendered home.html
    """
    return render_template('home.html')


@app.route('/about')
def about():
    """
    about page
    returns:
        rendered about.html
    """
    return render_template('about.html')


@app.route('/api/health')
def health():
    """
    rest api for health status
    returns:
        http code 200 if ok
    """
    return '{"status": "Ok"}', 200


@app.route('/api/article', methods=['POST'])
def article():
    """
    create a new article on rest
    """
    new_post = g.article.create(request.get_json())
    return jsonify(new_post)


@app.route('/api/article', methods=['GET'])
def list_articles():
    """
    list all article on rest api
    """
    return jsonify(g.article.list())


@app.route('/api/article/<article_id>', methods=['GET'])
def get_article(article_id=None):
    """
    get an article based on id via rest
    """
    if article_id is None:
        return list_articles()
    current = g.article.get(article_id)
    if current is None:
        return "no article", 404
    return jsonify(current)


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
