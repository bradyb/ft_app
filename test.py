from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def tester():
	return render_template('index.html')

@app.route('/ben')
def ben():
	players = ['Novak', 'Andy', 'Milos', 'Roger', 'Sam', 'Isner', 'Karlovic']
	return render_template('ben.html', players=players)


@app.route('/ben', methods=['GET', 'POST'])
def foo(x=None, y=None):
	players = ['Stanislas', 'Andy', 'Milos', 'Roger', 'Sam', 'Isner', 'Karlovic']
	return render_template('ben.html', players=players)


if __name__ == "__main__":
	app.run()