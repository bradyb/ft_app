import cPickle as pickle
from playerTypes import fPlayer, tPlayer

def initTourney():

	attrMap = pickle.load(open( "attrMap.p", "rb" ))
	tourneyFile = open('tInfo.txt', 'r')
	numPlayers = int(tourneyFile.readline())
	tourneyFile.readline()	
	playerList = list()
	# the tournament file needs to be formatted correctly in order for this to work 
	for i in range(0, numPlayers):
		playerList.append(fPlayer(tourneyFile.readline().rstrip()))
		for j in range(0,7):
			line = tourneyFile.readline().rstrip()
			lineData = line.split(' ')
			if int(lineData[-1]) == 0: #if they are not a bench player
                            playerList[i].team.append(tPlayer(" ".join(lineData[1:-2]), lineData[0], attrMap[lineData[-2]]))
			else:
                            playerList[i].bench.append(tPlayer(" ".join(lineData[1:-2]), lineData[0], attrMap[lineData[-2]]))
		tourneyFile.readline()

	pickle.dump( playerList, open( "playerInfo.p", "wb" ) )

	
if __name__ == "__main__":
	initTourney()
