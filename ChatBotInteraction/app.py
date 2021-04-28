from flask import Flask, render_template, session, request, jsonify, g
from flask_session import Session
from datetime import timedelta
from services import main as chatbot , Question_Table as qt
import json
import os
import uuid
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = "some_random"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT']= False
# Make the WSGI interface available at the top level so wfastcgi can get it.
#wsgi_app = app.wsgi_app

chatbotTraits  ={
    "Active" : "F",
    "qTableWrite": "F",
    "ratingAverage": 0.0,
    "rates": []
    }

database = qt.sqlConnection()
qt.sqlCreateTable(database)

Session(app)

@app.route('/')
def sessions():
    print("Start Site")
    return render_template('chat.html')

@app.route('/startchat', methods=['GET', 'POST'])
def startSession():
    username = request.form['username']
    email = request.form['email']
    sessionName = request.form['seshName']
    print(str(username))
    session['userLogs'] = []
    session['responseLogs'] = []
    session['username'] = username
    session['email'] = email
    session['sessionName'] = sessionName
    session['active'] = "true"
    uid = str(uuid.uuid4())
    session['userID'] = uid
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=180)
    startPackage = {
        "username": username,
        "chatTitle": sessionName
        }
    startPackage = {str(key): value for key, value in startPackage.items()}
    return jsonify(startPackage=startPackage);

def commandImpl(command):
    switcher ={
        "logs": "chatlogs",
        "clear": "clearlogs",
        "end":"endsession",
        "help": "helpPrompt",
        }
    r = switcher.get(command, "Invalid Command")
    return r

def getChatbotResponse(msg):
    while chatbotTraits["Active"] ==  "T" :
        time.sleep(1)
    chatbotTraits["Active"] = "T"
    m = chatbot.predict_message(msg)
    response = chatbot.obtain_response(m, chatbot.intents)
    chatbotTraits["Active"] = "F"
    time.sleep(1)
    return response

def writeToQtable(msg):
    while chatbotTraits["qTableWrite"] ==  "T" :
        time.sleep(1)
    chatbotTraits["qTableWrite"] =  "T"
    qt.questionInsert(str(session['userID']), str(session['username']), str(session['email']),msg,database)
    chatbotTraits["qTableWrite"] =  "F"

def interpretMessage(msg, uid, ul, rl):
    inputType = "none"
    response = "You Shouldn't See This"
    ucl = ul
    rcl = rl
    avgRating = 0
    if (msg[0] == '!'):
        print("Do command procedure")
        inputType = "command"
        if msg[1:8] == 'insert ':
            writeToQtable(msg[8:len(msg)])
            response = "insert"
        elif msg[1:6] == 'rate ' and len(msg) == 7:
            try:
                if int(msg[6])>= 0 and int(msg[6]) <= 5 :
                    u = chatbotTraits['rates']
                    u.append(int(msg[6]))
                    total = 0
                    for r in u:
                        total = total + r
                    chatbotTraits['ratingAverage'] = total/len(u)
                    avgRating = chatbotTraits['ratingAverage']
                    response = "rating"
                else:
                    response = "Invalid Command"
            except:
                response = "Invalid Command"
            
        else:
            response = commandImpl(msg[1:])
        
    else:
        print("Search for Response using msg")
        response = getChatbotResponse(msg)
        inputType = "question"
        ucl.append(msg)
        rcl.append(response)
        

    messageData = {
    "inputType": inputType,
    "message": msg,
    "response": response,
    "rating": avgRating,
    "userschatLogs": ucl,
    "responseschatLogs": rcl
    }
    return messageData

@app.route('/join', methods=['GET','POST'])
def handle_input():
    text = request.form.get('msg')
    result = {
        "inputType": "TIMEOUT",
        "message": "ERROR",
        "response": "ERROR",
        "rating": 0,
        "userschatLogs": [],
        "responseschatLogs": []
        }
    if 'userID' in session:
        ucl = session['userLogs']
        rcl = session['responseLogs']
        result = interpretMessage(str(text), str(session['userID']), ucl, rcl)
        if request.method == "POST":
            if (result["inputType"] == "question") :
                session['userLogs'] = result['userschatLogs']
                session['responseLogs'] = result['responseschatLogs']
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result);

@app.before_request
def before_request():
    g.user = None
    if 'userID' in session:
        g.user = session['userID']
    else:
        print("Session does not exist")
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

