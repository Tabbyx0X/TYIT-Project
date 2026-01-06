import os
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    """Get database URL, handling postgres:// vs postgresql:// prefix"""
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    return 'sqlite:///voting_system.db'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Your email
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # App password
    MAIL_USE_TLS = True
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = get_database_url()
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Optimized for Neon Pooler + Serverless
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_size': 2,
        'max_overflow': 3,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'connect_args': {
            'connect_timeout': 10,
            'application_name': 'voting_system'
        }
    }
    
    # Session configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
