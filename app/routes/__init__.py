from flask import Flask, Blueprint
from app.routes.animes_routes import bp_animes

def init_app(app: Flask):
    app.register_blueprint(bp_animes)