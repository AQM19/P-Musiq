from flask import Flask
from app.models import Config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    from app.routes import index_bp
    from app.routes import list_bp
    from app.routes import video_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(list_bp)
    app.register_blueprint(video_bp)

    return app
