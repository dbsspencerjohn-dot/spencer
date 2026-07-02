from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Issue & Vulnerability Tracking System for CA1"


if __name__ == "__main__":
    app.run(debug=False)