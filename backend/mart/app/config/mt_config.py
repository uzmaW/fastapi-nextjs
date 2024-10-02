import os
from dotenv import load_dotenv

env = os.getenv('ENV', 'local')
if env == 'production':
    load_dotenv('.env.prod')
else:
    load_dotenv('.env.local')
    
class MtConfig:
    '''
    General configuration parent class
    '''
    SECRET_KEY = os.getenv('SECRET_KEY') or 'itsjust-another-app-$123456'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'localhost:5434'
    SQLALCHEMY_DATABASE_URI_DISABLE = os.getenv('DATABASE_URL_SSL_DISABLE') or 'localhost:5434'
    POSTGRES_DB = os.getenv('POSTGRES_DB') or 'postgres'
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')
    PS_PORT = os.getenv('POSTGRES_PORT')
    ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES') or 30)
    ALGORITHM = os.getenv('ALGORITHM') or 'HS256'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'itsjust-another-app-$123456'

    #--------------------------------------------------------------------#
    # KAFKA configurations
    #--------------------------------------------------------------------#
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS') or 'localhost:19092'
    KAFKA_ORDER_TOPIC = os.getenv('KAFKA_TOPIC') or 'mt-orders'
    KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP') or 'mt-group'
    KAFKA_AUTO_OFFSET_RESET = os.getenv('KAFKA_AUTO_OFFSET_RESET') or 'earliest'
    KAFKA_ENABLE_AUTO_COMMIT = os.getenv('KAFKA_ENABLE_AUTO_COMMIT') or False
    KAFKA_REGISTRY_URL = os.getenv('KAFKA_REGISTRY_URL') or 'localhost:8001'
    #--------------------------------------------------------------------#
    # cloudinary configurations
    #--------------------------------------------------------------------#
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME') or 'dxx9pk6mb'
    #--------------------------------------------------------------------#
    # application  configurations
    #--------------------------------------------------------------------#
    DEBUG = os.getenv('DEBUG') or True
    APP_NAME = os.getenv('APP_NAME') or ''
    APP_VERSION = os.getenv('APP_VERSION') or '1.0.0'
    APP_DESCRIPTION = os.getenv('APP_DESCRIPTION') or 'A simple application'
   #UPLOADED_PHOTOS_DEST ='app/static/photos'
    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    # simple mde  configurations
    #SIMPLEMDE_JS_IIFE = True
    #SIMPLEMDE_USE_CDN = True        

    