from flask import Flask, render_template, redirect, url_for
from config import Config
from models import db, User
from routes import api

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(api)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)