###########
# Constants for gettings results from matches for a day.
###########

GET_RESULTS_HEADER = {
	'Accept': 'application/json, text/plain, */*',
	'Origin': 'https://ausopen.com',
	'Referer': 'https://ausopen.com/results',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}

GET_RESULTS_URL_PREFIX = 'https://prod-scores-api.ausopen.com/year/2019/period/MD/day/'
GET_RESULTS_URL_SUFFIX = '/results'

###########
# Constants for gettings results from matches for a day.
###########

GET_MATCH_HEADER = {
	'accept': 'application/json, text/plain, */*',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-US,en;q=0.9',
	'origin': 'https://ausopen.com',
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}

GET_MATCH_URL = 'https://prod-scores-api.ausopen.com/match-centre/PS120'

GET_MATCH_URL_PREFIX = 'https://prod-scores-api.ausopen.com/match-centre/'


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