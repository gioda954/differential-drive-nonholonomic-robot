from flask import Flask


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    from .routes import calculator_bp

    app.register_blueprint(calculator_bp)
    return app


app = create_app()


__all__ = ["app", "create_app"]
