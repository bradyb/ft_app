import cPickle as pickle

def AddPlayer(team_name, player_name, attribute):

    attribute_map = pickle.load(open( "attrMap.p", "rb" ))

    tourney_data = pickle.load(open( "playerInfo.p", "rb" ))

    for team in tourney_data:
        if team.name == team_name:
            team.addPickUp(player_name, 'm', attribute_map[attribute])

    pickle.dump(tourney_data, open("playerInfo.p", "wb"))

def PopPickUps():
     tourney_data = pickle.load(open( "playerInfo.p", "rb" ))
     for team in tourney_data:
         team.bench.pop()
     pickle.dump(tourney_data, open("playerInfo.p", "wb"))

if __name__=="__main__":
    AddPlayer('Steve', 'Grigor Dimitrov', 'power')

