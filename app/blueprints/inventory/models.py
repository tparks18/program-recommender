from app import db
from datetime import datetime
import os

class QuizResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_role = db.Column(db.String(150), nullable=False)
    years_experience = db.Column(db.String(150), nullable=False)
    time_commitment = db.Column(db.String(150), nullable=False)
    topics_addressed = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_role = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    time_commitment = db.Column(db.String(150), nullable=False)
    years_experience = db.Column(db.String(150), nullable=False)
    topics_addressed = db.Column(db.String(500), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Program|{self.name}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'job_role', 'name', 'description', 'time_commitment', 'years_experience', 'topics_addressed'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()