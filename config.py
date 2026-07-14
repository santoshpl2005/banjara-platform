import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "banjara_secret_2026")

    MYSQL_HOST = os.environ.get("MYSQLHOST", "localhost")
    MYSQL_USER = os.environ.get("MYSQLUSER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQLPASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQLDATABASE", "railway")
    MYSQL_PORT = int(os.environ.get("MYSQLPORT", 3306))

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "static/images")