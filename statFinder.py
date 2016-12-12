from lxml import html
import requests
import operator

print 'Available stats: aces, 2nd-serve-points-won, break-points-saved, break-points-converted, return-percentage'

statType = raw_input('Which stat are you interested in? ')

### some error handling in case statType is not of the right form ###

page = requests.get('http://www.atpworldtour.com/en/stats/' + statType + '/2016/all/all/')
tree = html.fromstring(page.content)


### check to see what all of the other xpaths look like for the other stats ####
  # I suspect that the tables will be slightly different and the following block of code 
  # needs to be put into some control flow
  # players xpath should be const (?)
  
players = tree.xpath('//*[@id="statsListingTableContent"]/table/tbody/tr/td[1]/table/tbody/tr/td[4]/a/text()')
aces = tree.xpath('//*[@id="statsListingTableContent"]/table/tbody/tr/td[2]/text()')
matches = tree.xpath('//*[@id="statsListingTableContent"]/table/tbody/tr/td[3]/text()')

quotient = [float(item) / float(matches[aces.index(item)]) for item in aces]

index, value = max(enumerate(quotient), key=operator.itemgetter(1))

coupled = zip(quotient, players)

topPlayers = sorted(coupled, key=operator.itemgetter(0), reverse=True)

print 'The top servers are: ', topPlayers[0:4]


