from flask import Flask, render_template, request, session, redirect, url_for, g
import model


app = Flask(__name__)
app.secret_key = 'jumpjacks'

username = ''
user = model.check_users()

@app.route('/', methods = ['GET'])
def home():
	if 'username' in session:
		g.user = session['username']
		return render_template('dashboard.html', message = model.get_lists(g.user) )
		#message = '<table><tr><td>First Row</td></tr><tr><tr><td>First Row</td></tr><tr><tr><td>First Row</td></tr></table>')
		# add the lists to show here "message ="
	return render_template('homepage.html', message = "Log in to the page or sign up!")

@app.route('/terms', methods = ['GET'])
def terms():
	return render_template('terms.html')

@app.route('/privacy', methods = ['GET'])
def privacy():
	return render_template('privacy.html')

@app.route('/about', methods = ['GET'])
def about():
	return render_template('about.html')

@app.route('/dashboard', methods = ['GET'])
def dashboard():
	return render_template('dashboard.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		session.pop('username', None)
		areyouuser = request.form['username']
		pwd = model.check_pw(areyouuser)
		if request.form['password'] == pwd:
			session['username'] = request.form['username']
			return redirect(url_for('home'))
	return render_template('index.html')

@app.before_request
def before_request():
	g.username = None
	if username in session:
		g.username = session['username']


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if request.method == 'GET':
		message = 'Please sign up!'
		return render_template('signup.html')
	else:
		username = request.form["username"]
		firstname = request.form["firstname"]
		lastname = request.form["lastname"]
		password = request.form["password"]
		message = model.signup(username,firstname, lastname, password)
		return render_template('signup.html', message = message)

@app.route('/getsession')
def getsession():
	if 'username' in session:
		return session['username']
	return redirect(url_for('login'))

@app.route('/createlist', methods=['GET','POST'])
def createlist():
	if request.method == 'POST':
		list = request.form['list']
		g.user = session['username']
		userID = model.getUserId(g.user)
		model.add_list(userID,list)
		return render_template('dashboard.html', message = model.get_lists(g.user))
	else:
		return render_template('createlist.html')

@app.route('/<int:tid>/delete',methods=['GET','POST'])
def deletetask(tid):
	model.delete_task(tid)
	# g.user = session['username']
	return redirect(url_for('home'))

@app.route('/<int:lid>/deletelist',methods=['GET','POST'])
def deletelist(lid):
	model.delete_list(lid)
	# g.user = session['username']
	return redirect(url_for('home'))

@app.route('/<int:lid>/add',methods=['GET','POST'])
def createtask(lid):
	model.add_task(lid,'new task')
	# g.user = session['username']
	return redirect(url_for('home'))

@app.route('/<int:tid>/updatetask', methods=['GET','POST'])
def update_task(tid):
	if request.method == 'POST':
		task = request.form['task']
		g.user = session['username']
		userID = model.getUserId(g.user)
		model.update_task(tid,task)
		return redirect(url_for('home'))
	else:
		tasktext='this is the text'
		print(model.get_tasktext(tid))
		return render_template('modifytask.html', text = model.get_tasktext(tid))

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(port = 7000, debug = True)