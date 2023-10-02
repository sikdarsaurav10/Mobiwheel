# import os


class Config:
    SECRET_KEY = '\xd30\xfc\xe6&\x87\xdc\x14\x07\xef\xcbHR\x95\xd8\xb2=\xfa\xc3\x8a\xcf\x97\x0eT'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Customer_Data.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mobservice789@gmail.com'
    MAIL_PASSWORD = 'nftxfoyuqkvcvlbq'
    MAIL_DEFAULT_SENDER = 'mobservice789@gmail.com'
