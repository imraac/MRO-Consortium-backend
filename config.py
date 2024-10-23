import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///agency.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)



    MAIL_SERVER = 'mail.mrosconsortium.org'  
    MAIL_PORT = 465
    MAIL_USE_SSL = True  
    MAIL_USE_TLS = False  
    MAIL_USERNAME = 'noreply@mrosconsortium.org'  
    MAIL_PASSWORD = 'No2024Reply'  
    MAIL_DEFAULT_SENDER = 'noreply@mrosconsortium.org'  
