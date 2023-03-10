from flask import Flask
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
import logging
from vasaloppet.scraping import VasaloppetScraper

app = Flask(__name__)
api = Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Vasaloppet Result API',
        version='2022',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/json/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

app.logger.setLevel(logging.INFO)

data_provider = VasaloppetScraper()
app.logger.info('Successfully initialized vasaloppet wrapper.')


from api.endpoints import *

api.add_resource(
    ResultFinder,
    '/result/<int:year>/<string:sex>/<int:place>',
    resource_class_kwargs = {'logger': app.logger}
)
docs.register(ResultFinder)