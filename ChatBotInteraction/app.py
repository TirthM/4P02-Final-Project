
from flask import Flask, render_template, session, request ,jsonify, g
from flask_session import Session
from datetime import timedelta
import json
import os
import uuid
app = Flask(__name__)
app.config['SECRET_KEY'] = "some_random"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT']= False
# Make the WSGI interface available at the top level so wfastcgi can get it.
#wsgi_app = app.wsgi_app

Session(app)

#Need to implement getting rid of the users in the server after they leave

users = {
    "users" : []
}

@app.route('/')
def sessions():
    if ('userLogs' not in session and 'responseLogs' not in session) :
        session['userLogs'] = []
        session['responseLogs'] = []
        uid = str(uuid.uuid4())
        session['userID'] = uid
        user = {
            "userID": uid,
            "userChatLogs": [],
            "responseChatLogs": []
            }
        users['users'].append(user)
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
    return render_template('chat.html')

def commandImpl(command):
    switcher ={
        "logs": "chatlogs",
        "clear": "clearlogs"
        }
    r = switcher.get(command, "Invalid Command")
    return r
    
def interpretMessage(msg, uid):
    inputType = "none"
    response = "You Shouldn't See This"
    ucl = []
    rcl = []
    if (msg[0] == '!'):
        print("Do command procedure")
        inputType = "command"
        response = commandImpl(msg[1:])
        if(response == "chatlogs"):
            for u in users['users'] :
                if (uid == u['userID']):
                    ucl = u["userChatLogs"]
                    rcl = u["responseChatLogs"]
                    break
    else:
        print("Search for Response using msg")
        response = "Hello this is a default response as this part is not implemented yet"
        inputType = "question"
        

    messageData = {
    "inputType": inputType,
    "message": msg,
    "response": response,
    "userschatLogs": ucl,
    "responseschatLogs": rcl
    }
    return messageData

@app.route('/join', methods=['GET','POST'])
def handle_input():
    text = request.form['msg']
    result = interpretMessage(str(text), str(session['userID']))
    if request.method == "POST":
        userLogs = result["message"]
        responseLogs = result["response"]
        if ('userLogs' in session and 'responseLogs' in session and result["inputType"] == "question") :
            for u in users['users']:
                if (u['userID'] == session['userID']):
                    u["userChatLogs"].append(str(userLogs))
                    u["responseChatLogs"].append(str(responseLogs))
                    session['userLogs'] = u["userChatLogs"]
                    session['responseLogs'] = u["responseChatLogs"]
                    break
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result);

@app.before_request
def before_request():
    g.user = None
    if 'userID' in session:
        g.user = session['userID']
    else:
        print("Session ended")
        #do stuff because session ended

#Main Dev Server to test on
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST,PORT)

