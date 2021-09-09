from project.server.app import db, ma


class BaseModel():
    """ BaseModel Model for audit column """
    created_by = db.Column(db.String(255), nullable=False)
    created_date= db.Column(db.DateTime, nullable=False)
    edited_by= db.Column(db.String(255), nullable=False)
    edited_date= db.Column(db.DateTime, nullable=False)
