def simple_bet(bettor, amount, beneficiaries, bet_type):
    if bet_type == 1:
        bet_type = "Ganador"
    elif bet_type == 2:
        bet_type = "Colocado"
    elif bet_type == 3:
        bet_type = "Tercero"
    return (bettor + " ha apostado " + amount + " monedas de oro por " + beneficiaries + " en calidad de " + bet_type)

def composite_bet(bettor, amount, beneficiaries):
    return ("{} ha apostado {} monedas de oro a la tripleta 1-{}, 2-{}, 3-{}".format(bettor, amount, beneficiaries[0], beneficiaries[1], beneficiaries[2]))

total_report = "Los resultados han sido:\n\n"

def report_bet_for(name):
    return ("Apuestas por {}:\n\n".format(name))

def report_bets_results(bettor, prize):
    return ("\t" + bettor + " ha ganado " + prize + " monedas de oro\n")
