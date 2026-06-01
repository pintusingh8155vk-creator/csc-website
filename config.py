import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cybercafe-secret-key-prod-2026')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    DEBUG = False
    TESTING = False
    
    # Database - Use the provided PostgreSQL URL
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://arcade_hub_db_005a_user:1eFI2CcvxvhXrdzMiTh8y9Ap2l8jdhIo@dpg-d876pqt7vvec738o5r10-a/arcade_hub_db_005a')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    
    # Fix postgres to postgresql protocol
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Allow non-HTTPS in development
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # WTForms
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Admin
    ADMIN_SECRET_KEY = os.environ.get('ADMIN_SECRET_KEY', 'secure-admin-key-2026')
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
