"""REST API for signing up/in account"""
import flask
import server
from server.utils import auth as auth2
from server.utils.returns import successJSON, LoginError, missingJSON
from server.utils.common import getBID

from  firebase_admin import auth

# This just for testing, will remove for production
# Input looks like {email: x}
@server.app.route('/api/v1/test',
                    methods=["POST"])
def test_signin():
    bid=getBID(flask.request.json['email'])
    if bid==-1:
        return LoginError("Invalid email to login with")
    flask.session['bid'] = bid
    print(flask.session['bid'])
    return successJSON('signed in!')


@server.app.route('/api/v1/account/signup', methods=["POST"])
def signing_up():
    if 'Authorization' not in flask.request.headers:
        return LoginError("Signing up witout Firebase header")

    if 'name' not in flask.request.json:
        return missingJSON("name")

    if 'description' not in flask.request.json:
        return missingJSON("description")

    # Verify Firebase auth.
    id_token = flask.request.headers['Authorization']
    decoded_token = auth.verify_id_token(id_token)
    if not decoded_token:
        return LoginError("Invalid Firebase Token")

    uid = decoded_token['uid']
    print("{} trying to make account".format(uid))

    connection = server.model.get_db()
    cur = connection.execute("""
        SELECT bid FROM businesses
        WHERE uid = :uid""", {'uid': uid})
    a = cur.fetchone()
    if a is not None:
        return LoginError("User already signed up")

    name = flask.request.json['name']
    description = flask.request.json['description']
    connection.execute("""
        INSERT INTO businesses
        (uid, name, description)
        VALUES (:uid, :name, :description)""",
            {
                'uid':              uid,
                'name':             name,
                'description':      description
            }
        )
    print("{} account made".format(uid))
    return successJSON('account created!')


@server.app.route('/api/v1/account/signin', methods=["POST"])
def signing_in():
    if 'Authorization' not in flask.request.headers:
        return LoginError("Signing in witout Firebase header")
    
    # Verify Firebase auth.
    id_token = flask.request.headers['Authorization']
    decoded_token = auth.verify_id_token(id_token)
    if not decoded_token:
        return LoginError("Invalid Firebase Token")

    uid = decoded_token['uid']
    print("{} trying to sign in".format(uid))

    connection = server.model.get_db()
    cur = connection.execute("""
        SELECT bid FROM businesses
        WHERE uid = :uid""", {'uid': uid})
    a = cur.fetchone()
    if a is None:
        return LoginError("User not signed up")

    flask.session['bid']=a['bid']
    print("{} signed in (bid: {})".format(uid, a['bid']))
    return retrieve_account()


# Input looks like {name:'new name',
# description: 'this is ..'}
# note there can be any subset of {name, description}
# don't have to have all, others assumed to not change
@server.app.route('/api/v1/account/update',
                    methods=["POST"])
@auth2.api_require
def update_account():
    # Get bid
    bid = flask.session['bid']
 
    options = {'name', 'description'}
    connection = server.model.get_db()
    for k, v in flask.request.json.items():
        if k in options:
            query = "UPDATE businesses SET {} = :v WHERE bid=:a".format(k)
            connection.execute(query,  {'a':bid, 'v':v})
    
    return successJSON("Account updated")


# Input looks like {}
@server.app.route('/api/v1/account/retrieve',
                    methods=["GET"])
@auth2.api_require
def retrieve_account():
    # Get bid
    bid = flask.session['bid']

    connection = server.model.get_db()
    cur = connection.execute("""SELECT bid, name, description FROM
        businesses WHERE bid=:a""",
        {'a': bid})
    info = cur.fetchone()
    return flask.jsonify(**info)


def login_account():
    email = flask.request.json['email']
    password_in = flask.request.json['password']
    connection = server.model.get_db()
    cur = connection.execute("""
        SELECT password FROM businesses WHERE email=:a""",
        {'a': email})
    password = cur.fetchone()
    if password == '':
        return LoginError('Account does not exist')
    elif password == password_in:
        return LoginError('Wrong password')
    else :
        context = {
            'message': "Login success",
            'status_code': 201
        }
    return flask.jsonify(**context), 201


# Not yet in use
def temp():
    weekdays = ['1','2','3','4','5','6','7']
    open_times, end_times = {}, {}
    for weekday in weekdays:
        open_times[weekday] = flask.request.json['open_time'][weekday]
        end_times[weekday] = flask.request.json['end_time'][weekday]
    phone_number = flask.request.json['phone_number']

    name = flask.request.json['name']
    email = flask.request.json['email']
    password = flask.request.json['password']
    address_street = flask.request.json['address_street']
    address_city = flask.request.json['address_city']
    address_state = flask.request.json['address_state']
    zipcode = flask.request.json['zipcode']


    connection = server.model.get_db()
    connection.execute("""
        INSERT INTO businesses
        (name, email, password, address_street, address_city, address_state, zipcode)
        VALUES (:email, :password, :address_street, :address_city, :address_state, :zipcode)""",
            {
                'name':             name,
                'email':            email,
                'password':         password,
                'address_street':   address_street,
                'address_city':     address_city,
                'address_state':    address_state,
                'zipcode':          zipcode

            }
        )
    bid = getBID(email)
    for weekday in weekdays:
        connection.execute("""
            INSERT INTO opening_hours
            (bid, weekday, open_time, end_time)
            VALUES (:bid, :weekday, :open_time, :end_time)""",
                {
                    'bid':          bid,
                    'weekday':      weekday,
                    'open_time':    open_times[weekday],
                    'end_time':     end_times[weekday]

                }
            )

    connection.execute("""
        INSERT INTO contact
        (bid, phone_number)
        VALUES (:bid, :phone_number)""",
            {
                'bid':          bid,
                'phone_number': phone_number
            }
        )
