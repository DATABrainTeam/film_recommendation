from flask import Flask

def create_app():
    #------------------------------------------- INIT -------------------------------------
    app = Flask(__name__)

    #----------------------------------------- ROUTES -------------------------------------
    from app_container.routes import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    return(app)