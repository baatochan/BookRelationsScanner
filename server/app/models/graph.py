from app.services.db import db


class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    ready = db.Column(db.Boolean)
    nodesData = db.Column(db.String(1000000000))
    name = db.Column(db.String(255))

    def __repr__(self):
        return "<Currency data: {} {} {} {} >".format(self.id, self.name, self.ready, self.nodesData)
