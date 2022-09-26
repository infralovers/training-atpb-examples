from flask import Flask

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def blog():
    return "My Blog"

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], port=51000)
