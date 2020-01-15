import aposteitor as app

#Creamos jugadores
pepe = app.Player("Pepe", 2000)
jose = app.Player("Jose", 1000)
tetona = app.Player("tetona", 3000)

#creamos participantes
gala = app.Competitor("Gala")
galaI = app.Competitor("GalaIncognito")
diana = app.Competitor("Diana")
dianaI = app.Competitor("DianaIncognito")

#Los incluimos en una ronda
ronda = app.Round()
ronda.loadPNJs()
ronda.add_competitors([gala, galaI, diana, dianaI])
print (pepe.__dict__,jose.__dict__,tetona.__dict__)

ronda.register_simple_bet(pepe, 10, gala, 1)
#ronda.register_simple_bet(jose, 20, galaI, 2)
#ronda.register_simple_bet(tetona, 30, diana, 3)

#ronda.register_simple_bet(pepe, 40, galaI, 1)
ronda.register_simple_bet(jose, 50, diana, 2)
ronda.register_simple_bet(tetona, 60, dianaI, 3)

#ronda.register_simple_bet(pepe, 70, diana, 1)
ronda.register_simple_bet(jose, 80, dianaI, 2)
ronda.register_simple_bet(tetona, 90, gala, 3)

#ronda.register_composite_bet(pepe, 100, [gala, galaI, diana])
#ronda.register_composite_bet(jose, 110, [gala, galaI, diana])
#ronda.register_composite_bet(tetona, 120, [diana, dianaI, gala])

print (pepe.__dict__,jose.__dict__,tetona.__dict__)
#ronda.generate_padding_bets(20)

ronda.proclaim_winner([gala, galaI, diana])

print(ronda.triplet_bets)
print(ronda.pot)
print(ronda.jackpot)
print(ronda.triplet_pot)
print(ronda.triplet_jackpot)

if ronda.pot == (60+150+240):
    print("pot SUCCESSFUL")
if ronda.jackpot == (10 + 90*0.4 + 20*0.7 + 30*0.4):
    print("jackpot SUCCESSFUL")
if ronda.triplet_pot == (330):
    print("triple_pot SUCCESSFUL")
if ronda.triplet_jackpot == (210):
    print("triple_jackpot SUCCESSFUL")
print(ronda.distribute_prize([gala]))

print (pepe.__dict__,jose.__dict__,tetona.__dict__)