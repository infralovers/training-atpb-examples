"""
python blog base example for automated testing with selenium and behave
"""
from flask import Flask, render_template, request, jsonify, g
from models import Article

DATABASE = 'blog.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


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
