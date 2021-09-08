# project/server/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))
# postgres_local_base = 'postgresql://postgres:@localhost/'
# sqlite_local_base = 'mysql+pymysql://root:Admin@123@localhost:3307/'
sqlite_local_base = 'sqlite:///' + basedir + '\\'
database_name = 'flask_db.sqlite'

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
    SQLALCHEMY_DATABASE_URI = sqlite_local_base + database_name

    STORAGE_ACCOUNT_NAME = 'pythonstorageaccount01'
    ACCOUNT_KEY = 'jdfhdsjkfsdfsyweiufhnsjd'
    CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=pythonstorageaccount01;AccountKey=f'{ACCOUNT_KEY}';EndpointSuffix=core.windows.net"
    CONTAINER_NAME = 'input'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024    # 20 Mb limit

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    # database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    # dbuser="qywtuaouswpwun",
    # dbpass="90eacb2e62e6fea6b00a33a0c7dbaabcc552292b789e9b840948aa8ceaa052e5",
    # dbhost="ec2-35-169-188-58.compute-1.amazonaws.com",
    # dbname="d4986ivbgijcja"
    # )
    SQLALCHEMY_DATABASE_URI = "postgres://qywtuaouswpwun:90eacb2e62e6fea6b00a33a0c7dbaabcc552292b789e9b840948aa8ceaa052e5@ec2-35-169-188-58.compute-1.amazonaws.com:5432/d4986ivbgijcja"
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'JHJGYU6563#^&*230UNNXDFTYM667ghgh*@$#jfdhg767rtcfssdm,mbnvbcv3568976fssdfcggvghfjyuyqwavSGHJ'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ""
