import flask
from flask_socketio import emit
from server import socketio

import time

import server

def refesh_room(qid):
    info = get_qpeople(qid)
    print("Sending: update {}".format(qid))
    socketio.emit("update {}".format(qid), info, room=int(qid))

def get_qpeople(qid):
    connection = server.model.get_db()
    query = "SELECT * FROM queue_qid{} \
        ORDER BY id ASC".format(qid)
    cur = connection.execute(query)
    line = cur.fetchall()

    query = "SELECT MAX(created) as t \
        FROM queue_qid{}".format(qid)
    cur = connection.execute(query)
    t = cur.fetchone()['t']

    return {
        'qid': qid,
        'line': line,
        'last_update': t
    }
