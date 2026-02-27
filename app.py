"""Fikri Production – Main Flask App"""
import os
from flask import Flask
from models import init_db
from routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fikri-production-2025')
    app.config['MAX_CONTENT_LENGTH'] = 210 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    app.config['POSTER_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'posters')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['POSTER_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images'), exist_ok=True)
    init_db(app)
    register_routes(app)
    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
