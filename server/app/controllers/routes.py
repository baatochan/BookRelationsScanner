from flask import request
from . import controllers
from flask import jsonify
from .. import services


@controllers.route('/', methods=['GET', 'POST'])
def index():
    services.ccl_orths()
    return 'ADAM JUPIKAJEJ KURWA';


@controllers.route('/methodOne', methods=['POST'])
def metOne():
    if request.method == 'POST':
        dataFromJson = request.get_json()

        if dataFromJson:
            try:
                text = dataFromJson['text']
                return text
            except Exception as e:
                print("Failed run text analize method: ", e)
                return 500
        return 500


def testFunction():
    return "testowa funkcja\n"
