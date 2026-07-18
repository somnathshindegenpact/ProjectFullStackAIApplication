import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.getenv('FLASK_SECRET_KEY', 'jwt-secret'))
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


config = Config()
