"""Functions to notify customers."""
import functools
import flask
from twilio.rest import Client

# send text to name with message at phone number
# Eventualy more secure with https://www.twilio.com/docs/usage/secure-credentials
# get from twilio console
client = Client(account_sid, auth_token)

def notify(phone, msg):
    phones = ['+12488207717', '+12488257021', '+12489718090']

    there = False
    for p in phones:
        if phone == p:
            there = True
    if not there:
        return

    try:
        message = client.messages.create(
            body=msg,
            from_='+12024106803',
            to=phone
        )
    except:
        print("Error sending twilio message. Likely unverified number {}".format(phone))
   
    print(message.sid)
