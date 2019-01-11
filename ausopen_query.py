import constants

import pprint as pp
import requests

def CreateGetMatchUrl(match_id):
	return constants.GET_MATCH_URL_PREFIX + str(match_id)

def GetDayResults(day):
	response = requests.get(constants.GET_RESULTS_URL,
							headers=constants.GET_RESULTS_HEADER)
	return response.json()['matches']

def GetDayMatchIds(matches):
	"""Input must be the result of GetDayResults"""
	return [ match['match_id'].encode("utf-8") for match in matches]

def GetDayMatches(day):
	matches = GetDayResults(day)
	match_ids = GetDayMatchIds(matches)

	match_dict = {}

	for match_id in match_ids:
		match_url = CreateGetMatchUrl(match_id)
		match = GetMatch(match_url)

		stats = GetMatchStats(match)
		players = GetMatchPlayerNames(match)

		match_dict[players['playerA']] = ['playerA', stats]
		match_dict[players['playerB']] = ['playerB', stats]


def GetMatch(url):
	response = requests.get(url, headers=constants.GET_MATCH_HEADER)
	return response.json()

def GetMatchStats(match_dict):
	"""Input must be the result of GetMatch"""
	raw_stats = match_dict['stats']['key_stats'][0]['sets'][-1]['stats']
	formatted_stats = {}
	for stat in raw_stats:
	    if stat['name'] == 'Break points won':
	        a_breaks_won = int(stat['teamA']['secondary'].split('/')[0])
	        b_breaks_won = int(stat['teamB']['secondary'].split('/')[0])
	        formatted_stats['Break points won'] = [a_breaks_won, b_breaks_won]
	        a_breaks_total = int(stat['teamA']['secondary'].split('/')[1]) if formatted_stats['Break points won'][0] else 0
	        b_breaks_total = int(stat['teamB']['secondary'].split('/')[1]) if formatted_stats['Break points won'][1] else 0
	        formatted_stats['Break points saved'] = [b_breaks_total - b_breaks_won, a_breaks_total - a_breaks_won]
	        continue
	    formatted_stats[stat['name']] = [int(stat['teamA']['primary']), int(stat['teamB']['primary'])]
	return formatted_stats

def GetMatchPlayerNames(match_dict):
	"""Input must be the result of GetMatch"""
	return {'playerA': match_dict['teams'][0]['players'][0]['full_name'].encode("utf-8"),
			'playerB': match_dict['teams'][1]['players'][0]['full_name'].encode("utf-8")}

if __name__ == "__main__":
	pp.pprint(GetMatchPlayerNames(GetMatch()))