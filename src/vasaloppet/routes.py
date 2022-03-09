from flask import Flask
from werkzeug.exceptions import *
from vasaloppet import app, wrapper
from vasaloppet.VasaloppetResultsWrapper import Sex
from .utils import *

@app.route("/event/<year>")
def event_id(year):
    try:
        log_to_console('GET: event ID for year ' + year)
        event = wrapper.FindEventIdForYear(int(year))
    except Exception as e:
        log_to_console('no event ID found for year ' + year, isError=True)
        raise BadRequest(e)
    return event

@app.route("/result/<year>/<sex>/<place>")
def result(year, sex, place):
    try:
        log_to_console('GET: result data for year %s, sex %s, and place %s'%(year, sex, place))
        event = wrapper.FindEventIdForYear(int(year))
        url = wrapper.GetResultUrl(event, Sex[sex.upper()], int(place))
        result = wrapper.ParseResult(url)
        jsonStr = obj_to_json(result)
    except Exception as e:
        raise BadRequest(e)
    return jsonStr
