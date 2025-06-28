from flask import Flask
from flask_cors import CORS
from database import db, init_db
from routes import register_routes


def create_app():
    app = Flask(__name__)
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
    app.run(debug=True, host='0.0.0.0', port=5000)
