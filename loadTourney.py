from players import fPlayer
from players import tPlayer


def loadTourney():

	return players.pickle.load(open( "playerInfo.p", "rb" ))


if __name__ == "__main__":
	loadTourney()