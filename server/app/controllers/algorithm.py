from flask.views import MethodView
from app.services.textAnalyse import main
from flask import request
from app.services.db import db
from app.models.graph import Graph


class Algorithm(MethodView):
    def post(self):
        dataFromJson = request.get_json()
        n = dataFromJson['name']
        g = Graph(ready=0, nodesData="", name=n,
                  settings="")
        db.session.add(g)
        db.session.commit()

        main(dataFromJson['text'], g.id)
        return str(g.id)

    def get(self):
        gID = request.args.get('id')
        g = Graph.query.filter_by(id=gID).first()

        if g.ready:
            json = g.toJSON()
            return '{"status":"ready", "graph":' + str(json) + '}'
        else:
            return '{"status":"analyzing"}'
