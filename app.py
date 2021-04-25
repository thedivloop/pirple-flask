from flask import Flask, render_template, request, session, redirect, url_for, g
from werkzeug.exceptions import HTTPException
import model
import math
import numpy as np


app = Flask(__name__)
app.secret_key = 'jumpjacks'

administrator = ''
username = ''
user = model.check_users()


@app.route('/', methods=['GET'])
def home():
    if 'username' in session:
        g.user = session['username']
        return render_template('dashboard.html', message=model.get_lists(g.user))
        # message = '<table><tr><td>First Row</td></tr><tr><tr><td>First Row</td></tr><tr><tr><td>First Row</td></tr></table>')
        # add the lists to show here "message ="
    return render_template('homepage.html', message="Log in to the page or sign up!")


@app.route('/terms', methods=['GET'])
def terms():
    status = "out"
    if 'username' in session:
        status = "in"
    return render_template('terms.html', message=status)


@app.route('/privacy', methods=['GET'])
def privacy():
    status = "out"
    if 'username' in session:
        status = "in"
    return render_template('privacy.html', message=status)


@app.route('/about', methods=['GET'])
def about():
    status = "out"
    if 'username' in session:
        status = "in"
    return render_template('about.html', message=status)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('username', None)
        areyouuser = request.form['username']
        pwd = model.check_pw(areyouuser)
        if request.form['password'] == pwd:
            session['username'] = request.form['username']
            model.setLog(model.getUserId(session['username']))
            # countLogs = model.getLogs()
            # print(countLogs)
            return redirect(url_for('home'))
    return render_template('index.html')


@app.before_request
def before_request():
    g.username = None
    if username in session:
        g.username = session['username']


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        # message = 'Please sign up!'
        return render_template('signup.html')
    else:
        username = request.form["username"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        model.signup(username, firstname, lastname, password, email)
        return redirect(url_for('login'))


@app.route('/getsession')
def getsession():
    if 'username' in session:
        return session['username']
    return redirect(url_for('login'))


@app.route('/createlist', methods=['GET', 'POST'])
def createlist():
    if request.method == 'POST':
        list = request.form['list']
        g.user = session['username']
        userID = model.getUserId(g.user)
        model.add_list(userID, list)
        return redirect(url_for('home'))
    else:
        return render_template('createlist.html')


@app.route('/<int:tid>/delete', methods=['GET', 'POST'])
def deletetask(tid):
    model.delete_task(tid)
    # g.user = session['username']
    return redirect(url_for('home'))


@app.route('/<int:lid>/deletelist', methods=['GET', 'POST'])
def deletelist(lid):
    model.delete_list(lid)
    # g.user = session['username']
    return redirect(url_for('home'))


@app.route('/<int:lid>/add', methods=['GET', 'POST'])
def createtask(lid):
    model.add_task(lid, 'new task')
    # g.user = session['username']
    return redirect(url_for('home'))


@app.route('/<int:tid>/updatetask', methods=['GET', 'POST'])
def update_task(tid):
    if request.method == 'POST':
        task = request.form['task']
        deadline = request.form['deadline']
        completion = request.form['completion']
        status = request.form['status']
        g.user = session['username']
        #userID = model.getUserId(g.user)
        model.update_task(tid, task, deadline, completion, status)
        return redirect(url_for('home'))
    else:
        #tasktext = 'this is the text'
        print(model.get_tasktext(tid))
        return render_template('modifytask.html', text=model.get_tasktext(tid))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin.html')
    else:
        session.pop('admin', None)
        areyouadmin = request.form['admin']
        pwd = model.check_pw_admin(areyouadmin)
        if request.form['password'] == pwd:
            session['admin'] = request.form['admin']
            return redirect(url_for('admin_dash'))


@app.route('/admin-dashboard', methods=['GET', 'POST'])
def admin_dash():
    if 'admin' in session:
        countLogs = model.getLogsCount()
        countLogs24h = model.getLastLogsCount()
        countLists = model.getListsCount()
        countLists24h = model.getLastListsCount()
        print(countLogs)
        return render_template('admin-dashboard.html', countLogs=countLogs, countLogs24h=countLogs24h, countLists=countLists, countLists24h=countLists24h)
    return redirect(url_for('admin_login'))


@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    if 'admin' in session:
        page = request.args.get('page', 1, type=int)
        # print("page is: ",page)
        entriesPerPage = 50
        allLogs = np.array(model.getLogsTable())
        totalPages = math.ceil(len(allLogs)/entriesPerPage)
        print("these are all logs")
        print(totalPages)
        # paginatedLogs = allLogs[entriesPerPage*(page-1), entriesPerPage*page-1]
        paginatedLogs = allLogs[entriesPerPage*(page-1): entriesPerPage*page]
        finalLogs = []
        for i in range(len(paginatedLogs)):
            finalLogs.append(
                [model.get_username(paginatedLogs[i][0]), paginatedLogs[i][1], paginatedLogs[i][0]])
        return render_template('admin-userslist.html', logs=finalLogs, page=page, totalPages=totalPages)
    return redirect(url_for('admin_login'))


@app.route('/admin/users/<int:uid>', methods=['GET', 'POST'])
def get_user_details(uid):
    if 'admin' in session:
        userstuff = model.getUserDetails(uid)
        userdetails = []
        for e in userstuff:
            userdetails.append(e)
        print("this is the lists", model.get_lists(userdetails[0]))
        userdetails.append(len(model.get_lists(userdetails[0])[0]))
        userdetails.append(len(model.get_lists(userdetails[0])[1]))
        return render_template('admin-userpage.html', userdetails=userdetails)
    return redirect(url_for('admin_login'))


@app.route('/admin/users/<int:uid>/delete', methods=['GET', 'POST'])
def delete_profile(uid):
    if 'admin' in session:
        model.delete_user(uid)
        return redirect(url_for('admin_users'))
    return redirect(url_for('admin_login'))


@app.route('/admin-logout')
def logout_admin():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))


@app.route('/deleteOwnProfile', methods=['GET', 'POST'])
def deleteOwnProfile():
    model.delete_user(model.getUserId(session['username']))
    return redirect(url_for('logout'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        status = "out"
        if 'username' in session:
            status = "in"
            userDetails = model.getUserDetails(
                model.getUserId(session['username']))
            # print(userDetails)
        return render_template('profile.html', userDetails=userDetails)
    else:
        username = session['username']
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        print(password)
        DBpassword = model.getUserDetails(
            model.getUserId(session['username']))[5]
        print(DBpassword)
        if password != DBpassword:
            userDetails = model.getUserDetails(
                model.getUserId(session['username']))
            return render_template('profile.html', message="Password is wrong!", userDetails=userDetails)
        status = model.updateSettings(username,
                                      firstname, lastname, password, email)
        userDetails = model.getUserDetails(
            model.getUserId(session['username']))
        return render_template('profile.html', message=status, userDetails=userDetails)

# @app.errorhandler(Exception)
# def handle_exception(e):
#     # pass through HTTP errors
#     if isinstance(e, HTTPException):
#         return e

#     # now you're handling non-HTTP exceptions only
#     return render_template("500_generic.html", e=e), 500


if __name__ == '__main__':
    app.run(port=7000, debug=True)
