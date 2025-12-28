"""
Configuration management for Destiny 2 Armor Sorter.
Provides environment-specific settings with secure defaults.
"""
import os
from datetime import timedelta


class Config:
    """Base configuration with secure defaults."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    # File Upload Settings
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'csv'}

    # Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Logging
    LOG_FOLDER = 'logs'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 10


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    TESTING = False

    # Less strict in development
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False

    # Strict security in production
    SESSION_COOKIE_SECURE = True

    # Ensure secret key is set
    @classmethod
    def validate(cls):
        """Validate production configuration."""
        if cls.SECRET_KEY == Config.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in production environment")


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    DEBUG = True

    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False

    # Use in-memory session
    SESSION_TYPE = 'filesystem'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    Get configuration object for specified environment.

    Args:
        env: Environment name ('development', 'production', 'testing')
             If None, reads from FLASK_ENV environment variable

    Returns:
        Configuration class for the specified environment
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')

    return config.get(env, config['default'])

