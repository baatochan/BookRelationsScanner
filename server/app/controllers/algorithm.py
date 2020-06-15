from flask.views import MethodView
from app.services.textAnalyse import main
from flask import request
from app.services.db import db
from app.models.graph import Graph


class Algorithm(MethodView):
    def post(self):
        dataFromJson = request.get_json()
        print("data: ", dataFromJson)
        try:
            n = dataFromJson['name']
            g = Graph(ready=0, nodesData="", name=n,
                      settings="")
            db.session.add(g)
            db.session.commit()

            # worker z main(dataFromJson['text']) i id g.id
            main(dataFromJson['text'], g.id)
            return str(g.id)
        except Exception as e:
            print("Failed to add new data: ", e)
            return str(500)

    def get(self):
        gID = request.args.get('id')
        g = Graph.query.filter_by(id=gID).first()

        if g.ready:
            json = g.toJSON()
            return '{"status":"ready", "graph":' + str(json) + '}'
        else:
            return '{"status":"analyzing"}'
