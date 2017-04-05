from flask import Flask, render_template, request, session, flash
import cPickle as pickle
import substitute as sub
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///users.db', echo=True)
app = Flask(__name__)


@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		users = pickle.load(open("playerInfo.p", "rb"))
		return render_template('index.html', users=users)

@app.route('/<username>')
def teamPage(username):
    if not session.get('logged_in'):
        return home()
	users = pickle.load(open("playerInfo.p", "rb"))
	for user in users:
		if username == user.name:
			return render_template('ben.html', user=user, teamName = username)
	return 'error'


@app.route('/<username>', methods=['GET', 'POST'])
def subPlayers(username):
    if not session.get('logged_in'):
        return home()
	playerName = request.form.get("bench",None)
	if playerName == None:
		users = pickle.load(open("playerInfo.p", "rb"))
		attrMap = pickle.load(open("attrMap.p", "rb"))
		playerName = request.form.get("subbed-player-name",None)
		playerAttr = request.form.get("subbed-player-attr",None)
		skipFlag = 0;

		for user in users:
			for player in user.team:

				if player.name == playerName and player.attribute == attrMap[playerAttr]:
					return render_template('ben.html', user=user, teamName = username)

		for user in users:
			if user.name == username:
				user.addPickUp(playerName,'m',attrMap[playerAttr])
				pickle.dump( users, open( "playerInfo.p", "wb" ) )
				return render_template('ben.html', user=user, teamName = username)
	else:
		user = sub.moveFromBench(playerName,username)
		return render_template('ben.html', user=user, teamName=username)
	return 'error'

@app.route("/login", methods=['POST'])
def login():
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
 
	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	result = query.first()
	if result:
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/test')
def test():
 
    POST_USERNAME = "python"
    POST_PASSWORD = "python"
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        return "Object found"
    else:
        return "Object not found " + POST_USERNAME + " " + POST_PASSWORD

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run()