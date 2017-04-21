import cPickle as pickle
from playerTypes import fPlayer, tPlayer
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

def initTourney():

	tourneyName = raw_data("Tourney name: ")

	# maps attribute names to their corresponding integer
	# are there enums in python?
	attrMap = pickle.load(open( "attrMap.p", "rb" ))

	# contains the teams for each player from the draft, trailing bit is True
	# if they are a bench player
	tourneyFile = open('tInfo.txt', 'r')

	numPlayers = int(tourneyFile.readline())

	tourneyFile.readline()	

	#playerList = list()

	# the tournament file needs to be formatted correctly in order for this to work 
	# for i in range(0, numPlayers):

	# 	playerList.append(fPlayer(tourneyFile.readline().rstrip()))

	# 	for j in range(0,7):

	# 		line = tourneyFile.readline().rstrip()
	# 		lineData = line.split(' ')
	# 		if int(lineData[4]) == 0: #if they are not a bench player
	# 			playerList[i].team.append(tPlayer(lineData[1] + " " + lineData[2], lineData[0], attrMap[lineData[3]]))
	# 		else:
	# 			playerList[i].bench.append(tPlayer(lineData[1] + " " + lineData[2], lineData[0], attrMap[lineData[3]]))

	# 	tourneyFile.readline()

	#from Aussie2017, would dump into pickled file, and that would be the state of the tourney
	#pickle.dump( playerList, open( "playerInfo.p", "wb" ) )

	engine = create_engine('sqlite:///testfrench2017.db', echo=True)
 
	# create a Session
	Session = sessionmaker(bind=engine)
	session = Session()

	teamsList = list()
	playerList = list()

	for i in range(0, numPlayers):

		username = tourneyFile.readline().rstrip()

		for j in range(0,7):

			curLine = tourneyFile.readline().rstrip()

			lineData = curLine.split(' ')

			teamsList.append(Teams(username, lineData[1] + " " + lineData[2], attrMap[lineData[3]] , int(lineData[4])))

			if (lineData[1] + " " + lineData[2]) not in playerList:
				
				playerList.append([lineData[1] + " " + lineData[2], 1])

	
	session.add_all(teamsList)

	# commit the record the database
	session.commit()
 
	session.commit()

	pickle.dump( playerList, open( "playerList_" + tourneyName + ".p", "wb" ) )


if __name__ == "__main__":
	initTourney()