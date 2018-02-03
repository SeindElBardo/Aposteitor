import aposteitor as app

#Creamos jugadores
pepe = app.Jugador("Pepe", 200)
jose = app.Jugador("Jose", 100)
tetona = app.Jugador("tetona", 300)

#creamos participantes
gala = app.Participante("Gala")
galaI = app.Participante("GalaIncognito")

#Los incluimos en una ronda
ronda = app.Ronda()
ronda.loadPNJs()
ronda.addParticipante(gala)
ronda.addParticipante(galaI)
print (pepe.__dict__,jose.__dict__,tetona.__dict__)
ronda.crearApuesta(pepe, 30, gala)
ronda.crearApuesta(pepe, 30, galaI)
ronda.crearApuesta(pepe, 50, gala)
print (pepe.__dict__,jose.__dict__,tetona.__dict__)
ronda.generarApuestasDeRelleno(20)
ronda.proclamarGanador([gala])
print(ronda.boteGanador)
ronda.repartirPremio([gala])
print (pepe.__dict__,jose.__dict__,tetona.__dict__)