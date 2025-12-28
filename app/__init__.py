from flask import Flask


def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
    app.config['SECRET_KEY'] = 'dev-secret-key-for-local-use-only'

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

