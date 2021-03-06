import ausopen_query
import constants

import _pickle as pickle
import pprint as pp
import os

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

def ComputeFrName(name):
    if name == 'Juan Martin Del Potro':
        return 'JM. DEL POTRO'
    else:
        return name[0].upper() + '. ' + name.split(' ')[-1].upper()

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

	player_matches = ausopen_query.GetDayMatches(constants.DATES_2019_FR[day])


	date_formatted =  constants.DATES_2019_FR[day]

	for team in tourney_data:
		for player in team.team:
		    already_played = False
		    added_day = False
		    for day in player.history:
		        if date_formatted != day[0]:
		            continue
		        if "-" != day[1] or "OUT" == day[1]:
		            already_played = True
		        else:
		            added_day = True
		    if already_played:
		        continue
		    if player.alive != 1:
		        player.history.append((date_formatted, 'OUT'))
		        continue
		    match_stats = None
		    if ComputeFrName(player.name) in player_matches:
		        match_stats = player_matches[ComputeFrName(player.name)]
		    elif added_day:
		        continue
		    else:
		        player.history.append((date_formatted, "-"))
		        continue

		    player_index = 1
		    if match_stats[0] == 'playerA':
		        player_index = 0

		    points_earned = GetPoints(player_index, player.attribute, match_stats[1])
		    player.points = player.points + points_earned
		    if added_day:
		        player.history[-1] = (date_formatted, points_earned)
		    else:
		        player.history.append((date_formatted, points_earned))
		    team.total = team.total + points_earned

		    player.alive = match_stats[2] == player_index

		for player in team.bench:
			already_played = False
			added_day = False
			for day in player.history:
				if date_formatted != day[0]:
				    continue
				if "-" != day[1] or "OUT" == day[1]:
					already_played = True
				else:
				    added_day = True
			if already_played:
				continue
			if player.alive != 1:
				player.history.append((date_formatted, 'OUT'))
				continue

			match_stats = None
			if player.name in player_matches:
				match_stats = player_matches[player.name]
			elif added_day:
			    continue
			else:
				player.history.append((date_formatted, "-"))
				continue

			player_index = None
			if match_stats[0] == 'playerA':
				player_index = 0
			else:
				player_index = 1

			points_earned = GetPoints(player_index, player.attribute,
									  match_stats[1])
			if added_day:
			    player.history[-1] = (date_formatted, '(' + str(points_earned) + ')')
			else:
			    player.history.append((date_formatted, '(' + str(points_earned) + ')'))
			player.alive = match_stats[2] == player_index


	tourney_data.sort(key=lambda fPlayer: -1 * fPlayer.total)
	pickle.dump( tourney_data, open( "playerInfo.p", "wb" ) )
	return


if __name__ == "__main__":
    #os.chdir("/home/bees1224/ft_app/")
    UpdateLeague(0)
