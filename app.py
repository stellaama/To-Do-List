from flask import Flask, render_template, json, request, session, redirect
import os, requests

app = Flask(__name__)
app.secret_key= 'webdevissoC00l'

@app.route('/', methods=['GET','POST'])
def home():
	if 'username' in session:
		return redirect('/loggedIn')
	else:
		print("not in session")

	if request.method == 'POST':
		submit_button = request.form['submit']
		username = request.form['username']
		if (submit_button == 'Register'):
			r = requests.post('https://hunter-todo-api.herokuapp.com/user', json={'username': username})
			print(r.json())
			print(r.url)
			print(r)
			if r.status_code == 409:
				return render_template('home.html', text = "<p>That user already exists.<p>")
		new_login = requests.post('https://hunter-todo-api.herokuapp.com/auth', json={'username': username})
		print (new_login.json())
		print(new_login.status_code)
		if new_login.status_code == 400:
			return render_template('home.html', text = "<p>That user doesn't exist.<p>")
			print(new_login.status_code)
		else:
			#storing the token
			session['username'] = new_login.json()['token']
			session['name'] = username
			return redirect('/loggedIn')
	return render_template('home.html', text = "<p>Welcome! Sign In or Register!<p>")

@app.route('/loggedIn', methods=['GET','POST'])
def loggedIn():
	if 'username' in session:
		#print(session.get('username', None));
		if request.method == 'POST':
			submit_button = request.form['submit']
			new_task = request.form['new_task']
			if (submit_button == 'Submit'):
				r = requests.post('https://hunter-todo-api.herokuapp.com/todo-item', cookies={'sillyauth': session.get('username', None)}, json={"content":new_task})
		list_of_tasks=requests.get('https://hunter-todo-api.herokuapp.com/todo-item', cookies={'sillyauth': session.get('username', None)})
		return render_template('loggedIn.html', Name= session['name'], tasks=list_of_tasks.json())
	else:
		return redirect('/')


@app.route('/update_done/<id>', methods=['GET'])
def update_done(id):
	if 'username' in session:
		r = requests.put('https://hunter-todo-api.herokuapp.com/todo-item/'+id, cookies={'sillyauth': session.get('username', None)}, json={"completed": True})
		print(r.json())
		return redirect('/loggedIn')
	else:
		return redirect('/')

@app.route('/update_notdone/<id>', methods=['GET'])
def update_notdone(id):
	if 'username' in session:
		r = requests.put('https://hunter-todo-api.herokuapp.com/todo-item/'+id, cookies={'sillyauth': session.get('username', None)}, json={"completed": False})
		print(r.json())
		return redirect('/loggedIn')
	else:
		return redirect('/')

@app.route('/delete_task/<id>', methods=['GET'])
def delete_task(id):
	if 'username' in session:
		r = requests.delete('https://hunter-todo-api.herokuapp.com/todo-item/'+id, cookies={'sillyauth': session.get('username', None)})
		print(r.text)
		return redirect('/loggedIn')
	else:
		return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('name', None)
   return redirect('/')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)
