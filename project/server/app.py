
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)

CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
    # 'project.server.config.TestingConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


migrate = Migrate()
migrate.init_app(app, db)


from project.server.auth.views import auth_blueprint
from project.server.student.views import stu_blueprint
from project.server.document.upload_azure_view import upload_blueprint
from project.server.document.extract_content import extract_blueprint
from project.server.document.entity_view import entity_blueprint
from project.server.category.views import category_blueprint
from project.server.categoryconfig.config_view import config_blueprint
from project.server.classification.spam_classification import spam_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(stu_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(entity_blueprint)
app.register_blueprint(extract_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(config_blueprint)
app.register_blueprint(spam_blueprint)
