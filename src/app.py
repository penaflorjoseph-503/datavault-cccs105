"""
app.py - Main Flask application entry point
"""
from flask import Flask
from config import Config
import db as database
from routes.auth      import auth_bp
from routes.dashboard import dashboard_bp
from routes.employees import employees_bp
from routes.products  import products_bp
from routes.export    import export_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register DB teardown
    database.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(export_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
