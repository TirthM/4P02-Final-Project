"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
 """

from flask import Flask, render_template, session, request ,jsonify
import json
import os
import secrets
app = Flask(__name__)


# Make the WSGI interface available at the top level so wfastcgi can get it.
#wsgi_app = app.wsgi_app

#Data Used to store users chatlogs
UserData = {
      "UserchatLogs": [],
      "ResponseLogs": [] 
    }

@app.route('/')
def sessions():
    """Renders a sample page."""
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
        UserData["UserchatLogs"].append(str(msg))
        UserData["ResponseLogs"].append(response)
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

