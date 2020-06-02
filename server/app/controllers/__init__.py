from app.services.app import app
from . import algorithm


def init_routes():
    app.add_url_rule(
        '/methodOne', view_func=algorithm.Algorithm.as_view('methodOne'))
