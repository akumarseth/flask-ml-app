from project.server.app import app, db, bcrypt
from project.server.dbmodel.basemodel import BaseModel


class Student(db.Model, BaseModel):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)