from project.server.app import app, db
from project.server.dbmodel.basemodel import BaseModel

class Test(db.Model, BaseModel):
    __tablename__ = 'Test'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)