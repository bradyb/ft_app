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
		return render_template('index.html', users=users)
	else:
		user = sub.moveFromBench(playerName,"Ben")
		return render_template('ben.html', user=user)


if __name__ == "__main__":
	app.run()