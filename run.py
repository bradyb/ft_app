from flask import Flask, render_template, request
import cPickle as pickle
import substitute as sub
app = Flask(__name__)

@app.route('/')
def home():
	users = pickle.load(open("playerInfo.p", "rb")) 
	return render_template('index.html', users=users)

@app.route('/Ben')
def Ben():
	users = pickle.load(open("playerInfo.p", "rb"))
	for user in users:
		if "Ben" == user.name:
			return render_template('ben.html', user=user)


@app.route('/Ben', methods=['GET', 'POST'])
def subPlayers():
	playerName = request.form.get("bench",None)
	if playerName == None:
		users = pickle.load(open("playerInfo.p", "rb"))
		statMap = pickle.load(open("statMap.p", "rb"))
		playerName = request.form.get("subbed-player-name",None)
		playerAttr = request.form.get("subbed-player-attr",None)

		for user in users:
			for player in user.team:

				if player.name == playerName and player.attribute = statMap[playerAttr]:
					return render_template('ben.html', users=users) 

		for user in users:
			if user.name == "Ben":
				user.addPickUp(playerName,'m',statMap[playerAttr])
				return render_template('ben.html', users=users)
	else:
		user = sub.moveFromBench(playerName,"Ben")
		return render_template('ben.html', user=user)


if __name__ == "__main__":
	app.run()