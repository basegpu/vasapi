import sys
import json

def log_to_console(msg, isError=False):
    if isError:
        msg = 'ERROR: %s'%msg
    print(msg, file=sys.stderr)

def obj_to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)