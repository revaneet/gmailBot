from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

def connectToDB(msg,sender):
    client=MongoClient("mongodb+srv://admin:admin@cluster0-3lmbr.mongodb.net/test?retryWrites=true&w=majority")
    db=client.get_database('gmailBotDB')
    records=db.gmailBotCollection
    new_record={
        'sender':sender,
        'msg':msg    
    }
    records.insert_one(new_record)


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')
    connectToDB(msg,sender)

    # Create reply
    resp = MessagingResponse()
    resp.message(fetch_reply(msg,sender))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)