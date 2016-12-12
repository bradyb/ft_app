import cPickle as pickle
from playerTypes import tPlayer


def moveFromBench(playerName, userName):

	attribute = ""

	name = ""

	tourneyData = pickle.load(open( "playerInfo.p", "rb" ))

	for user in tourneyData:

		if user.name != userName:
			continue

		for player in user.bench:

			if player.name != playerName:
				continue

			attribute = player.attribute

			user.team.append(player)

			break

		for player in user.team:

			if player.attribute != attribute:
				continue

			name = player.name

			user.bench.append(player)

			break

		user.bench = [player for player in user.bench if player.name != playerName]

		user.team = [player for player in user.team  if player.name != name]

		user.team.sort(key=lambda tPlayer: tPlayer.attribute)

		pickle.dump( tourneyData, open( "playerInfo.p", "wb" ) )

		return user 

