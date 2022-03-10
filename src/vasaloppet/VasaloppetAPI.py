from flask_restful import Resource
from werkzeug.exceptions import *
from .VasaloppetResultsWrapper import Sex
from .utils import *
from . import wrapper

class EventFinder(Resource):
    def get(self, year):
        try:
            log_to_console('GET: event ID for year %i'%year)
            event = wrapper.FindEventIdForYear(int(year))
        except Exception as e:
            log_to_console('no event ID found for year %i'%year, isError=True)
            raise BadRequest(e)
        return event

class ResultFinder(Resource):
    def get(self, year, sex, place):
        try:
            log_to_console('GET: result data for year %i, sex %s, and place %i'%(year, sex, place))
            result = wrapper.FindResultForYearSexPlace(year, Sex[sex.upper()], place)
            jsonStr = obj_to_json(result)
        except Exception as e:
            raise BadRequest(e)
        return jsonStr
