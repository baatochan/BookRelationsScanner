from flask.views import MethodView
from app.services.gfdGenerator import main
from flask import request


class Gdf(MethodView):
    def post(self):
        dataFromJson = request.get_json()
        try:
            d = main(dataFromJson['text'], dataFromJson['filename'])
            return d
        except Exception as e:
            print("Failed to add new data: ", e)
            return str(500)

    def get(self):
        return "Work"
