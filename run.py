from flask import Flask, render_template, request, session
import cPickle as pickle
import substitute as sub
import os
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
        return render_template('login.html')
	users = pickle.load(open("playerInfo.p", "rb"))
	for user in users:
		if username == user.name:
			return render_template('ben.html', user=user, teamName = username)
	return 'error'


@app.route('/<username>', methods=['GET', 'POST'])
def subPlayers(username):
    if not session.get('logged_in'):
        return render_template('login.html')
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


if __name__ == "__main__":
	app.run()