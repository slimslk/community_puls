from os import getenv
from dotenv import load_dotenv

load_dotenv()
DATABASE_USERNAME = getenv("DATABASE_USERNAME", "username")
DATABASE_PASSWORD = getenv("DATABASE_PASSWORD", "password")
DATABASE_HOST = getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = getenv("DATABASE_PORT", 3306)
DATABASE_NAME = getenv("DATABASE_NAME", "db_name")


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}"
                               f":{DATABASE_PORT}/{DATABASE_NAME}")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
