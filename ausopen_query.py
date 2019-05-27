import constants

import pprint as pp
import requests

_TOURNAMENT = 'FR'

def CreateGetMatchUrl(match_id):
    return constants.GET_MATCH_URL_PREFIX + str(match_id)

def CreateFrGetMatchUrl(match_id):
    return constants.GET_FR_MATCH_URL_PREFIX + str(match_id)

def CreateAusGetResultsUrl(day):
    return constants.GET_AUS_RESULTS_URL_PREFIX + str(day) + constants.GET_AUS_RESULTS_URL_SUFFIX

def CreateFrGetResultsUrl(day):
    return constants.GET_FR_RESULTS_URL_PREFIX + str(day)

def GetFrDayResults(day):
    response = requests.get(CreateFrGetResultsUrl(day), headers=constants.GET_FR_RESULTS_HEADER)
    return response.json()['matches']

def GetDayResults(day):
    response = requests.get(CreateGetResultsUrl(day),
            headers=constants.GET_RESULTS_HEADER)
    return response.json()['matches']

def GetAusDayMatchIds(matches):
    """Input must be the result of GetDayResults"""
    match_ids_and_winners = []
    for match in matches:
        if match['match_state'] != 'Complete':
            continue
        info = [match['match_id']]
        if 'status' in match['teams'][0] and match['teams'][0]['status'] == 'Winner':
            info = info + [0]
        else:
            info = info + [1]
        match_ids_and_winners.append(info)
    return match_ids_and_winners

def GetFrenchDayMatchIdsAndWinners(matches):
    """Input must be the result of GetDayResults"""
    match_ids_and_winners = []
    for match in matches:
        if 'Singles' in match['matchData']['typeLabel']:
            match_ids_and_winners.append([match['id'], match['teamB']['winner'] == True])
    return match_ids_and_winners

def GetDayMatches(day):
    matches = GetFrDayResults(day)
    if _TOURNAMENT == 'AUS':
        match_ids = GetAusDayMatchIds(matches)
    elif _TOURNAMENT == 'FR':
        match_ids = GetFrenchDayMatchIdsAndWinners(matches)
    else:
        match_ids = None

    match_dict = {}

    for match_id, winner in match_ids:
        print("Match id: %s", match_id)
        match_url = CreateFrGetMatchUrl(match_id)
        match = GetMatch(match_url)
        pp.pprint(match)
        stats = GetFrMatchStats(match)
        pp.pprint(stats)
        players = GetFrMatchPlayerNames(match)
        pp.pprint(players)

        match_dict[players['playerA']] = ['playerA', stats, winner]
        match_dict[players['playerB']] = ['playerB', stats, winner]

    return match_dict


def GetMatch(url):
    print("Here is the GetMatch url: %s", url)
    response = requests.get(url, headers=constants.GET_FR_MATCH_HEADER)
    return response.json()

def GetMatchStats(match_dict):
    """Input must be the result of GetMatch"""
    pp.pprint(match_dict)
    raw_stats = match_dict['stats']['key_stats'][0]['sets'][-1]['stats']
    formatted_stats = {}
    for stat in raw_stats:
        if stat['name'] == 'Break points won':
            a_breaks_won = int(stat['teamA']['secondary'].split('/')[0])
            b_breaks_won = int(stat['teamB']['secondary'].split('/')[0])
            formatted_stats['Break points won'] = [a_breaks_won, b_breaks_won]
            a_breaks_total = int(stat['teamA']['secondary'].split('/')[1])
            b_breaks_total = int(stat['teamB']['secondary'].split('/')[1])
            formatted_stats['Break points saved'] = [b_breaks_total - b_breaks_won, a_breaks_total - a_breaks_won]
        else:
           formatted_stats[stat['name']] = [int(stat['teamA']['primary']), int(stat['teamB']['primary'])]
    return formatted_stats

def GetFrMatchStats(match_dict):
    """Input must be the result of GetMatch"""
    formatted_stats = {}
    for stat in match_dict['setStats']['set0']:
        if stat['name'] == 'Break points won':
            a_breaks_won = int(stat['player1'].split('/')[0])
            b_breaks_won = int(stat['player2'].split('/')[0])
            formatted_stats['Break points won'] = [a_breaks_won, b_breaks_won]
            a_breaks_total = int(stat['player1'].split('/')[1].split(' ')[0])
            b_breaks_total = int(stat['player2'].split('/')[1].split(' ')[0])
            formatted_stats['Break points saved'] = [b_breaks_total - b_breaks_won, a_breaks_total - a_breaks_won]
        elif '%' in str(stat['player1']):
            a_scores = stat['player1'].split('/')
            b_scores = stat['player2'].split('/')
            formatted_stats[stat['name']] = [int(round(int(a_scores[0]) * 100 / int(a_scores[1].split(' ')[0]))),
                                             int(round(int(b_scores[0]) * 100 / int(b_scores[1].split(' ')[0])))]
        else:
            formatted_stats[stat['name']] = [int(stat['player1']), int(stat['player2'])]
    return formatted_stats

def GetMatchPlayerNames(match_dict):
    """Input must be the result of GetMatch"""
    return {'playerA': match_dict['teams'][0]['players'][0]['full_name'].encode("utf-8"),
            'playerB': match_dict['teams'][1]['players'][0]['full_name'].encode("utf-8")}

def GetFrMatchPlayerNames(match_dict):
    return {'playerA': match_dict['players'][0]['player1name'],
            'playerB': match_dict['players'][1]['player1name']}

if __name__ == "__main__":
    pp.pprint(GetFrenchMatchStats(GetMatch(constants.GET_FR_MATCH_URL)))
