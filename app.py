from flask import Flask, render_template, request, session, redirect, url_for, g
import model


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
            #countLogs = model.getLogs()
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
        password = request.form["password"]
        message = model.signup(username, firstname, lastname, password)
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
        g.user = session['username']
        userID = model.getUserId(g.user)
        model.update_task(tid, task)
        return redirect(url_for('home'))
    else:
        tasktext = 'this is the text'
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
        countLogs = model.getLogs()
        countLogs24h = model.getLastLogs()
        countLists = model.getLists()
        countLists24h = model.getLastLists()
        print(countLogs)
        return render_template('admin-dashboard.html', countLogs=countLogs, countLogs24h=countLogs24h, countLists=countLists, countLists24h=countLists24h)
    return redirect(url_for('admin_login'))


@app.route('/admin-logout')
def logout_admin():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(port=7000, debug=True)
