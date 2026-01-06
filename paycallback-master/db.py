from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///counter.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
