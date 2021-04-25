import sqlite3
import click
from datetime import datetime
from flask import current_app, g
from flask.cli import with_appcontext

# get the list of the lists for a specified userID


def get_lists(username):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT userID FROM users WHERE username = '{username}' ;""".format(
        username=username))
    userIdent = cursor.fetchone()[0]
    # print(userIdent)
    cursor.execute(""" SELECT listID, listname FROM lists WHERE userID = '{userID}'; """.format(
        userID=userIdent))
    db_lists = cursor.fetchall()
    print(db_lists)
    lists = []
    tasks = []

    for i in range(len(db_lists)):
        row = db_lists[i][0]
        lists.append(row)

    for l in lists:
        cursor.execute(
            """ SELECT listID, taskID,taskname,deadline,completion,status FROM tasks WHERE listID = '{listID}'; """.format(listID=l))
        db_tasks = cursor.fetchall()
        for t in db_tasks:
            tasks.append(t)
        print(db_tasks)

    connection.commit()
    cursor.close()
    connection.close()
    overdue = []
    for i in range(len(tasks)):
        if tasks[i][3] != None:
            now = datetime.now()
            date_object = datetime.strptime(tasks[i][3], "%Y-%m-%d %H:%M:%S")
            print("date_object =", date_object)
            if now > date_object:
                print("overdue")
                print(now)
                overdue.append(1)
            else:
                overdue.append(0)

    return db_lists, tasks, overdue


# get the list of the tasks for a specified listID
def get_tasks(list):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT tasktname FROM tasks WHERE listID = '{list}' ORDER BY listID DESC; """)
    db_tasks = cursor.fetchall()
    tasks = []

    for i in range(len(db_tasks)):
        row = db_tasks[i][0]
        tasks.append(row)

    connection.commit()
    cursor.close()
    connection.close()

    return tasks


def get_tasktext(tid):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT taskname,deadline,completion,status FROM tasks WHERE taskID = '{tid}';""".format(tid=tid))
    tasktext = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return tasktext

# create a new list for a specified userID


def add_list(userID, listname):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" INSERT INTO lists(userID, listname, numberoftasks) VALUES ('{userID}', '{listname}', '{numberoftasks}')""".format(
        userID=userID, listname=listname, numberoftasks=0))

    connection.commit()
    cursor.close()
    connection.close()
    print(listname, "successfully added to user", userID)
    return listname + " successfully added to user " + str(userID)

# create a new task for a specified listID


def add_task(listID, taskname):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" INSERT INTO tasks(listID, taskname, completion) VALUES ('{listID}', '{taskname}',0)""".format(
        listID=listID, taskname=taskname))

    cursor.execute(
        """ SELECT numberoftasks FROM lists WHERE listID = '{listID}' ORDER BY listID DESC; """.format(listID=listID))
    newnumberoftasks = cursor.fetchone()[0] + 1

    # cursor.execute(""" UPDATE lists SET numberoftasks = 2 WHERE listID = '{listID}'""".format(listID = listID))
    cursor.execute(""" UPDATE lists SET numberoftasks = '{newnumberoftasks}' WHERE listID = '{listID}'""".format(
        newnumberoftasks=newnumberoftasks, listID=listID))

    connection.commit()
    cursor.close()
    connection.close()

    return print(taskname, "successfully added to list", listID)

# modify a task


def update_task(taskID, newtaskname, newdeadline, newcompletion, newstatus):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" UPDATE tasks SET taskname = '{newtaskname}', deadline='{newdeadline}',completion='{newcompletion}',status='{newstatus}' WHERE taskID = '{taskID}'""".format(
        newtaskname=newtaskname, taskID=taskID, newdeadline=newdeadline, newcompletion=newcompletion, newstatus=newstatus))

    connection.commit()
    cursor.close()
    connection.close()

    return print("Task ID", taskID, "successfully update to ", newtaskname)

# deletes a task based on the taskID


def delete_task(taskID):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute(
        """ SELECT listID FROM tasks WHERE taskID = '{taskID}' ORDER BY listID DESC; """.format(taskID=taskID))
    listID = cursor.fetchone()[0]

    cursor.execute(
        """ DELETE FROM tasks WHERE taskID = '{taskID}'""".format(taskID=taskID))

    cursor.execute(
        """ SELECT numberoftasks FROM lists WHERE listID = '{listID}' ORDER BY listID DESC; """.format(listID=listID))
    newnumberoftasks = max(cursor.fetchone()[0] - 1, 0)

    # cursor.execute(""" UPDATE lists SET numberoftasks = 2 WHERE listID = '{listID}'""".format(listID = listID))
    cursor.execute(""" UPDATE lists SET numberoftasks = '{newnumberoftasks}' WHERE listID = '{listID}'""".format(
        newnumberoftasks=newnumberoftasks, listID=listID))

    connection.commit()
    cursor.close()
    connection.close()

    return print(taskID, "successfully deleted")
# modify a list


def update_list(listID, newlistname):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" UPDATE lists SET listname = '{newlistname}' WHERE listID = '{listID}'""".format(
        newlistname=newlistname, listID=listID))

    connection.commit()
    cursor.close()
    connection.close()

    return print("List ID", listID, "successfully update to ", newlistname)

# deletes a list based on the listID


def delete_list(list):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ DELETE FROM lists WHERE listID = '{list}'""".format(list=list))

    connection.commit()
    cursor.close()
    connection.close()

    return print(list, "successfully deleted")


def check_pw(username):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM users WHERE username = '{username}' ORDER BY userID DESC; """.format(
        username=username))
    password = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return password


def check_pw_admin(username):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM admin WHERE username = '{username}' ORDER BY username DESC; """.format(
        username=username))

    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return password


def signup(username, firstname, lastname, password, email):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM users WHERE username = '{username}' ORDER BY userID DESC; """.format(
        username=username))
    exist = cursor.fetchone()

    if exist is None:
        cursor.execute(""" INSERT INTO users(username, firstname, lastname, password, email)VALUES('{username}', '{firstname}', '{lastname}','{password}','{email}')""".format(
            username=username, firstname=firstname, lastname=lastname, password=password, email=email))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        return('User already existed!!')

    return 'You have successfully signed up!'


def updateSettings(username, firstname, lastname, password, email):

    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""UPDATE users SET firstname='{firstname}',lastname='{lastname}',email='{email}',password='{password}' WHERE username = '{username}'""".format(
        username=username, firstname=firstname, lastname=lastname, password=password, email=email))
    connection.commit()
    cursor.close()
    connection.close()
    return 'Settings successfully updated'


def check_users():
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT username FROM users ORDER BY userID DESC; """)
    db_users = cursor.fetchall()
    users = []

    for i in range(len(db_users)):
        person = db_users[i][0]
        users.append(person)

    connection.commit()
    cursor.close()
    connection.close()

    return users


def get_users():
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT username,userID,firstname,lastname,password,email FROM users ORDER BY userID DESC; """)
    db_users = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()
    print(db_users)
    return db_users


def get_username(userId):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT username FROM users WHERE userID='{userId}'; """.format(userId=userId))
    username = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()
    # print(username)
    return username


def getUserId(username):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT userID FROM users WHERE username='{username}'; """.format(
        username=username))
    db_users = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return db_users[0][0]


def getUserDetails(userId):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT username, firstname, lastname, userID,email,password FROM users WHERE userID='{userId}'; """.format(userId=userId))
    userDetails = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()
    print(userDetails)
    return userDetails


def setLog(userId):
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ INSERT INTO logs(userId) VALUES ('{userId}');""".format(userId=userId))
    connection.commit()

    cursor.close()
    connection.close()


def getLogsCount():
    print("getLogs is running")
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM logs")
    (countLogs,) = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return countLogs


def getListsCount():
    print("getLists is running")
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM lists")
    (countLists,) = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return countLists


def getLastLogsCount():
    print("getLastLogs is running")
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        "select count(*) from logs where log >= datetime('now','-24 hour');")
    (countLogs,) = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return countLogs


def getLastListsCount():
    print("getLastLists is running")
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        "select count(*) from lists where timestamp >= datetime('now','-24 hour');")
    (countLists,) = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return countLists


def getLogsTable():
    print("getLogsTable is running")
    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM logs ORDER BY log DESC")
    logsTable = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return logsTable


def delete_user(uid):
    print("Deleting user", uid)
    username = get_username(uid)
    lists, tasks, unused = get_lists(username)
    print(username)
    print(lists)
    print(tasks)
    for task in tasks:
        delete_task(task[1])
    for list in lists:
        delete_list(list[0])

    connection = sqlite3.connect('project.db', check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute(
        """ DELETE FROM users WHERE userID = '{uid}'""".format(uid=uid))
    cursor.execute(
        """ DELETE FROM logs WHERE userid = '{uid}'""".format(uid=uid))

    connection.commit()
    cursor.close()
    connection.close()

    return print("User ID", uid, "successfully deleted")
