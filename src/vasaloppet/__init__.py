from flask import Flask
from flask_restful import Api
from .VasaloppetResultsWrapper import *

app = Flask(__name__)
api = Api(app)
wrapper = VasaloppetResultsWrapper()

from vasaloppet.VasaloppetAPI import *

api.add_resource(EventFinder, '/event/<int:year>')
api.add_resource(ResultFinder, '/result/<int:year>/<string:sex>/<int:place>')