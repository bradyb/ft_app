import cPickle as pickle
from playerTypes import fPlayer, tPlayer
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tableBuilder import *


def checkContentsOfTable(tableName):

		engine = create_engine('sqlite:///testfrench2017.db', echo=True)
 
		# create a Session
		Session = sessionmaker(bind=engine)
		session = Session()

		query = session.query(User)

		for result in query:
			print result.username, result.totalPoints



if __name__ == "__main__":
	tableName = raw_input("Name of table to inspect: ")
	checkContentsOfTable(tableName)








