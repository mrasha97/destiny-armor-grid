"""
Improved Flask application factory with security enhancements.
This version includes logging, error handlers, and security headers.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from app.config import get_config


def create_app(config_name=None):
    """
    Factory function to create and configure the Flask application.

    Args:
        config_name: Environment name ('development', 'production', 'testing')
                    If None, reads from FLASK_ENV environment variable

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    config_obj = get_config(config_name)
    app.config.from_object(config_obj)

    # Setup logging
    setup_logging(app)

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Register error handlers
    register_error_handlers(app)

    # Add security headers
    register_security_headers(app)

    app.logger.info('Destiny 2 Armor Sorter application started')

    return app


def setup_logging(app):
    """
    Configure application logging with rotating file handler.

    Args:
        app: Flask application instance
    """
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        log_folder = app.config.get('LOG_FOLDER', 'logs')
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)

        # Setup rotating file handler
        log_file = os.path.join(log_folder, 'destiny-armor.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=app.config.get('LOG_MAX_BYTES', 10 * 1024 * 1024),
            backupCount=app.config.get('LOG_BACKUP_COUNT', 10)
        )

        # Set log format
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))

        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)


def register_error_handlers(app):
    """
    Register application-wide error handlers.

    Args:
        app: Flask application instance
    """
    from app.services.csv_parser import CSVParserError

    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors."""
        app.logger.warning(f'404 error: {error}')
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        app.logger.error(f'Server Error: {error}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle file too large errors."""
        app.logger.warning(f'File too large: {error}')
        max_size_mb = app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
        return jsonify({
            'error': f'File too large. Maximum size is {max_size_mb:.0f}MB'
        }), 413

    @app.errorhandler(CSVParserError)
    def handle_csv_error(error):
        """Handle CSV parsing errors."""
        app.logger.warning(f'CSV parsing error: {error}')
        return jsonify({'error': str(error)}), 400


def register_security_headers(app):
    """
    Add security headers to all responses.

    Args:
        app: Flask application instance
    """
    @app.after_request
    def add_security_headers(response):
        """Add security headers to response."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # Add CSP header for development/production
        if not app.debug:
            response.headers['Content-Security-Policy'] = (
                "default-src 'self'; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data:; "
                "script-src 'self' 'unsafe-inline'"
            )

        return response

