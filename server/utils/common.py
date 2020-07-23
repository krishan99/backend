"""Commonly used queries"""
import flask
import server

def getBID(email):
    connection = server.model.get_db()
    cur = connection.execute("""SELECT bid FROM
            businesses WHERE email=:a""",
            {'a': email})
    a = cur.fetchone()
    if a is None:
        return -1
    bid = a['bid']
    return bid

def checkQIDwithBID(b, q):
    connection = server.model.get_db()
    cur = connection.execute("""SELECT COUNT(*) as c FROM
        queues WHERE qid=:a AND bid=:b""",
        {'a': q, 'b': b})
    if cur.fetchone()['c']==1:
        return True
    return False

def checkQnamewithBID(b, q):
    connection = server.model.get_db()
    cur = connection.execute("""SELECT COUNT(*) as c FROM
        queues WHERE qname=:a AND bid=:b""",
        {'a': q, 'b': b})
    if cur.fetchone()['c']==1:
        return True
    return False

def checkQID(q):
    connection = server.model.get_db()
    cur = connection.execute("""SELECT COUNT(*) as c FROM
        queues WHERE qid=:a""",
        {'a': q})
    if cur.fetchone()['c']==1:
        return True
    return False
    