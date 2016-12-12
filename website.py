import cPickle as pickle


def writeToWeb():
	index = open("/home/bradyb/Projects/bradyb.github.io/projects/tennis/index.html", 'w')

	beginning = """<!DOCTYPE html> 
	<html>
	<head>
		<title>Fantasy Tennis</title>
		<!-- link to main stylesheet -->
		<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/tennis.css\">
	</head>

	<body>
		<header id=\"header\">
				 <h1>Fantasy Tennis</h1>
		</header>
		 <div style = \"text-align: center;\">
		  <div style=\"display: inline-block; text-align: left; max-width: 60%;\">
		<table style=\"width:100%\">
		<col align="left">
		<col align="left">
		<col align="right">
  		<tr>
    		<th>Player</th>
   			<th>Serve</th> 
    		<th>Power</th>
    		<th>Return</th>
    		<th>Defense</th>
    		<th>Mind</th>
    		<th>Total</th>
  		</tr> """

  	tourneyData = pickle.load(open("playerInfo.p", "rb")) 

	data = ""

	for user in tourneyData:

		data = data + "<tr><td><a href=\"https://bradyb.github.io/projects/tennis/" + user.name.lower() + "/\">" + user.name + "</a></td>"

		sorted(user.team, key=lambda tPlayer: tPlayer.attribute)

		for player in user.team:

			if player.attribute == 6:
				continue

			data = data + "<td>" + player.name + "</td>"

		data = data + "</tr><tr><td>  </td>"

		pointSum = 0

		for player in user.team:

			if player.attribute == 6:
				continue

			pointSum = pointSum + player.points

			data = data + "<td>" + str(player.points) + "</td>"

		data = data + "<td>" + str(pointSum) + "</td>"

		data = data + "</tr>"


	end = """		
		</table>
		<footer>
    		<ul>
        		<li><a href="mailto:ben.brady1224@gmail.com">email</a></li>
        		<li><a href="https://github.com/bradyb">github.com/bradyb</a></li>
			</ul>
		</footer>
		</div>
		</div>
	</body>
	</html> """

	text = beginning + data + end

	index.write(text)

def setStats(user):

	beginning = """<!DOCTYPE html> 
	<html>
	<head>
		<title>""" + "Team | " + user.name + """</title>
		<!-- link to main stylesheet -->
		<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/team.css\">
	</head>

	<body>
		<header id=\"header\">
				 <h1>""" + user.name + "'s Team" + """</h1>
		</header>
		 <div style = \"text-align: center;\">
		  <div style=\"display: inline-block; text-align: left; max-width: 60%;\">
		<table style=\"width:100%\">
		<col align="left">
		<col align="left">
		<col align="right">
  		<tr>
  			<th>Date</th>
    		<th>Serve</th> 
    		<th>Power</th>
    		<th>Return</th>
    		<th>Defense</th>
    		<th>Mind</th>
    		<th>Bench</th>
    		<th>Bench</th>
    		<th>Bench<th>
    	</tr> """

	data = beginning
	user.team.sort(key=lambda tPlayer: tPlayer.attribute)


	#setting up the top player row
	data = data + "<tr><td>-</td>"



	daysOfPlay = len(user.team[0].history)

	for player in user.team:

		data = data + "<td>" + player.name + "</td>"

	for player in user.bench:

		data = data + "<td>" + player.name + "</td>"

	data = data + "</tr>"


	#printing their daily stats
	for day in range(0, daysOfPlay):

		data = data + "<tr>"

		dateFlag = 1
		
		#iterate over players and index into the 'day' of their history
		for player in user.team:

			if dateFlag:
				#subs have dummy dates before they are entered so this corrects it
				for bPlayer in user.bench:
					if bPlayer.history[day][0] != "0/0/0":
						data = data + "<td>" + bPlayer.history[day][0] + "</td>"
						break
				dateFlag = 0

			data = data + "<td>" + str(player.history[day][1]) + "</td>"

		for player in user.bench:

			data = data + "<td>" + str(player.history[day][1]) + "</td>"

		data = data + "</tr>"

	data = data + "<tr><td></td>"

	for player in user.team:
		data = data + "<td></td>"

	for player in user.bench:
		data = data + "<td><label for=\"bench\">Add to linuep</label> <input type=\"checkbox\" name=\"bench\" id=\"bench\" value=\"lineup\"></td>"

	data = data + "</tr>"

	return data


def writeToTeam():

	tourneyData = pickle.load(open("playerInfo.p", "rb")) 

	for user in tourneyData:
		
		index = open("/home/bradyb/Projects/bradyb.github.io/projects/tennis/" + user.name.lower() + "/index.html", 'w')

		front = setStats(user)

		text = front + """		
							</table>
							<footer>
    							<ul>
        							<li><a href="mailto:ben.brady1224@gmail.com">email</a></li>
        							<li><a href="https://github.com/bradyb">github.com/bradyb</a></li>
								</ul>
							</footer>
							</div>
							</div>
							</body>
							</html> """
  	
  		index.write(text)

		index.close()


if __name__ == "__main__":
	writeToWeb()
	writeToTeam()
	