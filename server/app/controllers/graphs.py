from flask.views import MethodView
from app.services.textAnalyse import main
from flask import request, json
from app.services.db import db
from app.models.graph import Graph


class Graphs(MethodView):
    def get(self):
        try:
            graphs = Graph.query.with_entities(Graph.id, Graph.name, Graph.ready).all()
            return '{"ghraps":' + json.dumps(graphs) + '}'
        except Exception as e:
            print("Failed get ghraps data: ", e)
            return str(500)
