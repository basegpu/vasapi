from flask_restful import Resource
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from werkzeug.exceptions import *
from .models import *
from .schemas import *
from .utils import *
from . import wrapper

class EventFinder(MethodResource, Resource):

    @doc(
        tags=['raw'],
        description='Get the Vasaloppet event ID for specific year.',
        params={'year': 
        {
            'description': 'The year of the Vasaloppet race.',
            'example': '2022'
        }
    })
    @marshal_with(EventSchema)
    def get(self, year):
        try:
            log_to_console('GET: event ID for year %i'%year)
            event_id = wrapper.FindEventIdForYear(year)
            event = Event(year, event_id)
        except Exception as e:
            log_to_console('no event ID found for year %i'%year, isError=True)
            raise BadRequest(e)
        return EventSchema().dump(event)

class ResultFinder(Resource):
    def get(self, year, sex, place):
        try:
            log_to_console('GET: result data for year %i, sex %s, and place %i'%(year, sex, place))
            result = wrapper.FindResultForYearSexPlace(year, Sex[sex.upper()], place)
            jsonStr = obj_to_json(result)
        except Exception as e:
            raise BadRequest(e)
        return jsonStr
