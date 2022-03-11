import sys

def log_to_console(msg, isError=False):
    if isError:
        msg = 'ERROR: %s'%msg
    print(msg, file=sys.stderr)