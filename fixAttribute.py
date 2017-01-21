import cPickle as pickle

tourneyData = pickle.load(open( "playerInfo.p", "rb" ))

for user in tourneyData:
	if user.name == 'Jack':
		for player in user.bench:
			if player.name == 'Dominic Thiem':
				player.attribute = 1
				print 'here'

pickle.dump( tourneyData, open( "playerInfo.p", "wb" ) )
