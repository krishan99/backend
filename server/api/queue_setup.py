"""REST API for setting up queues."""
import flask
import server
from server.utils import auth
from server.utils.returns import missingJSON, permissionError, logicError, successJSON
from server.utils.common import getBID, checkQIDwithBID, checkQnamewithBID


# Input looks like {qid: x}
@server.app.route('/api/v1/queue/delete',
                    methods=["POST"])
@auth.api_require
def delete_q():
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
    connection.execute("""DELETE FROM
        queues WHERE qid=:a""",
        {'a': qid})

    query = "DROP TABLE queue_qid{}".format(qid)
    connection.execute(query)

    return successJSON("Queue deleted")


# Input looks like {qid: x, qname:'new name',
# code:'1234', description: 'this is ..'}
# note there can be any subset of {qname, code, description}
# don't have to have all, others assumed to not change
@server.app.route('/api/v1/queue/update',
                    methods=["POST"])
@auth.api_require
def update_q():
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
    options = {'qname', 'code', 'description'}
    connection = server.model.get_db()
    for k, v in flask.request.json.items():
        if k in options:
            query = "UPDATE queues SET {} = :v WHERE qid=:a".format(k)
            connection.execute(query,  {'a':qid, 'v':v})
    
    return successJSON("Queue updated")


# Input looks like {qid: x}
@server.app.route('/api/v1/queue/retrieve',
                    methods=["GET"])
@auth.api_require
def retrieve_q():
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
    cur = connection.execute("""SELECT qid, qname, code, description FROM
        queues WHERE qid=:a""",
        {'a': qid})
    info = cur.fetchone()
    return flask.jsonify(**info)


# Input looks like {qname: x, description:}
# description optional
@server.app.route('/api/v1/queue/make',
                    methods=["POST"])
@auth.api_require
def make_q():
    # Check if input is right
    if 'qname' not in flask.request.json:
        return missingJSON("qname")
    
    desc = ""
    if 'description' in flask.request.json:
        desc = flask.request.json['description']
    
    # Get bid
    bid = flask.session['bid']
    
    # Check if qname with bid already exists
    qname = flask.request.json['qname']
    if checkQnamewithBID(bid, qname):
        return logicError("Queue with this name already exists")
    
    # Now they are authenticated and qname doesn't exist yet
    if len(qname) < 5:
        return logicError("Queue name must be at least 5 characters")
        
    # At some point generate fancier codes
    connection = server.model.get_db()
    cur = connection.execute("""SELECT COUNT(*) as c FROM queues
        WHERE bid=:a """, {'a': bid})
    count = cur.fetchone()['c']
    code = bid*100 + 4 + 7*count
    print("Code: {}".format(code))

    connection.execute("""INSERT INTO queues 
        (bid, qname, code, description)
        VALUES (:bid, :qname, :code, :desc)""",
            {'bid':bid,
            'qname':qname,
            'code':code,
            'desc':desc}
        )
    cur = connection.execute("""SELECT qid FROM queues 
        WHERE bid=:a AND qname=:b""",
            {'a':bid,
            'b':qname}
        )
    qid = cur.fetchone()['qid']
    # This would be nicer but isn't working rn
    # query = "CREATE TABLE queue_qid{} AS \
    #    SELECT * FROM queue_qid0".format(qid)
    query = "CREATE TABLE queue_qid{}( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        name VARCHAR(20) NOT NULL, \
        phone VARCHAR(20) NOT NULL, \
        note VARCHAR(100) NOT NULL, \
        created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL \
        )".format(qid)
    connection.execute(query)
    
    cur = connection.execute("""SELECT qid, qname, code, description FROM
        queues WHERE qid=:a""",
        {'a': qid})
    info = cur.fetchone()
    
    print("Queue created. Name: {} Qid: {}".format(qname, qid))
    return flask.jsonify(**info)


# Input looks like {} (empty)
@server.app.route('/api/v1/queue/retrieve_all',
                    methods=["GET"])
@auth.api_require
def retrieve_all():
    # Get bid
    bid = flask.session['bid']
  
    # Now we look for their queues
    connection = server.model.get_db()
    cur = connection.execute("""SELECT qid, qname, code, description FROM
        queues WHERE bid=:a""",
        {'a': bid})
    info = cur.fetchall()
    return {
        'queues': info
    }
