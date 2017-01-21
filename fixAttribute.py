import cPickle as pickle

tourneyData = pickle.load(open( "playerInfo.p", "rb" ))

for user in tourneyData:
	if user.name == 'Geoff':
		user.addPickUp('Dominic Thiem', 'm', 4)

pickle.dump( tourneyData, open( "playerInfo.p", "wb" ) )
