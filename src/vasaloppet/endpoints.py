from flask_restful import Resource
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from werkzeug.exceptions import *
from .models import *
from .schemas import *
from .utils import *
from . import container

class ResultFinder(MethodResource, Resource):
    @doc(
        tags=['raw'],
        description='Get the result of single lopper for specific year, defined by sex (M/W) and place.',
        params={
            'year': {
                'description': 'The year of the Vasaloppet race.',
                'example': 2022
            },
            'sex': {
                'description': 'M for male, W for female lopper.',
                'example': 'W'
            },
            'place': {
                'description': 'The ranking among M or W.',
                'example': 314
            }
        })
    @marshal_with(ResultSchema)
    def get(self, year, sex, place):
        try:
            log_to_console('GET: result data for year %i, sex %s, and place %i'%(year, sex, place))
            result = container.Get(year, Sex[sex.upper()], place)
        except Exception as e:
            raise BadRequest(e)
        return ResultSchema().dump(result)

class CacheManager(MethodResource, Resource):
    @doc(
        tags=['ops'],
        description='Get the number of cached results and the corresponding total size (bytes) in memory.'
    )
    @marshal_with(CacheSizeSchema)
    def get(self):
        try:
            log_to_console('GET: cache size')
            cacheStatus = container.GetCacheSize()
        except Exception as e:
            raise BadRequest(e)
        return CacheSizeSchema().dump(cacheStatus)
