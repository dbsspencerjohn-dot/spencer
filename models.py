from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

class VulnIssue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    decription = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
   
    def __repr__(self):
        return f"VulnIssue(title={self.title})"