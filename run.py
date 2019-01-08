from flask import Flask, render_template, request, session, flash, redirect, url_for
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
def teamPage(username, location=None):

	if not session.get('logged_in'):
		return redirect(url_for('home'))
	users = pickle.load(open("playerInfo.p", "rb"))

	for user in users:
		if username == user.name:
			#if (location !=  None):
			#	return render_template('ben.html#'+location, user=user, teamName = username, sessionUser=session.get('username'))
			return render_template('ben.html', user=user, teamName = username, sessionUser=session.get('username'))
	return 'error'


@app.route('/<username>/bench', methods=['POST'])
def benchPlayers(username):
	if not session.get('logged_in'):
		return home()
	playerName = request.form.get("bench",None)
	if playerName == None:
		return 'error'
	
	user = sub.moveFromBench(playerName,username)
	return redirect(url_for('teamPage', username=username) + "#scores")
	#return teamPage(username)
	

@app.route('/<username>/sub', methods=['POST'])
def subPlayers(username):
	if not session.get('logged_in'):
		return home()

	users = pickle.load(open("playerInfo.p", "rb"))
	attrMap = pickle.load(open("attrMap.p", "rb"))
	playerName = request.form.get("subbed-player-name",None)
	playerAttr = request.form.get("subbed-player-attr",None)

	for user in users:
		for player in user.team:
			if player.name == playerName and player.attribute == attrMap[playerAttr]:
				return redirect(url_for('teamPage', username=username) + "#scores")

	for user in users:
		if user.name == username:
			user.addPickUp(playerName,'m',attrMap[playerAttr])
			pickle.dump( users, open( "playerInfo.p", "wb" ) )
			return redirect(url_for('teamPage', username=username)+ "#scores")

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
		session['username'] = POST_USERNAME
		print session['username']
	else:
		flash('wrong password!')
	return redirect(url_for('home'))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return home()

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run()