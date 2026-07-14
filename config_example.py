# Copy this file to config.py and fill in your details
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'your_mysql_password_here'
    MYSQL_DB = 'banjara_db'
    UPLOAD_FOLDER = 'static/images'