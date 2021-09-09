from project.server.app import db, ma


class BaseModel():
    """ BaseModel Model for audit column """
    created_by = db.Column(db.String(255), unique=False, nullable=False)
    created_date= db.Column(db.Text, unique=False, nullable=True)
    edited_by= db.Column(db.String(255), unique=False, nullable=True)
    edited_date= db.Column(db.Text, unique=False, nullable=True)
