"""FlaskのConfigを提供する"""
import os

class DevelopmentConfig:
    # SQLAlchemy

    if os.environ['DATABASE_URL']:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']        
    elif os.environ['ENV'] == "wercker":
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/koukokuDB?charset=utf8'.format(**{
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'root'),
            'host': os.environ['MYSQL_PORT_3306_TCP_ADDR'],
        })
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/koukokuDB?charset=utf8'.format(**{
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'root'),
            'host': os.getenv('DB_HOST', 'localhost'),
        })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


Config = DevelopmentConfig
