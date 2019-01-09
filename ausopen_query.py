import constants

import pprint as pp
import requests

def GetDayResults():
	response = requests.get(constants.GET_RESULTS_URL, 
							headers=constants.GET_RESULTS_HEADER)
	return response.json()['matches']

def GetMatch():
	response = requests.get(constants.GET_MATCH_URL, 
							headers=constants.GET_MATCH_HEADER)
	return response.json()

def GetMatchStats(match_dict):
	"""Input must be the result of GetMatch"""
	return match_dict['stats']['key_stats'][0]['sets'][-1]

def GetMatchPlayerNames(match_dict):
	"""Input must be the result of GetMatch"""
	return {'playerA': match_dict['teams'][0]['players'][0]['full_name'].encode("utf-8"),
			'playerB': match_dict['teams'][1]['players'][0]['full_name'].encode("utf-8")}

if __name__ == "__main__":
	pp.pprint(GetMatchPlayerNames(GetMatch()))