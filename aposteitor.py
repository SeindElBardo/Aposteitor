import os
import pathlib
os.chdir(pathlib.Path(__file__).parent.absolute())
import random
import math
import time
import text
import config

class Player(): # Called bettor on majority of variables
    def __init__(self, name, money):
        self.name = name
        self.money = self.initial_money = money

    def move_money(self, amount):
        """
        Update players' money when they bet.
        If it is not possible, raise an exception.
        
        :param      amount:  The amount
        :type       amount:  Double
        """
        if (self.money + amount) >= 0:
            self.money = round(self.money + amount, 2) # It is always rounded to avoid problems of arithmetic operations with floats
        else:
            raise ValueError("{} no tiene suficientes fondos como para hacer la apuesta. Actualmente sólo tiene {} pos".format(self.name, self.money))

    def bet(self, amount, bet_type):
        """
        Build a bet.
        
        :param      amount:      The amount
        :type       amount:      Double
        :param      bet_type:    The type of the bet (1 = winner, 2 = placed, 3 = third or <list of three Competitor> = triplet)
        :type       bet_type:    Int or list of three Competitor
        """
        if amount < 1:
            raise ValueError("Las apuestas deben ser de al menos un po") 
        self.move_money(-amount)
        if bet_type == 1:
            return BetWinner(self, amount)
        if bet_type == 2:
            return BetPlaced(self, amount)
        if bet_type == 3:
            return BetThird(self, amount)
        if type(bet_type) is list and len(bet_type) == 3:
            return BetTriplet(self, amount, bet_type)
        raise TypeError("Error creando la apuesta")


    def results(self):
        """
        Show the difference between the start money and the end money
        """
        return self.money - self.initial_money

class Npc(Player): # Para que no explote
    def __init__(self, name, average, variance, money = float("inf")):
        super(Npc, self).__init__(name, money)
        self.average = average
        self.variance = variance

    def generate_amount(self):
        """
        All pngs generating their amount for bet with a normal function.
        """
        amount = math.ceil(random.normalvariate(self.average, self.variance))
        if amount < 1:
            return 1
        return amount

class Competitor():
    def __init__(self, name):
        self.name = name
        self.bets = []
                        
class Bet():
    def __init__(self, bettor, amount):
        self.bettor = bettor
        self.amount = amount
        self.effective_amount = self.amount

# It may be a bad idea to use different classes
class BetWinner(Bet):
    def __init__(self, bettor, amount):
        super(BetWinner, self).__init__(bettor, amount)
        self.effective_amount = self.amount * config.par_effective_ratio_in_winner_bet
        self.type = 1

class BetPlaced(Bet):
    def __init__(self, bettor, amount):
        super(BetPlaced, self).__init__(bettor, amount)
        self.effective_amount = self.amount * config.par_effective_ratio_in_placed_bet
        self.type = 2

class BetThird(Bet):
    def __init__(self, bettor, amount):
        super(BetThird, self).__init__(bettor, amount)
        self.effective_amount = self.amount * config.par_effective_ratio_in_third_bet
        self.type = 3

class BetTriplet(Bet):
    def __init__(self, bettor, amount, triplet):
        super(BetTriplet, self).__init__(bettor, amount)
        self.triplet = triplet


class Round():
    def __init__(self, competitors = [], round_id = time.strftime("%d_%m_%y - %H:%M:%S")):
        self.id = round_id
        open(str(self.id) + ".log", "x")
        self.register_event("new_round", self.id)
        self.bettors = [] # Creo que no vale para nada
        self.npcs = []
        self.load_npcs()
        self.competitors = {}
        self.add_competitors(competitors)
        self.pot = 0.0
        self.jackpot = 0.0 # It is necessary to obtain the proportion of the jackpot
        self.winners = []
        self.triplet_bets = []
        self.triplet_pot = 0.0
        self.triplet_jackpot = 0.0 # It is necessary to obtain the proportion of the jackpot 
        self.triplet_winner_bets = []

    def exist_competitors(self, competitors):
        """
        Evaluates if some one of competitors within in the competitor's list given is already added in competitor's list of the round.
        
        :param      competitors:  The competitors
        :type       competitors:  List of Competitor. It's a list for convenience of a register_composite_bet function
        """
        for competitor in competitors:
            if competitor in self.competitors.values() or competitor.name in self.competitors.keys():
                return True
        return False

    def get_competitor_by_name(self, name):
        """
        Gets the competitor by name.
        
        :param      name:  The name
        :type       name:  String

        :returns:   The competitor
        :rtype:     Competitor
        """
        if name in self.competitors.keys():
            return self.competitors[name]
        raise ReferenceError("No existe un competidor llamado {} en la ronda actual".format(name)) 


    def add_competitors(self, competitors): ## Comprobar si se puede meter un participante en blanco o una lista
        """
        Adds competitors to list of the round. If the parameter competitors  is only the names, instantiates competitors objets before.
        Each competitor must have a different name and cannot be added more than once.
        
        :param      competitors:  The competitors
        :type       competitors:  List of Competitor or list of Strings
        """
        if type(competitors[0]) is str:
            for competitor_name in competitors:
                if competitor_name in self.competitors.keys():
                    raise NameError("El competidor {}ya está incluido en la ronda o ya existe un competidor con el mismo nombre".format(competitor.name))
                self.competitors[competitor_name] = Competitor(competitor_name)
                self.register_event("add_competitor", competitor_name)
        else: # competitors is a list
            for competitor in competitors:
                if self.exist_competitors([competitor]):
                    raise NameError("El competidor {}ya está incluido en la ronda o ya existe un competidor con el mismo nombre".format(competitor.name))
                self.competitors[competitor.name] = competitor
                self.register_event("add_competitor", competitor.name)



    def register_simple_bet(self, bettor, amount, competitor, bet_type):
        """
        Build a simple bet and registres it in the pool of bets of the round.
        
        :param      bettor:      The bettor
        :type       bettor:      Player
        :param      amount:      The amount
        :type       amount:      Double
        :param      competitors: The competitor
        :type       competitors: Competitor
        :param      bet_type:    The bet_type
        :type       bet_type:    Integer 1-3

        :returns:   Susccessful text
        :rtype:     String
        """
        if not self.exist_competitors([competitor]):
            raise ReferenceError("El competidor por el que se realiza la apuesta no está participando en esta ronda")
        competitor.bets.append(bettor.bet(amount, bet_type))
        self.pot += amount
        self.register_event("add_simple_bet", (bettor.name, amount, competitor.name, bet_type))
        return text.simple_bet(bettor.name, str(amount), competitor.name, bet_type)


    def register_composite_bet(self, bettor, amount, competitors):
        """
        Build a composite bet (triplet) and registres it in the pool of bets of the round.
        
        :param      bettor:       The bettor
        :type       bettor:       Player
        :param      amount:       The amount
        :type       amount:       Double
        :param      competitors:  The competitors
        :type       competitors:  List of three Competitors

        :returns:   Susccessful text
        :rtype:     String
        """
        if not self.exist_competitors(competitors):
            raise ReferenceError("Uno o varios de los competidores por los que se realiza la apuesta no están participando en esta ronda")
        self.triplet_bets.append(bettor.bet(amount, competitors))
        self.triplet_pot += amount
        self.register_event("add_composite_bet", (bettor.name, amount, [competitor.name for competitor in competitors]))
        return text.composite_bet(bettor.name, str(amount), [competitor.name for competitor in competitors])


    def proclaim_winner(self, winners):
        """
        Prepare the jackpots for distribute the prize.
        
        :param      winners:  The winners
        :type       winners:  List of Competitors
        """
        winner_index = 0
        while winner_index < len(winners): # Simple bets
            for bet in winners[winner_index].bets:
                if bet.type > winner_index:
                    self.jackpot += bet.effective_amount
            winner_index += 1
        if len(winners) == 3: # Triplet bets
            for bet in self.triplet_bets:
                if bet.triplet == winners:
                    self.triplet_winner_bets.append(bet)
                    self.triplet_jackpot += bet.effective_amount
        self.register_event("proclaim_winner", [competitor.name for competitor in winners])


    def distribute_prize(self, winners):
        """
        Updates the bettors money with the prize obtained (is necessary to call proclaim winner function before).
        The house gains the money don't reparted.
        
        :param      winners:  The winners
        :type       winners:  List of one or three Competitors

        :returns:   Reports the prizes
        :rtype:     String
        """
        report = text.total_report
        gains_for_house = self.pot + self.triplet_pot
        # Simple bets
        proportion_simple_bets = self.pot/self.jackpot if self.jackpot >= 1 else 0
        winner_index = 0
        while winner_index < len(winners):
            report += text.report_bet_for(winners[winner_index].name)
            for bet in winners[winner_index].bets:
                if bet.type > winner_index:
                    prize = math.floor(bet.effective_amount*proportion_simple_bets*100)/100
                    if config.par_round_coins:
                        prize = int(prize)
                    bet.bettor.move_money(prize)
                    gains_for_house = round(gains_for_house - prize, 2)
                    report += text.report_bets_results(bet.bettor.name, str(prize))
            winner_index += 1
        # Triplet bets
        proportion_triplet_bets = self.triplet_pot/self.triplet_jackpot if self.triplet_jackpot >= 1 else 0
        if len(winners) == 3:
            for bet in self.triplet_winner_bets:
                report += text.report_bet_for(bet.bettor.name)
                prize = math.floor(bet.effective_amount*proportion_triplet_bets*100)/100
                if config.par_rounds_coins:
                        prize = int(prize)
                bet.bettor.move_money(prize)
                gains_for_house = round(gains_for_house - prize, 2)
                report += text.report_bets_results(bet.bettor.name, str(prize))
        report += text.report_bets_results("\n\nHouse", str(gains_for_house))
        self.register_event("distribute_prize", report)
        return report

    def load_npcs(self):
        """
        Loads npcs so they can bet.
        """
        try:
            file_handle = open("./npcs.txt", "r")
        except:     
            file_handle = open("npcs.txt", "w")
            file_handle.close()
            return
        npcs_list = file_handle.readlines()[1:] # Remove first line (headers)
        for npc in npcs_list:
            npc = npc[:-1] # Remove line break
            npc_atributes = npc.split(';')
            self.npcs.append(Npc(npc_atributes[0], int(npc_atributes[1]), float(npc_atributes[2])))
            file_handle.close()


    def generate_padding_bets(self, amount):
        """
        Generate the indicated amount of bets.
        
        :param      amount:  The amount
        :type       amount:  Integer
        """
        competitors = list(self.competitors.values())
        for x in range(amount):
            npc = random.choice(self.npcs)
            if random.random() < config.par_simple_npcs_bets:
                self.register_simple_bet(npc, npc.generate_amount(), random.choice(competitors), random.randrange(1,4))
            else:
                random.shuffle(competitors)
                self.register_composite_bet(npc, npc.generate_amount(), [competitors[0], competitors[1], competitors[2]])



## LOGs 
    def register_event(self, event_type, args):
        log_file = open(str(self.id) + ".log", "a+")
        apt_file = open(str(self.id) + ".apt", "a+")
        if event_type == "new_round":
            log_file.write(text.log_new_round(args))
        elif event_type == "add_competitor":
            log_file.write(text.log_add_competitor(args)) # args = competitor name
            if apt_file.tell() > 0:
                apt_file.write(",{}".format(args))
            else:
                apt_file.write("{}".format(args))
        elif event_type == "add_simple_bet":
            log_file.write(text.log_add_simple_bet(args[0], args[1], args[2], args[3])) # args = (bettor name, amount, beneficiarie name, bet_type)
            apt_file.write("\n{},{},{},{}".format(args[0], args[1], args[2], args[3]))
        elif event_type == "add_composite_bet":
            log_file.write(text.log_add_composite_bet(args[0], args[1], args[2])) # args = (bettor name, amount, beneficiaries names)
            apt_file.write("\n{},{},{}".format(args[0], args[1], args[2][0], args[2][1], args[2][2]))
        elif event_type == "proclaim_winner":
            log_file.write(text.log_proclaim_winner(args)) # args = list of winners names
            apt_file.write("\n{},{},{}".format(args[0], args[1], args[2]))
        elif event_type == "distribute_prize":
            log_file.write(text.log_distribute_prize(args)) # args = report to distribute_prize function
        log_file.close()
        apt_file.close()


# APT files
def load_apt(file, npcs_bets, generates_log = False):
    """
    Loads an apt 
    
    :param      file:           The file
    :type       file:           String
    :param      npcs_bets:      The amount of npcs_bets
    :type       npcs_bets:      Integer
    :param      generates_log:  Normaly the logs exits already. If this param is True, makes it again.
    :type       generates_log:  boolean
    """
    # Makes Round and adds competitors
    try:
        commands = open(file, "r").readlines()
    except:
        print("{} doesn't exist in current directory")
        return
    competitors = commands[0][:-1].split(',')
    simulation = Round(competitors)
    # Makes bets
    simulation.generate_padding_bets(npcs_bets)
    bettors = {}
    for command_index in range(1, len(commands)-2):
        bet = commands[command_index].replace('\n','').split(',')
        if not (bet[0] in bettors.keys()):
            bettors[bet[0]] = Player(bet[0], 335000)
        bettor = bettors[bet[0]]
        competitor = simulation.get_competitor_by_name(bet[2])
        if len(bet) == 4: # simple bet
            simulation.register_simple_bet(bettor, int(bet[1]), competitor, int(bet[3]))
        else: # composite bet
            second_competitor = simulation.get_competitor_by_name(bet[3])
            third_competitor = simulation.get_competitor_by_name(bet[4])
            simulation.register_composite_bet(bettor, int(bet[1]), [competitor, second_competitor, third_competitor])
    # Proglaims winner
    winners_names = commands.pop().split(",")
    if not (
            (len(simulation.competitors.items()) > 2 and len(winners_names) == 3) or
            (len(simulation.competitors.items()) == 2 and len(winners_names) == 1)):
        raise EnvironmentError("El número de ganadores no es consistente con el número de participantes")
    winners = []
    for winner_name in winners_names:
        winners.append(simulation.get_competitor_by_name(winner_name))
    simulation.proclaim_winner(winners)
    reply = simulation.distribute_prize(winners)
    print(reply)
    if(not generates_log):
        log_file = remove(str(simulation.id) + ".log")