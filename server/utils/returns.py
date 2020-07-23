"""Common return jsons"""
import flask


def missingJSON(s):
    context = {
        'message': "JSON Missing Field(s) {}".format(s),
        'status_code': 405
    }
    return flask.jsonify(**context), 405

def goodJSON(arr):
    for i in arr:
        if i not in flask.request.json:
            return i
    return ""

def permissionError():
    context = {
        'message': "Forbidden",
        'status_code': 403
    }
    return flask.jsonify(**context), 403

def logicError(s):
    context = {
        'message': s,
        'status_code': 404
    }
    return flask.jsonify(**context), 404

def LoginError(s):
    context = {
        'message': s,
        'status_code': 406
    }
    return flask.jsonify(**context), 406

def successJSON(s):
    context = {
        'message': s,
        'status_code': 200
    }
    return flask.jsonify(**context), 200
