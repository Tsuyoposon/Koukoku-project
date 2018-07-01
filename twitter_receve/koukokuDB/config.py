"""FlaskのConfigを提供する"""
import os

class DevelopmentConfig:
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/koukokuDB?charset=utf8'.format(**{
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'root'),
        'host': os.getenv('DB_HOST', 'localhost'),
    })
    if os.environ['ENV'] == "wercker":
            SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/koukokuDB?charset=utf8'.format(**{
                'user': os.getenv('DB_USER', 'root'),
                'password': os.getenv('DB_PASSWORD', 'root'),
                'host': os.environ['MYSQL_PORT'],
            })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


Config = DevelopmentConfig
