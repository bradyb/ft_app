import cPickle as pickle


statMap = {"serve": "Aces", 'df': '3', 'defense': '6', 'mind': '7', 'bpsConv': '12', 'return': '10', 'return2': '11'}

pickle.dump(statMap, open("statMap.p", "wb"))

attrMap = {"serve": 1, "power": 2, "return": 3, "defense": 4, "mind": 5}

pickle.dump(attrMap, open("attrMap.p", "wb"))

