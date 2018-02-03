def bet(apostador, cantidad, beneficiario):
	return (apostador + " ha apostado " + cantidad + " monedas de oro por " + beneficiario)

rpTotal = "Los resultados han sido:\n\n"

def rpBetOf(nombre):
	return ("Apuestas por " + nombre)

def rpBetResults(apostador, premio):
	return ("\t" + apostador + " ha ganado " + premio + " monedas de oro\n")
