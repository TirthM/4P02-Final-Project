import sqlite3

def sqlConnection():
    try:
        database = sqlite3.connect("Question_Table.db", check_same_thread= False)
        return database
    except:
        return False

def sqlCreateTable(database):
    cur_object = database.cursor()
    cur_object.execute("CREATE TABLE IF NOT EXISTS questions (sessionid TEXT PRIMARY KEY, name TEXT, email TEXT, question TEXT)")
    database.commit()

def sqlInsert(database, values):
    cur_object = database.cursor()
    cur_object.execute("INSERT INTO questions (sessionid, name, email, question) VALUES (?,?,?,?)", values)
    database.commit()

def questionInsert(uid, username, email, msg, dbValues):
    sessionid = uid
    name = username
    email = email
    question = msg
    values = (sessionid, name, email, question)
    sqlInsert(dbValues, values)

