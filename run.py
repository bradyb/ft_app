from flask import Flask, render_template, request
import cPickle as pickle
import substitute as sub
app = Flask(__name__)

@app.route('/')
def home():
	users = pickle.load(open("playerInfo.p", "rb")) 
	return render_template('index.html', users=users)

@app.route('/history/<tournament>')
def DisplayTournament(tournament):
	tournament_str = '_'.join(tournament.split('-'))
	file_name = '_'.join(tournament.split('-')) + '.p'
	tournament_data = pickle.load(open(file_name, "rb"))
	return render_template('history/index.html', 
							users=tournament_data,
							tournament=tournament_str,
							tournament_display=' '.join(tournament.split('-')))

@app.route('/history/<tournament>/<username>')
def DisplayTournamentUser(tournament, username):
	file_name = '_'.join(tournament.split('-')) + '.p'
	users = pickle.load(open(file_name, "rb"))
	for user in users:
		if username == user.name:
			return render_template('history/team.html', 
									user=user, 
									teamName = username,
									tournament=tournament)
	return 'error'

@app.route('/<username>')
def teamPage(username):
	users = pickle.load(open("playerInfo.p", "rb"))
	for user in users:
		if username == user.name:
			return render_template('team.html', user=user, teamName = username)
	return 'error'


@app.route('/<username>', methods=['GET', 'POST'])
def subPlayers(username):
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
					return render_template('team.html', user=user, teamName = username) 

		for user in users:
			if user.name == username:
				user.addPickUp(playerName,'m',attrMap[playerAttr])
				pickle.dump( users, open( "playerInfo.p", "wb" ) )
				return render_template('team.html', user=user, teamName = username)
	else:
		user = sub.moveFromBench(playerName,username)
		return render_template('team.html', user=user, teamName=username)
	return 'error'


if __name__ == "__main__":
	app.run()