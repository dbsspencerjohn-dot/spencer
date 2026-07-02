from flask import Flask
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(api)

@app.route("/")
def home():
    return "Issue & Vulnerability Tracking System for CA1"


if __name__ == "__main__":
    app.run(debug=False)