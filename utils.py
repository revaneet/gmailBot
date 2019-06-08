import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gmailbotKey.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = <YOUR PROJECT ID>

import ezgmail

from quickstart import main
# main()
# ezgmail.init()

def mail_summary():
    #print(parameters.get('Body'))
    main()
    ezgmail.init()
    unreadThreads = ezgmail.unread(maxResults=5)
    print(unreadThreads)
    return unreadThreads

def send_mail(parameters):
    main()
    ezgmail.init()
    print(parameters)
    toEmail=parameters['email']
    subject=parameters['sub_email']
    body=parameters['body_email']
    print(toEmail,subject,body,sep="  ")
    ezgmail.send(toEmail,subject,body)



def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg,session_id):
    response=detect_intent_from_text(msg,session_id)
    if response.intent.display_name=='check_email':
        print("in fetch_reply IF")
        unreadThreads=mail_summary()
        #unreadThreadsUtils=ezgmail.messages(unreadThreads)
        unreadThreads_summary="here are emails:"
        
        for row in unreadThreads:
            msg=row.messages[0]
            unreadThreads_summary+="\n\n{}\n\n{}\n\n".format(msg.subject,msg.snippet)
        print(unreadThreads_summary)
        return unreadThreads_summary
    elif response.intent.display_name=='send_email' :
        send_mail(response.parameters)
        temp="Email sent to {}".format(response.parameters['email'])
        return temp
    else:
        return response.fulfillment_text
