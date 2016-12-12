secondSrvPct = float(raw_input("Second Serve in percentage: "))
secondWin = float(raw_input("Second Serve percentavge won when in: "))

firstSrvPct = float(raw_input("First Serve in percentage: "))
firstWin = float(raw_input("First Serve percentavge won when in: "))


if firstSrvPct * firstWin > secondSrvPct * secondWin:
	print("Uhhhh no doy")
else: 
	print("Keep on keepin on")


