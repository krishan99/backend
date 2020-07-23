"""REST API for using queues by customer."""
import flask
import server
from server.utils.returns import missingJSON, permissionError, logicError, successJSON, goodJSON
from server.utils.common import checkQID
from server.utils.notification import notify
from server.utils.sockethelper import refesh_room

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import phonenumbers

# Input looks like {code: x}
@server.app.route('/api/v1/queue/user/getform',
                    methods=["POST"])
def get_form_q():
    # Check if input is right
    if 'code' not in flask.request.json:
        return missingJSON("code")
    
    code = flask.request.json['code']

    connection = server.model.get_db()
    cur = connection.execute("""SELECT queues.qid as qid, 
        businesses.name as name
        FROM queues INNER JOIN businesses 
        ON queues.bid = businesses.bid
        WHERE queues.code=:a""", {'a':code}
        )
    a = cur.fetchone()
    if a is None:
        return logicError("Invalid code")

    qid = a['qid']
    name = a['name']
    # Eventually will have custom queue form
    context = {
        'qid': qid,
        'code': code,
        'business': name,
        'Name: ': 'string',
        'Phone: ': 'string'
    }
    return flask.jsonify(**context)


# Input looks like {qid: qid, name:"", phomne:""}
@server.app.route('/api/v1/queue/user/postform',
                    methods=["POST"])
def post_form_q():
    # Check if input is right
    t = goodJSON(['qid', 'name', 'phone'])
    if t != "":
        return missingJSON(t)

    qid = flask.request.json['qid']
    name = flask.request.json['name']
    raw_phone = flask.request.json['phone']

    if not checkQID(qid):
        return logicError("Invalid queue id")

    try:
        z = phonenumbers.parse(raw_phone, region="US")
    except phonenumbers.NumberParseException as e:
        print(e)
        return logicError("Invalid phone number")
    
    phone = phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.E164)

    connection = server.model.get_db()
    query = "SELECT COUNT(*) as c FROM \
        queue_qid{} WHERE phone=:phone".format(qid)
    cur = connection.execute(query, {'phone':phone})
    if cur.fetchone()['c'] != 0:
        return logicError("Phone number already in queue")

    query = "INSERT INTO queue_qid{} \
        (name, phone, note) \
        VALUES (:name, :phone, :note)".format(qid)
    connection.execute(query,
            {'name':name,
            'phone':phone,
            'note': ""}
        )
    cur = connection.execute("""SELECT businesses.name as name
        FROM queues INNER JOIN businesses 
        ON queues.bid = businesses.bid
        WHERE queues.qid=:a""", {'a':qid}
        )
    a = cur.fetchone()
    notify(phone, "{}, you have been added to the queue for {}!".format(name, a['name']))
    notify(phone, "Send \"[code]: Q \" to leave the queue at any time. You'll be messaged when to enter the store.")
    print("{} added to the qid {}".format(name, qid))
    refesh_room(qid)
    
    return successJSON("Added to queue!")

'''
@server.app.route('/api/v1/sms', methods=["POST"])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    print("Recieved a text from {}".format(number))
    resp = twiml.Response()

    connection = server.model.get_db()
    cur = connection.execute("SELECT qid, status FROM \
        users WHERE phone=:phone", {'phone':phone})
    data = cur.fetchone()
    # note yet in any queue
    if data is None:
        code = message_body
        cur = connection.execute("""SELECT queues.qid as qid, 
            businesses.name as name
            FROM queues INNER JOIN businesses 
            ON queues.bid = businesses.bid
            WHERE queues.code=:a""", {'a':code}
        )
        a = cur.fetchone()
        if a is None:
            resp.message("Hi this is LiveSafe. The code entered is invalid, please respond with a valid queue code")
            return str(resp)
        qid = a['qid']
        cur = connection.execute("INSERT INTO users (phone, qid) \
            VALUES (:phone, :qid)", {'phone':phone, 'qid': qid})
        resp.message("Hi, welcome to LiveSafe. To join the queue for {}, please enter your name.".format(a['name']))
        return str(resp)
    
    elseif data['status']==0:
        name = message_body

    resp = twiml.Response()
    resp.message('Hello {}, you said: {}'.format(number, message_body))
    return str(resp)
'''
@server.app.route('/api/v1/sms', methods=["POST"])
def sms():
    print("received sms")
    phone = request.form['From']
    message_body = request.form['Body']
    print("Recieved a text from {}".format(phone))
    arr = message_body.split(':')
    resp = MessagingResponse()
    if(len(arr) < 2):
        resp.message("Invalid format. Use \"[code]: name\" to join queue and \"[code]: Q \" to leave the queue")
        return str(resp)
    code = arr[0]
    msg = arr[1]
    connection = server.model.get_db()
    cur = connection.execute("""SELECT queues.qid as qid, 
        businesses.name as name
        FROM queues INNER JOIN businesses 
        ON queues.bid = businesses.bid
        WHERE queues.code=:a""", {'a':code}
        )
    a = cur.fetchone()
    if a is None:
        return logicError("Invalid code")

    qid = a['qid']
    name = a['name']
    if(msg == 'Q'):
        query = "DELETE FROM queue_qid{} \
            WHERE id=:id".format(qid)
        connection.execute(query, {'phone': phone})
        notify(phone, "You have been removed from the queue and will no longer receive messages.")
        refesh_room(qid)
    else:
        query = "SELECT COUNT(*) as c FROM \
            queue_qid{} WHERE phone=:phone".format(qid)
        cur = connection.execute(query, {'phone':phone})
        if cur.fetchone()['c'] != 0:
            resp.message("This phone number is already part of the queue")
            return str(resp)

        query = "INSERT INTO queue_qid{} \
            (name, phone, note) \
            VALUES (:name, :phone, :note)".format(qid)
        connection.execute(query,
                {'name':name,
                'phone':phone,
                'note': ""}
            )
        cur = connection.execute("""SELECT businesses.name as name
            FROM queues INNER JOIN businesses 
            ON queues.bid = businesses.bid
            WHERE queues.qid=:a""", {'a':qid}
            )
        a = cur.fetchone()
        notify(phone, "{}, you have been added to the queue for {}!".format(name, a['name']))
        notify(phone, "Send \"[code]: Q \" to leave the queue at any time. You'll be messaged when to enter the store.")
        print("{} added to the qid {}".format(name, qid))
        refesh_room(qid)
        