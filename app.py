from flask import (Flask, render_template, request, jsonify, g)
from flask.cli import with_appcontext
from models import ArticleModel

DATABASE = 'blog.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


class Article():
    def __init__(self, db):
        self.model = ArticleModel(db)

    def create(self, json):
        result = self.model.create(
            json['title'],
            json['content'])
        return result

    def get(self, article_id):
        result = self.model.get(article_id)
        return result

    def list(self):
        result = self.model.list_items()
        return result

def init_db():
    g.article = Article(app.config['DATABASE'])

@app.before_request
def before_request():
    init_db()

@app.route('/')
def blog():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/health')
def health():
    return '{"status": "Ok"}', 200


@app.route('/api/article', methods=['POST'])
def article():
    new_post = g.article.create(request.get_json())
    return jsonify(new_post)


@app.route('/api/article', methods=['GET'])
def list_articles():
    return jsonify(g.article.list())


@app.route('/api/article/<article_id>', methods=['GET'])
def get_article(article_id=None):
    if article_id is None:
        return list_articles()
    current = g.article.get(article_id)
    if current is None:
        return "no article", 404
    return jsonify(current)


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
