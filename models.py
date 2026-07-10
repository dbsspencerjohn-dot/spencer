from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

db = SQLAlchemy()

# Create a model for the vulnerability issues
class VulnIssue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    reporter = db.Column(db.String(100), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    affected_system = db.Column(db.String(150), nullable=False)
    cvss_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
    db.DateTime,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
    )
   
    def __repr__(self):
        return f"VulnIssue(title={self.title})"
    
    # coversion method to convert the model instance to a dict 
    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "status": self.status,
            "reporter": self.reporter,
            "assigned_to": self.assigned_to,
            "affected_system": self.affected_system,
            "cvss_score": self.cvss_score,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

# Create a model for application users
class User(db.Model):

    __tablename__ = "users"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(255),
        nullable=False
    )

    def __repr__(self):

        return f"User(username={self.username})"