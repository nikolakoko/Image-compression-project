import os
from flask import Flask
from flask_cors import CORS
from database import db, init_db
from routes import register_routes


def create_app():
    app = Flask(__name__)
    database_url = os.environ.get('DATABASE_URL')

    # Database configuration - support both SQLite and PostgreSQL
    if database_url:
        # Production/Docker - use PostgreSQL
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Development fallback - use SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///compressions.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

    # Enable CORS for all routes
    CORS(app)

    # Initialize database
    db.init_app(app)

    # Register routes
    register_routes(app)

    # Create tables using your function
    with app.app_context():
        init_db()  # Using your function instead of db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
