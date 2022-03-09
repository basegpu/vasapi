from flask import Flask
from .VasaloppetResultsWrapper import *

app = Flask('vasapi')

wrapper = VasaloppetResultsWrapper()

from vasaloppet import routes