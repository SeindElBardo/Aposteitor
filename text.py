def simple_bet(apostador, cantidad, beneficiario, bet_type):
    if bet_type == 1:
        bet_type = "Ganador"
    elif bet_type == 2:
        bet_type = "Colocado"
    elif bet_type == 3:
        bet_type = "Tercero"
    return (apostador + " ha apostado " + cantidad + " monedas de oro por " + beneficiario + " en calidad de " + bet_type)

def composite_bet(apostador, cantidad, beneficiarios):
    return ("{} ha apostado {} monedas de oro a la tripleta 1-{}, 2-{}, 3-{}".format(apostador, cantidad, beneficiarios[0], beneficiarios[1], beneficiarios[2]))

total_report = "Los resultados han sido:\n\n"

def report_bet_for(nombre):
    return ("Apuestas por " + nombre)

def report_bets_results(apostador, premio):
    return ("\t" + apostador + " ha ganado " + premio + " monedas de oro\n")
