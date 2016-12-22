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
		attrMap = pickle.load(open("attrMap.p", "rb"))
		playerName = request.form.get("subbed-player-name",None)
		playerAttr = request.form.get("subbed-player-attr",None)
		print "here"
		skipFlag = 0;

		for user in users:
			for player in user.team:

				if player.name == playerName and player.attribute == attrMap[playerAttr]:
					return render_template('ben.html', user=user) 

		for user in users:
			if user.name == "Ben":
				user.addPickUp(playerName,'m',attrMap[playerAttr])
				pickle.dump( users, open( "playerInfo.p", "wb" ) )
				return render_template('ben.html', user=user)
	else:
		user = sub.moveFromBench(playerName,"Ben")
		return render_template('ben.html', user=user)


if __name__ == "__main__":
	app.run()