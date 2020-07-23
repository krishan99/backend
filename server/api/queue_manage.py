"""REST API for managing queues."""
import flask
from flask import render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

import server
from server.utils import auth
from server.utils.returns import missingJSON, permissionError, logicError, successJSON
from server.utils.common import getBID, checkQIDwithBID
from server.utils.notification import notify
from server.utils.sockethelper import get_qpeople, refesh_room


@server.socketio.on('connect')
def test_connect():
    # Get bid
    bid = flask.session['bid']
    print("Client {} connected (bid: {})".format(request.sid, bid))

    connection = server.model.get_db()
    cur = connection.execute("SELECT qid FROM \
        queues WHERE bid=:bid", {'bid': bid})
    a = cur.fetchall()
    for i in a:
        join_room(i["qid"])


@server.socketio.on('disconnect')
def test_disconnect():
    print('Client {} disconnected'.format(request.sid))

@server.socketio.on('join')
def on_join(data):
    print('received join: ' + str(data))
    if 'qid' not in data:
        return missingJSON("qid")

    # Get bid from logname
    bid = flask.session['bid']
    
    # Check if qid belongs to their bid
    qid = data['qid']
    if not checkQIDwithBID(bid, qid):
        return permissionError()
    
    # Now they are authenticated and qid exists
    info = get_qpeople(qid)
    emit("update {}".format(qid), info)
    join_room(qid)


@server.socketio.on('leave')
def on_leave(data):
    print('received leave: ' + str(data))
    if 'qid' not in data:
        return missingJSON("qid")
    qid = data['qid']
    leave_room(qid)


# Input looks like {qid: x}
@server.app.route('/api/v1/queue/manage/get',
                    methods=["GET"])
@auth.api_require
def get_q():
    # Check if input is right
    if 'qid' not in flask.request.json:
        return missingJSON("qid")
    
    # Get bid
    bid = flask.session['bid']
    
    # Check if qid belongs to their bid
    qid = flask.request.json['qid']
    if not checkQIDwithBID(bid, qid):
        return permissionError()
    
    # Now they are authenticated and qid exists
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


# Input looks like {qid: x, id: y}
@server.app.route('/api/v1/queue/manage/pop',
                    methods=["POST"])
@auth.api_require
def pop():
    # Check if input is right
    if 'qid' not in flask.request.json or \
        'id' not in flask.request.json:
        return missingJSON("qid or id")
    
    # Get bid
    bid = flask.session['bid']
    
    # Check if qid belongs to their bid
    qid = flask.request.json['qid']
    if not checkQIDwithBID(bid, qid):
        return permissionError()
    
    # Now they are authenticated and qid exists
    id = flask.request.json['id']
    connection = server.model.get_db()
    query = "SELECT name, phone FROM \
        queue_qid{} WHERE id=:id".format(qid)
    cur = connection.execute(query,
        {'id': id})
    info = cur.fetchone()
    if info is None:
        return logicError("Invalid ID to pop")

    notify(info['phone'], "{}, you can come into the store!".format(info['name']))
    query = "DELETE FROM queue_qid{} \
         WHERE id=:id".format(qid)
    connection.execute(query, {'id': id})
    
    print("Popped {} from qid {}".format(id, qid))
    refesh_room(qid)
    
    return successJSON("{} popped!".format(info['name']))


# For mamager to add to queue, just use user functions
# Will leave add to front for beta release with queue editing
