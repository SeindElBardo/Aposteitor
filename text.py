import time
import os
import pathlib
print(os.getcwd())
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

total_report = "Los resultados han sido:\n"
bets_logs = "Las apuestas efectuadas durante la ronda han sido:\n\n"
triplets = "\nPremios de las tripletas:\n\n"

def report_bet_for(name):
    return ("\nApuestas por {}:\n\n".format(name))

def report_bets_results(bettor, prize):
    return ("\t" + bettor + " ha ganado " + prize + " monedas de oro\n")

def beeting_log(bettor, prize, competitor, bet_type):
    # This is better than a log class attribute
    pass

## LOGs

def log_new_round(name):
    return "[{}]\t created new round with name: {}\n".format(time.strftime("%d/%m/%y - %H:%M:%S"), name)


def log_add_competitor(name):
    return "[{}]\t added new competitor with name: {}\n".format(time.strftime("%d/%m/%y - %H:%M:%S"), name)


def log_add_simple_bet(bettor_name, amount, beneficiarie_name, bet_type):
    return "[{}]\t created new simple bet: {}, {}, {}, {}\n".format(time.strftime("%d/%m/%y - %H:%M:%S"), bettor_name, amount, beneficiarie_name, bet_type)


def log_add_composite_bet(bettor_name, amount, beneficiarie_name):
    return "[{}]\t created new composite bet: {}, {}, {} {} {}, {}\n".format(time.strftime("%d/%m/%y - %H:%M:%S"), bettor_name, amount, beneficiarie_name[0], beneficiarie_name[1], beneficiarie_name[2], 4)


def log_proclaim_winner(winner_name):
    return "[{}]\t proclaimed the following winner: {}\n".format(time.strftime("%d/%m/%y - %H:%M:%S"), winner_name)

def log_proclaim_winners(winners_names):
    return "[{}]\t proclaimed the following winners: {}, {}, {}\n".format(time.strftime("%d/%m/%y - %H:%M:%S"), winners_names[0], winners_names[1], winners_names[2])


def log_distribute_prize(report):
    return "[{}]\t the report of the distribute_prize function is:\n{}\n".format(time.strftime("%d/%m/%y - %H:%M:%S"), report)

