from flask.views import MethodView


class Algorithm(MethodView):
    def get(self):
        return "Przemek bawi się (swoim) pythonem"
