# project/server/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))
# postgres_local_base = 'postgresql://postgres:@localhost/'
# sqlite_local_base = 'mysql+pymysql://root:Admin@123@localhost:3307/'
sqlite_local_base = 'sqlite:///' + basedir + '\\'
database_name = 'flask_db.sqlite'

# pro_dbname=f"'flask_mp_app_db' user='abhishekkumar13@usepostgresserver' host='usepostgresserver.postgres.database.azure.com' password='Admin#123' port='5432' sslmode='true'"
po_db = f"postgresql://usepostgresserver.postgres.database.azure.com:5432/flask_ml_app_db?user=abhishekkumar13@usepostgresserver&password=Admin#123&sslmode=require"
# EmailID
serviceEmail = 'xxxx@gmail.com'
password = '********'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = po_db #sqlite_local_base + database_name

    STORAGE_ACCOUNT_NAME = 'pythonstorageaccount01'
    ACCOUNT_KEY = '*******************'
    CONNECTION_STRING = '*************************'
    CONTAINER_NAME = 'input'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024    # 20 Mb limit

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = sqlite_local_base + database_name
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'JHJGYU6563#^&*230UNNXDFTYM667ghgh*@$#jfdhg767rtcfssdm,mbnvbcv3568976fssdfcggvghfjyuyqwavSGHJ'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = po_db
