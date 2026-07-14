import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'banjara_secret_2026')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root123')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'banjara_db')
    MYSQL_PORT = int(os.environ.get("MYSQLPORT", 3306))
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/images')