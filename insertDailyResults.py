import cPickle as pickle
from playerTypes import fPlayer, tPlayer
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

def insertDailyResults():

	dailyData = pickle.load(open( "dailyInfo.p", "rb" ))

	date = dailyData.date

	for player in dailyData.activeList:

		# insert the daily info into the players list
		# make sure you update the active flag





if __name__ == "__main__":
	insertDailyResults()