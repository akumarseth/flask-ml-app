from project.server.app import app, db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from project.server.dbmodel.basemodel import BaseModel


class ConfigTemplate(db.Model, BaseModel):
    """ ConfigTemplate Model for storing document category configuration template details """
    __tablename__ = "ConfigTemplate"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.Text, unique=False, nullable=False)
    display_template_name = db.Column(db.Text, unique=False, nullable=False)
    template_name = db.Column(db.Text, unique=True, nullable=False)
    version_no = db.Column(db.Text, unique=False, nullable=False)
    is_default = db.Column(db.Boolean, default=False, nullable=False)


class ConfigTemplateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfigTemplate


class ConfigTemplateMetadata(db.Model, BaseModel):
    """ ConfigTemplateMetadata Model for storing document category configuration template details """
    __tablename__ = "ConfigTemplateMetadata"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feature_name = db.Column(db.Text, unique=False, nullable=False)
    pattern = db.Column(db.Text, unique=False, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('ConfigTemplate.id'))


class ConfigTemplateMetadataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfigTemplateMetadata
