import cPickle as pickle
from lxml import html
import requests
import operator
import datetime
from bs4 import BeautifulSoup
import urllib2
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

## maybe this should be broken up later ##


def getAllStats(name, order, statNames, soup, date):

	aces = int(soup.find('div', {'id': statNames[0] + order}).text)
	dfs = int(soup.find('div', {'id': statNames[1] + order}).text)
	winners = int(soup.find('div', {'id': statNames[2] + order}).text)
	ues = int(soup.find('div', {'id': statNames[3] + order}).text)
	returns = int(soup.find('div', {'id': statNames[5] + order}).text.split('(')[1].split('%')[0])
	defense = int(soup.find('div', {'id': statNames[4] + order}).text.split('(')[1].split('%')[0])

	bpc = 0
	bps = 0
	bpl = 0

	if order == '1':
		bpc = int(soup.find('div', {'id': statNames[6] + order}).text.split('/')[0])
		bps = int(soup.find('div', {'id': statNames[6] + '2'}).text.split('/')[1].split(' ')[0])
		bpl = int(soup.find('div', {'id': statNames[6] + '2'}).text.split('/')[0])

		
	else:
		bpc = int(soup.find('div', {'id': statNames[6] + order}).text.split('/')[0])
		bps = int(soup.find('div', {'id': statNames[6] + '1'}).text.split('/')[1].split(' ')[0])
		bpl = int(soup.find('div', {'id': statNames[6] + '1'}).text.split('/')[0])

	playerObj = players(name, date, aces, dfs, winners, ues, defense, returns, bps, bpc, bpl)

	session.add(playerObj)
	session.commit()

def updatePlayersTable(tourneyName):

	if todayDate == None:
		today = datetime.datetime.now()
		todayDate =  str(today.month) + '/' + str(today.day) + '/' + str(today.year)


	baseURL = "http://www.ausopen.com/en_AU/scores/completed_matches/day"

	urlStr = baseURL + tourneyDay + ".html"

	page = requests.get(urlStr)
	tree = html.fromstring(page.content)

	players = tree.xpath('//div[contains(@data-event, "MS") or contains(@data-event ,"WS")]/div[3]/div/div[1]/a/text()')

	links = tree.xpath('//div[contains(@data-event, "MS") or contains(@data-event ,"WS")]/div[4]/div/a/@href')

	wd = webdriver.Firefox()

	playerList = pickle.load(open( "playerList_" + tourneyName + ".p", "rb" ))

	engine = create_engine('sqlite:///testfrench2017.db', echo=True)

	Session = sessionmaker(bind=engine)
	session = Session()

	#player is of the form [playerName, alive]
	for player in playerList:

		#if the player is not alive then continue
		if player[1] == 0:
			continue

		#puts the name in the form F. Last
		shortName = player[0].split(' ')[0][0] + ". " + player[0].split(' ')[1]

		if shortName in players:

			playerIndex = players.index(shortName)

			if playerIndex % 2 == 0:
				orderBool = '1'
				orderName = 'One'
			else:
				orderBool = '2'
				orderName = 'Two'

			wd.get("https://www.ausopen.com" + links[playerIndex / 2])

			time.sleep(5)

			soup = BeautifulSoup(wd.page_source, "lxml")

			pointsEarned = getAllStats(player[0], orderBool, neededStats, soup, session)

			if "crticon winner" not in str(soup.find('div', {'class': 'teaminfo team' + orderName }).contents[2]):
				player[1] = 0

	session.commit()


def updateUsersTable(date):

	engine = create_engine('sqlite:///testfrench2017.db', echo=True)

	Session = sessionmaker(bind=engine)
	session = Session()

	user_query = session.query(User)

	for user in user_query:

		#points accumulated from players who've played today
		datePoints = 0

		team_query = session.query(Teams).filter_by(username = user.username, benched = 0)

		for player in team_query:

			playerObj = session.query(players).filter_by(name=player.player_name,asOfDate = date).first()


			##compute the points for this player and add it to datePoints

		user.totalPoints += datePoints

		session.commit()




	session.commit()



if __name__ == "__main__":
	date = raw_input('Enter the tournament day: ')
	updateLeague(date)





# def getPoints(name, attribute,	order, statNames, soup):
	

# 	if attribute == 1:
# 		#print soup.find('div', {'id': statNames[0] + order}).text
# 		#print statNames[0] + order
# 		aces = int(soup.find('div', {'id': statNames[0] + order}).text)
# 		dfs = int(soup.find('div', {'id': statNames[1] + order}).text)
# 		return 3 *(aces - dfs)

# 	elif attribute == 2:
# 		winners = int(soup.find('div', {'id': statNames[2] + order}).text)
# 		ues = int(soup.find('div', {'id': statNames[3] + order}).text)
# 		return 2 * winners - ues

# 	elif attribute == 3:
# 		#print soup.find('div', {'id': statNames[5] + order}).text
# 		return int(soup.find('div', {'id': statNames[5] + order}).text.split('(')[1].split('%')[0])

# 	elif attribute == 4:
# 		#print soup.find('div', {'id': statNames[4] + order}).text
# 		#print statNames[4] + order
# 		return int(soup.find('div', {'id': statNames[4] + order}).text.split('(')[1].split('%')[0])
		

# 	elif attribute == 5:
# 		if order == '1':
# 			bpc = int(soup.find('div', {'id': statNames[6] + order}).text.split('/')[0])
# 			bps = int(soup.find('div', {'id': statNames[6] + '2'}).text.split('/')[1].split(' ')[0])

# 			bpl = int(soup.find('div', {'id': statNames[6] + '2'}).text.split('/')[0])

# 			return 5*(bps - bpl + bpc) - 3 * bpl
# 		else:
# 			bpc = int(soup.find('div', {'id': statNames[6] + order}).text.split('/')[0])
# 			bps = int(soup.find('div', {'id': statNames[6] + '1'}).text.split('/')[1].split(' ')[0])

# 			bpl = int(soup.find('div', {'id': statNames[6] + '1'}).text.split('/')[0])

# 			return 5*(bps - bpl + bpc) - 3 * bpl



# def updateLeague(tourneyDay,todayDate = None):

# 	## TODO: tourney map of name to code ##
# 	## does the name change from year to year? It must, right? ##

# 	tourneyName = "australian-open"

# 	tourneyCode = "580"

# 	tourneyData = pickle.load(open( "playerInfo.p", "rb" ))

# 	statMap = pickle.load(open("statMap.p", "rb"))

# 	if todayDate == None:
# 		today = datetime.datetime.now()
# 		todayDate =  str(today.month) + '/' + str(today.day) + '/' + str(today.year)


# 	baseURL = "http://www.ausopen.com/en_AU/scores/completed_matches/day"

# 	urlStr = baseURL + tourneyDay + ".html"

# 	page = requests.get(urlStr)
# 	tree = html.fromstring(page.content)

	
# 	players = tree.xpath('//div[contains(@data-event, "MS") or contains(@data-event ,"WS")]/div[3]/div/div[1]/a/text()')


# 	links = tree.xpath('//div[contains(@data-event, "MS") or contains(@data-event ,"WS")]/div[4]/div/a/@href')

# 	pointsEarned = 0

# 	wd = webdriver.Firefox()


# 	neededStats = ["aces_p", "double_faults_p", "winners_p", 
# 		"unforced_errors_p", "second_srv_pts_won_p", "rec_pts_won_p",
# 			"brk_pts_won_p"]

	

# 	orderBool = '1'
# 	orderName = ''
# 	for user in tourneyData:

# 		for player in user.team:

			

# 			if player.alive != 1:
# 				player.history.append((todayDate, 'OUT'))
# 				continue

# 			shortName = player.name[0] + ". " + player.name.split(' ')[1]

# 			if shortName in players:

# 				playerIndex = players.index(shortName)

# 				if playerIndex % 2 == 0:
# 					orderBool = '1'
# 					orderName = 'One'
# 				else:
# 					orderBool = '2'
# 					orderName = 'Two'

# 				print playerIndex, len(links)

# 				wd.get("https://www.ausopen.com" + links[playerIndex / 2])

# 				time.sleep(5)

# 				soup = BeautifulSoup(wd.page_source, "lxml")

# 				pointsEarned = getPoints(player.name, player.attribute,	orderBool, neededStats, soup)

# 				#print str(soup.find('div', {'class': 'teaminfo team' + orderName }).contents[2])
# 				if "crticon winner" not in str(soup.find('div', {'class': 'teaminfo team' + orderName }).contents[2]):
# 					#print soup.find('div', {'class': 'teaminfo team' + orderName })
# 					player.alive = 0
# 					print player.name, ' here'



# 			# elif player.name in losers:

# 			# 	#orderBool = (player.name.split(' ')[1] < winners[losers.index(player.name)].split(' ')[1])
				
# 			# 	pointsEarned = getPoints(player.name, losers.index(player.name), baseURL, player.attribute, 
# 			# 					statMap, orderBool, links, neededStats)

# 			# 	player.alive = 0

# 			else:
# 				dailyStatus = "DNP"
# 				# if player.sex == 'f':
# 				# 	femaleResult = raw_input("Score for " + player.name + " " + player.attr  +  ": ")
# 				# 	if femaleResult.isdigit() or femaleResult[1:].isdigit:
# 				# 		pointsEarned = int(femaleResult)
# 				# 	elif femaleResult == "OUT":
# 				# 		player.alive = 0
# 				# 		dailyStatus = femaleResult

# 				player.history.append((todayDate, dailyStatus))
# 				continue

# 			player.points = player.points + pointsEarned

# 			player.history.append((todayDate, pointsEarned))

# 			user.total = user.total + pointsEarned

# 		for benchPlayer in user.bench:			

# 			if benchPlayer.alive != 1:
# 				benchPlayer.history.append((todayDate, 'OUT'))
# 				continue

# 			shortName = benchPlayer.name[0] + ". " + benchPlayer.name.split(' ')[1]

# 			if shortName in players:

# 				playerIndex = players.index(shortName)

# 				if playerIndex % 2 == 0:
# 					orderBool = '1'
# 					orderName = 'One'
# 				else:
# 					orderBool = '2'
# 					orderName = 'Two'

# 				wd.get("https://www.ausopen.com" + links[playerIndex / 2])

# 				time.sleep(5)

# 				soup = BeautifulSoup(wd.page_source, "lxml")

# 				pointsEarned = getPoints(benchPlayer.name, benchPlayer.attribute,	orderBool, neededStats,  soup)

# 				if "crticon winner" not in str(soup.find('div', {'class': 'teaminfo team' + orderName }).contents[2]):
# 					benchPlayer.alive = 0
# 					print benchPlayer.name, ' here'

# 			else:
# 				dailyStatus = "DNP"
# 				# if player.sex == 'f':
# 				# 	femaleResult = raw_input("Score for " + player.name + " " + player.attr  +  ": ")
# 				# 	if femaleResult.isdigit() or femaleResult[1:].isdigit:
# 				# 		pointsEarned = int(femaleResult)
# 				# 	elif femaleResult == "OUT":
# 				# 		player.alive = 0
# 				# 		dailyStatus = femaleResult

# 				benchPlayer.history.append((todayDate, dailyStatus))
# 				continue

# 			benchPlayer.history.append((todayDate,'(' + str(pointsEarned) + ')'))

# 	tourneyData.sort(key=lambda fPlayer: -1 * fPlayer.total)



# 	pickle.dump( tourneyData, open( "playerInfo.p", "wb" ) )
# 	wd.quit()