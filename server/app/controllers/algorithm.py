from flask.views import MethodView
from app.services.textAnalyse import main
from flask import request


class Algorithm(MethodView):
    def post(self):
        dataFromJson = request.get_json()
        return main(dataFromJson['text'])
