
from flask import Flask, render_template, session, request ,jsonify
from flask_session import Session
import json
import os
import secrets
app = Flask(__name__)
app.config['SECRET_KEY'] = "some_random"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT']= False
# Make the WSGI interface available at the top level so wfastcgi can get it.
#wsgi_app = app.wsgi_app

#Data Used to store users chatlogs NOTE: THIS DATA SHOULD BE TEMPORARY AS THIS WILL NOT WORK WITH MULTIPLE USERS WE NEED A DATA BASE TO STORE USER INFORMATION

chatlogs = {
    "userChatLogs": [],
    "responseChatLogs": []
    }

Session(app)

@app.route('/')
def sessions():
    if ('userLogs' not in session and 'responseLogs' not in session) :
        session['userLogs'] = []
        session['responseLogs'] = []
    return render_template('form.html')

def interpretMessage(msg):
    inputType = "none"
    response = "You Shouldn't See This"
    if (msg[0] == '!'):
        print("Do command procedure")
        inputType = "command"
        response = "Command Entered"
    else:
        print("Search for Response using msg")
        response = "Hello this is a default response as this part is not implemented yet"
        inputType = "question"
        

    messageData = {
    "inputType": inputType,
    "message": msg,
    "response": response
    }
    return messageData

@app.route('/join', methods=['GET','POST'])
def handle_input():
    text = request.form['msg']
    result = interpretMessage(str(text))
    if request.method == "POST":
        userLogs = result["message"]
        responseLogs = result["response"]
        if ('userLogs' in session and 'responseLogs' in session) :
            chatlogs["userChatLogs"].append(str(userLogs))
            chatlogs["responseChatLogs"].append(str(responseLogs))
            session['userLogs'] = chatlogs["userChatLogs"]
            session['responseLogs'] = chatlogs["responseChatLogs"]
            
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result);


#Main Dev Server to test on
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST,PORT)

