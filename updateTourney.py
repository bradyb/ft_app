import cPickle as pickle
from lxml import html
import requests
import operator
import datetime


## maybe this should be broken up later ##

def getPoints(playerName, index, baseURL, playerAttr, statMap, win, links, neededStats):

	winnersStats = []
	losersStats = []
	#linkIndex = sideList.index(playerName)
	matchStatsURL = baseURL + links[index]

	statsPage = requests.get(matchStatsURL)
	tree1 = html.fromstring(statsPage.content)

	stats = tree1.xpath('//*[@id="matchStatsData"]/text()')
	name = tree1.xpath('//*[@id="modalScoresMatchStatsTable"]/div[1]/div[1]/div[2]/a/span[2]/text()')

	if playerName.split(' ')[1] in name[0]:
		win = 1;
	else: 
		win = 0

	statsList = stats[0].split('\r\n')

	stats = -1

	counter = 0


	for item in statsList:

		if "\"setNum\": 1," in item:
			break
		#print item
		#print neededStats[counter]
		if neededStats[counter] in item:

			itemList = item.split(' ')
			stats = int(itemList[len(itemList) - 1][:-1])

			if len(winnersStats) < len(neededStats):
				winnersStats.append(stats)
			else:
				losersStats.append(stats)
			
			counter = (counter + 1) % len(neededStats)


	if playerAttr == 1:
		if win:
			return 3 * (winnersStats[0] - winnersStats[1])
		else:
			return 3 * (losersStats[0] - losersStats[1])

	elif playerAttr == 2:
		numWinners = int(raw_input("Number Winners for " + playerName + "?"))
		numUE = int(raw_input("Number of Unforced Errors?"))
		return 2 * numWinners - numUE

	elif playerAttr == 3:
		if win:
			return winnersStats[5]
		else:
			return losersStats[5]

	elif playerAttr == 4:
		if win:
			return winnersStats[2]
		else:
			return losersStats[2]


	elif playerAttr == 5:
		if win:
			return 5 * (losersStats[4] - losersStats[3] + winnersStats[3]) - 3 * (winnersStats[4] - winnersStats[3])
		else:
			return 5 * (winnersStats[4] - winnersStats[3] + losersStats[3]) - 3 * (losersStats[4] - losersStats[3])



def updateLeague():

	## TODO: tourney map of name to code ##
	## does the name change from year to year? It must, right? ##

	tourneyName = "brisbane"

	tourneyCode = "339"

	tourneyData = pickle.load(open( "playerInfo.p", "rb" ))

	statMap = pickle.load(open("statMap.p", "rb"))

	today = datetime.datetime.now()

	todayDate =  str(today.month) + '/' + str(today.day) + '/' + str(today.year)

	print todayDate

	baseURL = "http://www.atpworldtour.com"

	urlStr = "http://www.atpworldtour.com/en/scores/current/" + tourneyName + '/' + tourneyCode + '/' + 'results?matchdate=' + todayDate

	page = requests.get(urlStr)
	tree = html.fromstring(page.content)

	winners = tree.xpath('//*[@id="scoresResultsContent"]/div/table/tbody/tr/td[3]/a/text()')

	print winners

	losers = tree.xpath('//*[@id="scoresResultsContent"]/div/table/tbody/tr/td[7]/a/text()')

	print losers


	links = tree.xpath('//*[@id="scoresResultsContent"]/div/table/tbody/tr/td[8]/a/@href')

	pointsEarned = 0

	neededStats = ["Aces", "DoubleFaults", "SecondServePointsWonPercentage", 
						"BreakPointsSavedDividend", "BreakPointsSavedDivisor", "TotalReturnPointsWonPercentage"]

	orderBool = 0
	for user in tourneyData:

		for player in user.team:

			

			if player.alive != 1:
				player.history.append((todayDate, 'OUT'))
				continue

			if player.name in winners:

				#orderBool = (player.name.split(' ')[1] < losers[winners.index(player.name)].split(' ')[1])

				pointsEarned = getPoints(player.name, winners.index(player.name), baseURL, player.attribute, 
								statMap, orderBool, links, neededStats)

			elif player.name in losers:

				#orderBool = (player.name.split(' ')[1] < winners[losers.index(player.name)].split(' ')[1])
				
				pointsEarned = getPoints(player.name, losers.index(player.name), baseURL, player.attribute, 
								statMap, orderBool, links, neededStats)

				player.alive = 0

			else:
				player.history.append((todayDate, 'DNP'))
				continue

			player.points = player.points + pointsEarned

			player.history.append((todayDate, pointsEarned))

			user.total = user.total + pointsEarned

		for benchPlayer in user.bench:			

			if benchPlayer.alive != 1:
				benchPlayer.historiy.append((todayDate, 'OUT'))
				continue

			if benchPlayer.name in winners:

				orderBool = (benchPlayer.name.split(' ')[1] < losers[winners.index(benchPlayer.name)].split(' ')[1])

				pointsEarned = getPoints(benchPlayer.name, winners.index(benchPlayer.name), baseURL, benchPlayer.attribute, 
								statMap, orderBool, links, neededStats)

			elif benchPlayer.name in losers:
				
				orderBool = (benchPlayer.name.split(' ')[1] < winners[losers.index(benchPlayer.name)].split(' ')[1])

				pointsEarned = getPoints(benchPlayer.name, losers.index(benchPlayer.name), baseURL, benchPlayer.attribute, 
								statMap, orderBool, links, neededStats)

				benchPlayer.alive = 0

			else:
				benchPlayer.history.append((todayDate, 'DNP'))
				continue

			benchPlayer.history.append((todayDate,'(' + str(pointsEarned) + ')'))

	sorted(tourneyData, key=lambda player: player.total)

	pickle.dump( tourneyData, open( "playerInfo.p", "wb" ) )

if __name__ == "__main__":
	updateLeague()
	
