# import os


class Config:
    SECRET_KEY = 'myhello'
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////mnt/e/projects/fullstack/mobiwheel/web/Customer_Data.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sikdarsaurav10@gmail.com'
    MAIL_PASSWORD = 'ksccvhtqwkzqkzxa'
    MAIL_DEFAULT_SENDER = 'sikdarsaurav10@gmail.com'
