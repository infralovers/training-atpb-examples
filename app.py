import sqlite3
from flask import Flask, render_template, request, jsonify
from models import ArticleModel, Schema

app = Flask(__name__)


class Article():
    def __init__(self):
        self.model = ArticleModel()

    def create(self, params):
        result = self.model.create(params['title'], params['content'])
        return result

    def get(self, params):
        result = self.model.get(params['id'])
        return result

    def list(self):
        result = self.model.list_items()
        return result


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
    return jsonify(Article().create(request.get_json()))


@app.route('/api/article', methods=["GET"])
def list_article():
    return jsonify(Article().list())


@app.route('/api/article')
def get_article():
    conn = sqlite3.connect("blog.db")
    cursor = conn.execute("SELECT * FROM article")
    for row in cursor:
        print("ID =", row[0])
        print("Title =", row[1])
        print("Content =", row[2], "\n")
    conn.close()

    return ''


if __name__ == "__main__":
    Schema()
    app.run(debug=True)
