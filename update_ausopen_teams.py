import ausopen_query

import cPickle as pickle

def UpdateLeague(day):
	tourney_data = pickle.load(open( "playerInfo.p", "rb" ))
	stat_map = pickle.load(open("statMap.p", "rb"))
	results = ausopen_query.GetDayResults()
	tourney_data.sort(key=lambda fPlayer: -1 * fPlayer.total)
	pickle.dump( tourney_data, open( "playerInfo.p", "wb" ) )
	return

def GetActiveMatchIds(teams, results):
	pass


if __name__ == "__main__":
	day = raw_input('Enter the tournament day: ')
	UpdateLeague(day)