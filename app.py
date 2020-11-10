from flask import Flask

# from models import Article
# DATABASE = 'blog.db'

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def init_db():
    """
    init db based in config 'DATABASE'
    """
    print("Creating database")
    # g.article = Article(app.config['DATABASE'])


@app.route('/')
def blog():
    return "My Blog"

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], port=5000)
