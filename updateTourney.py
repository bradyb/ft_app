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


def getPoints(name, attribute,	order, statNames, soup):
	

	if attribute == 1:
		#print soup.find('div', {'id': statNames[0] + order}).text
		#print statNames[0] + order
		aces = int(soup.find('div', {'id': statNames[0] + order}).text)
		dfs = int(soup.find('div', {'id': statNames[1] + order}).text)
		return 3 *(aces - dfs)

	elif attribute == 2:
		winners = int(soup.find('div', {'id': statNames[2] + order}).text)
		ues = int(soup.find('div', {'id': statNames[3] + order}).text)
		return 2 * winners - ues

	elif attribute == 3:
		#print soup.find('div', {'id': statNames[5] + order}).text
		return int(soup.find('div', {'id': statNames[5] + order}).text.split('(')[1].split('%')[0])

	elif attribute == 4:
		#print soup.find('div', {'id': statNames[4] + order}).text
		#print statNames[4] + order
		return int(soup.find('div', {'id': statNames[4] + order}).text.split('(')[1].split('%')[0])
		

	elif attribute == 5:
		if order == '1':
			bpc = int(soup.find('div', {'id': statNames[6] + order}).text.split('/')[0])
			bps = int(soup.find('div', {'id': statNames[6] + '2'}).text.split('/')[1].split(' ')[0])

			bpl = int(soup.find('div', {'id': statNames[6] + '2'}).text.split('/')[0])

			return 5*(bps - bpl + bpc) - 3 * bpl
		else:
			bpc = int(soup.find('div', {'id': statNames[6] + order}).text.split('/')[0])
			bps = int(soup.find('div', {'id': statNames[6] + '1'}).text.split('/')[1].split(' ')[0])

			bpl = int(soup.find('div', {'id': statNames[6] + '1'}).text.split('/')[0])

			return 5*(bps - bpl + bpc) - 3 * bpl



def updateLeague(tourneyDay,todayDate = None):

	## TODO: tourney map of name to code ##
	## does the name change from year to year? It must, right? ##

	tourneyName = "australian-open"

	tourneyCode = "580"

	tourneyData = pickle.load(open( "playerInfo.p", "rb" ))

	statMap = pickle.load(open("statMap.p", "rb"))

	if todayDate == None:
		today = datetime.datetime.now()
		todayDate =  str(today.month) + '/' + str(today.day) + '/' + str(today.year)

	#baseURL = "http://www.atpworldtour.com"

	baseURL = "http://www.ausopen.com/en_AU/scores/completed_matches/day"

	#urlStr = "http://www.atpworldtour.com/en/scores/current/" + tourneyName + '/' + tourneyCode + '/' + 'results?matchdate=' + todayDate

	urlStr = baseURL + tourneyDay + ".html"

	page = requests.get(urlStr)
	tree = html.fromstring(page.content)

	
	players = tree.xpath('//*[@class="name singles"]/a/text()')


	links = tree.xpath('//div[contains(@data-event, "MS") or contains(@data-event ,"WS")]/div[4]/div/a/@href')

	pointsEarned = 0

	wd = webdriver.Firefox()


	neededStats = ["aces_p", "double_faults_p", "winners_p", 
		"unforced_errors_p", "second_srv_pts_won_p", "rec_pts_won_p",
			"brk_pts_won_p"]

	

	orderBool = '1'
	orderName = ''
	for user in tourneyData:

		for player in user.team:

			

			if player.alive != 1:
				player.history.append((todayDate, 'OUT'))
				continue

			shortName = player.name[0] + ". " + player.name.split(' ')[1]

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

				pointsEarned = getPoints(player.name, player.attribute,	orderBool, neededStats, soup)

				#print str(soup.find('div', {'class': 'teaminfo team' + orderName }).contents[2])
				if "crticon winner" not in str(soup.find('div', {'class': 'teaminfo team' + orderName }).contents[2]):
					#print soup.find('div', {'class': 'teaminfo team' + orderName })
					player.alive = 0
					print player.name, ' here'
			else:
				dailyStatus = "DNP"

				player.history.append((todayDate, dailyStatus))
				continue

			player.points = player.points + pointsEarned

			player.history.append((todayDate, pointsEarned))

			user.total = user.total + pointsEarned

		for benchPlayer in user.bench:			

			if benchPlayer.alive != 1:
				benchPlayer.history.append((todayDate, 'OUT'))
				continue

			shortName = benchPlayer.name[0] + ". " + benchPlayer.name.split(' ')[1]

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

				pointsEarned = getPoints(benchPlayer.name, benchPlayer.attribute,	orderBool, neededStats,  soup)

				if "crticon winner" not in str(soup.find('div', {'class': 'teaminfo team' + orderName }).contents[2]):
					benchPlayer.alive = 0
					print benchPlayer.name, ' here'

			else:
				dailyStatus = "DNP"
				# if player.sex == 'f':
				# 	femaleResult = raw_input("Score for " + player.name + " " + player.attr  +  ": ")
				# 	if femaleResult.isdigit() or femaleResult[1:].isdigit:
				# 		pointsEarned = int(femaleResult)
				# 	elif femaleResult == "OUT":
				# 		player.alive = 0
				# 		dailyStatus = femaleResult

				benchPlayer.history.append((todayDate, dailyStatus))
				continue

			benchPlayer.history.append((todayDate,'(' + str(pointsEarned) + ')'))

	tourneyData.sort(key=lambda fPlayer: -1 * fPlayer.total)

	

	pickle.dump( tourneyData, open( "playerInfo.p", "wb" ) )
	wd.quit()

if __name__ == "__main__":
	date = raw_input('Enter the tournament day: ')
	updateLeague(date)

