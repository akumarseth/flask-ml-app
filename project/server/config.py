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

    STORAGE_ACCOUNT_NAME = 'dssstorageflaskapp'
    CONTAINER_NAME = 'input'
    CONFIG_CONTAINER_NAME='config'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024    # 20 Mb limit
    


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = sqlite_local_base + database_name

    # STORAGE_ACCOUNT_NAME = 'pythonstorageaccount01'
    # ACCOUNT_KEY = 'KJ7dCf+yykXGmotjYtKgwgYjcm4BWlC56TajsfShAhu0UnYHhOPYJzmKo/4r6lfAXpCQ6o5aOvhKmp7kprBT7g=='
    # CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={ACCOUNT_KEY};EndpointSuffix=core.windows.net"
        
    ACCOUNT_KEY = 'pdLARQZbo5mjcJkKnWVLbGBVdhFdr9/hORs9AxoG4skXOWxpnp+HEb81hkiCFovEQDKvRI9jEa44ghVN2aMklQ=='
    CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={BaseConfig.STORAGE_ACCOUNT_NAME};AccountKey={ACCOUNT_KEY};EndpointSuffix=core.windows.net"


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = "postgresql://qywtuaouswpwun:90eacb2e62e6fea6b00a33a0c7dbaabcc552292b789e9b840948aa8ceaa052e5@ec2-35-169-188-58.compute-1.amazonaws.com:5432/d4986ivbgijcja"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    
    ACCOUNT_KEY = 'pdLARQZbo5mjcJkKnWVLbGBVdhFdr9/hORs9AxoG4skXOWxpnp+HEb81hkiCFovEQDKvRI9jEa44ghVN2aMklQ=='
    CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={BaseConfig.STORAGE_ACCOUNT_NAME};AccountKey={ACCOUNT_KEY};EndpointSuffix=core.windows.net"
    


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'JHJGYU6563#^&*230UNNXDFTYM667ghgh*@$#jfdhg767rtcfssdm,mbnvbcv3568976fssdfcggvghfjyuyqwavSGHJ'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ""
