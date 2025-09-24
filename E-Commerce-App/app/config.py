import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devsecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///ecommerce.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False