from flask import Flask, render_template
from config import Config
from models import db, User
from routes import api
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

    # check if the user admin exist 
    admin = User.query.filter_by(username="admin").first()

    if admin is None:

        admin = User(
            username="admin",
            password=generate_password_hash("admin123")
        )

        db.session.add(admin)
        db.session.commit()

        #print("Administrator account created.")

app.register_blueprint(api)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)