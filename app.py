import sqlite3
import sys
from flask import Flask, render_template, request, jsonify
from models import ArticleModel, Schema

app = Flask(__name__)

class Article():
    def __init__(self):
        self.model = ArticleModel()

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
     newPost = Article().create(request.get_json())
     return jsonify(newPost)


@app.route('/api/article', methods=['GET'])
def list_articles():
    return jsonify(Article().list())

@app.route('/api/article/<article_id>', methods=['GET'])
def get_article(article_id=None):
    if(article_id == None):
        return list_articles()
    article = Article().get(article_id)
    if(article == None):
        return "no article", 404
    return jsonify(article)


if __name__ == "__main__":
    Schema()
    app.run(debug=True)
