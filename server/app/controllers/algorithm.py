from flask.views import MethodView
from app.services.textAnalyse import main
from flask import request
from app.services.db import db


class Algorithm(MethodView):
    def post(self):
        dataFromJson = request.get_json()
        # tworze nową instancje
        # odpalam alg w tle
        # zwracam id osoby do wyświetlenia
        return main(dataFromJson['text'])
