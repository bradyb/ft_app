import ausopen_query

import cPickle as pickle

def ServeScore(index, stats):
	aces = stats['Aces'][index]
	double_faults = stats['Double faults'][index]
	return 3 * aces - 3 * double_faults

def PowerScore(index, stats):
	winners = stats['Winners'][index]
	unforced_errors = stats['Unforced errors'][index]
	return 2 * winners - unforced_errors

def ReturnScore(index, stats):
	return stats['Receiving points won'][index]

def DefenseScore(index, stats):
	return stats['Win 2nd serve'][index]

def MindScore(index, stats):
	opponent_breaks_won = stats['Break points won'][(index + 1) % 2]
	breaks_saved = stats['Break points saved'][index]
	breaks_won = stats['Break points won'][index]
	return 5 * (breaks_won + breaks_saved) - 3 * opponent_breaks_won

def GetPoints(index, attribute, stats):
	if attribute == 1:
		return ServeScore(index, stats)

	elif attribute == 2:
		return PowerScore(index, stats)

	elif attribute == 3:
		return ReturnScore(index, stats)

	elif attribute == 4:
		return DefenseScore(index, stats)		

	elif attribute == 5:
		return MindScore(index, stats)

def UpdateLeague(day):
	tourney_data = pickle.load(open( "playerInfo.p", "rb" ))
	stat_map = pickle.load(open("statMap.p", "rb"))
	
	player_matches = ausopen_query.GetDayMatches(day)

	today = datetime.datetime.now()
	date_formatted =  str(today.month) + '/' + str(today.day) + '/' + str(today.year)

	for team in tourney_data:
		for player in team.team:
			if player.alive != 1:
				player.history.append((date_formatted, 'OUT'))
				continue

			match_stats = None
			if player.name in player_matches:
				match_stats = player_matches[player.name]
			else:
				player.history.append((date_formatted, "DNP"))
				continue

			player_index = None
			if match_stats[0] == 'playerA':
				player_index = 'teamA'
			else:
				player_index = 'teamB'

			points_earned = GetPoints(player_index, player.attribute,
									  match_stats[1])
			player.points = player.points + points_earned
			player.history.append((date_formatted, points_earned))
			user.total = user.total + points_earned

		for player in team.bench:
			if benchPlayer.alive != 1:
				benchPlayer.history.append((date_formatted, 'OUT'))
				continue

			match_stats = None
			if player.name in player_matches:
				match_stats = player_matches[player.name]
			else:
				player.history.append((date_formatted, "DNP"))
				continue

			player_index = None
			if match_stats[0] == 'playerA':
				player_index = 0
			else:
				player_index = 1

			points_earned = GetPoints(player_index, player.attribute,
									  match_stats[1])
			player.history.append((date_formatted,'(' + str(points_earned) + ')'))

	tourney_data.sort(key=lambda fPlayer: -1 * fPlayer.total)
	pickle.dump( tourney_data, open( "playerInfo.p", "wb" ) )
	return


if __name__ == "__main__":
	day = raw_input('Enter the tournament day: ')
	UpdateLeague(day)