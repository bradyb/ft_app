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

def updatePlayersTable(tourneyDay,tourneyName = None):

	today = datetime.datetime.now()
	todayDate =  str(today.month) + '/' + str(today.day) + '/' + str(today.year)

	#Australian Open
	#baseURL = "http://www.ausopen.com/en_AU/scores/completed_matches/day"
	
	#French Open
	baseURL = "http://www.rolandgarros.com/en_FR/scores/completed_matches/day"

	urlStr = baseURL + tourneyDay + ".html"

	page = requests.get(urlStr)
	tree = html.fromstring(page.content)

	#Australian Open
	#players = tree.xpath('//div[contains(@data-event, "MS") or contains(@data-event ,"WS")]/div[3]/div/div[1]/a/text()')

	#French Open
	players = tree.xpath('//div[contains(@data-event, "MS") or contains(@data-event ,"WS")]/div/div[2]/div[1]/div/div[1]/a/text()')

	#Australian Open
	#links = tree.xpath('//div[contains(@data-event, "MS") or contains(@data-event ,"WS")]/div[4]/div/a/@href')

	#French Open
	links = tree.xpath('//div[contains(@data-event, "MS") or contains(@data-event ,"WS")]/div/div[2]/div[3]/div/a/@href')

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

			playerStats = session.query(players).filter_by(name=player.player_name,asOfDate = date).first()

			#serve
			if (player.attribute == 1):
				datePoints += 3*(playerStats.aces - playerStats.double_faults)
			#power
			elif (player.attribute == 2):
				datePoints += 2*playerStats.winners - playerStats.unforced_errors
			#return
			elif (player.attribute == 3):
				datePoints += playerStats.receive_percent
			#defense
			elif (player.attribute == 4):
				datePoints += playerStats.second_srv_percent
			#mind
			elif (player.attribute == 5):
				datePoints += 5*(playerStats.bps - playerStats.bpl + playerStats.bpc) - 3 * playerStats.bpl


		user.totalPoints += datePoints

		session.commit()

	session.commit()



if __name__ == "__main__":
	date = raw_input('Enter the tournament day: ')
	updatePlayersTable(date)

