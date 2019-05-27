###########
# Constants for gettings results from matches for a day.
###########

GET_AUS_RESULTS_HEADER = {
	'Accept': 'application/json, text/plain, */*',
	'Origin': 'https://ausopen.com',
	'Referer': 'https://ausopen.com/results',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}

GET_AUS_RESULTS_URL_PREFIX = 'https://prod-scores-api.ausopen.com/year/2019/period/MD/day/'
GET_AUS_RESULTS_URL_SUFFIX = '/results'

GET_FR_RESULTS_HEADER = {
        'Accept': 'application/json, text/plain, */*',
	'Referer': 'https://rolandgarros.com/en-us/',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}
        

GET_FR_RESULTS_URL_PREFIX = 'https://www.rolandgarros.com/api/en-us/finished?tournamentDay='

###########
# Constants for gettings results from matches for a day.
###########

GET_AUS_MATCH_HEADER = {
	'accept': 'application/json, text/plain, */*',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-US,en;q=0.9',
	'origin': 'https://ausopen.com',
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}

GET_AUS_MATCH_URL = 'https://prod-scores-api.ausopen.com/match-centre/PS120'

GET_AUS_MATCH_URL_PREFIX = 'https://prod-scores-api.ausopen.com/match-centre/'

GET_FR_MATCH_HEADER = {
	'accept': 'application/json, text/plain, */*',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-US,en;q=0.9',
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}

GET_FR_MATCH_URL = 'https://itp.infosys-platforms.com/api/stats-plus/rg/keystats/year/2019/eventId/520/matchId/SM096'

GET_FR_MATCH_URL_PREFIX = 'https://itp.infosys-platforms.com/api/stats-plus/rg/keystats/year/2019/eventId/520/matchId/'

DATES_2019_AUS = [
	'1/14/19',
	'1/15/19',
	'1/16/19',
	'1/17/19',
	'1/18/19',
	'1/19/19',
	'1/20/19',
	'1/21/19',
	'1/22/19',
	'1/23/19',
	'1/24/19',
	'1/25/19',
	'1/26/19',
	'1/27/19',
	'1/28/19',
	'1/29/19',
]

DATES_2019_FR = [
        '20190526',
        '20190527',
        '20190528',
        '20190529',
        '20190530',
        '20190531',
        '20190601',
        '20190602',
        '20190603',
        '20190604',
        '20190605',
        '20190606',
        '20190607',
        '20190608',
        '20190609',
]
