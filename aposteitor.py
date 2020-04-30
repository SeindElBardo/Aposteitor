import os
import pathlib
import random
import math
import time
from . import text
from . import config

LOCAL_PATH = pathlib.Path(__file__).parent.absolute()

class Player(): # Called bettor on majority of variables
    def __init__(self, name, money):
        self.name = name
        self.money = self.initial_money = money


    def move_money(self, amount):
        """Increase amount of money.
        
        Change the player's amount of money by increasing or decreasing according to the specified amount.
        If this change causes the player's money to be less that 0, raises a ValueError.
        
        Arguments:
            amount {Integer} -- Amount that is added to the real money of the players
        
        Raises:
            ValueError -- The final money don't be lower than 0
        """
        if (self.money + amount) >= 0:
            self.money = round(self.money + amount, 2) # It is always rounded to avoid problems of arithmetic operations with floats
        else:
            raise ValueError("{} no tiene suficientes fondos como para hacer la apuesta. Actualmente sólo tiene {} pos".format(self.name, self.money))


    def bet(self, amount, bet_type):
        """Builds a bet.
        
        Instances a Bet object according to the specified amount and the bet type. 
        
        Arguments:
            amount {[Double]} -- The amount
            bet_type {Int or list of three Competitor} -- The type of the bet (1 = winner, 2 = placed, 3 = third or <list of three Competitor> = triplet)
        
        Returns:
            Bet -- Instance of the amount and type bet specified 
        
        Raises:
            ValueError -- amount must must at least 1
            TypeError -- type_bet must be a number between 1 and 4
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
        """Calculates the difference between the start money and the end money.
        
        Calculates the difference between the start money and the end money.
        
        Returns:
            Double -- Difference between the start money and the end money
        """
        return self.money - self.initial_money


class Npc(Player): # Para que no explote
    def __init__(self, name, average, variance, money = float("inf")):
        super(Npc, self).__init__(name, money)
        self.average = average
        self.variance = variance


    def generate_amount(self):
        """Generates a amount with a function.
        
        All pngs generating their amount for bet with a normal function.
        
        Returns:
            Integer -- amount for a bet
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
        self.effective_amount = self.amount * config.EFFECTIVE_RATIO_IN_WINNER_BET
        self.type = 1


class BetPlaced(Bet):
    def __init__(self, bettor, amount):
        super(BetPlaced, self).__init__(bettor, amount)
        self.effective_amount = self.amount * config.EFFECTIVE_RATIO_IN_PLACED_BET
        self.type = 2


class BetThird(Bet):
    def __init__(self, bettor, amount):
        super(BetThird, self).__init__(bettor, amount)
        self.effective_amount = self.amount * config.EFFECTIVE_RATIO_IN_THIRD_BET
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
        """Checks if a competitor exits already.
        
        Evaluates if some one of competitors within in the competitor's list given is already added in competitor's list of the round.
                
        Arguments:
            competitors {List of Competitor} -- It's a list for convenience of a register_composite_bet function
        
        Returns:
            bool -- True if competitor is in list
        """
        for competitor in competitors:
            if competitor in self.competitors.values() or competitor.name in self.competitors.keys():
                return True
        return False

    def get_competitor_by_name(self, name):
        """Gets a object competitor with the name.
        
        Gets the competitor by name from competitors list.
        
        Arguments:
            name {String} -- Value in name atribute.
        
        Returns:
            Competitor -- Competitor object which name is the specified in param
        
        Raises:
            ReferenceError -- Raises if don't exists a competitor with the specified name in the list
        """
        if name in self.competitors.keys():
            return self.competitors[name]
        raise ReferenceError("No existe un competidor llamado {} en la ronda actual".format(name)) 


    def add_competitors(self, competitors): ## Comprobar si se puede meter un participante en blanco o una lista
        """Adds one o many competitors to list.
        
        Adds competitors to list of the round. If the parameter competitors  is only the names, instantiates competitors objets before.
        Each competitor must have a different name and cannot be added more than once.
        
        :param      competitors:  The competitors
        :type       competitors:  List of Competitor or list of Strings
        
        Arguments:
            competitors {list of Competitor or list of Stings} -- List with competitors objects or names to add
        
        Raises:
            NameError -- Don't exists a competitor with these name
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
        """Add a simple bet to list of bets.
        
        Build a simple bet and registres it in the pool of bets of the round.
        
        Arguments:
            bettor {Player} -- Player that does the bet
            amount {Integer} -- Amount of money beted
            competitor {Competitor} -- Competitor by the which does the bet
            bet_type {Integer} -- Number that identifys the bet type
        
        Returns:
            String -- Susccessful
        
        Raises:
            ReferenceError -- Competitor don't exist
        """
        if not self.exist_competitors([competitor]):
            raise ReferenceError("El competidor por el que se realiza la apuesta no está participando en esta ronda")
        competitor.bets.append(bettor.bet(amount, bet_type))
        self.pot += amount
        self.register_event("add_simple_bet", (bettor.name, amount, competitor.name, bet_type))
        return text.simple_bet(bettor.name, str(amount), competitor.name, bet_type)


    def register_composite_bet(self, bettor, amount, competitors):
        """Add a simple bet to list of bets.
        
        Build a composite bet (triplet) and registres it in the pool of bets of the round.
        
        Arguments:
            bettor {Player} -- Player that does the bet
            amount {Integer} -- Amount of money beted
            competitor {Competitor} -- Competitor by the which does the bet
        
        Returns:
            String -- Susccessful
        
        Raises:
            ReferenceError -- Competitor don't exist
        """
        
        if not self.exist_competitors(competitors):
            raise ReferenceError("Uno o varios de los competidores por los que se realiza la apuesta no están participando en esta ronda")
        self.triplet_bets.append(bettor.bet(amount, competitors))
        self.triplet_pot += amount
        self.register_event("add_composite_bet", (bettor.name, amount, [competitor.name for competitor in competitors]))
        return text.composite_bet(bettor.name, str(amount), [competitor.name for competitor in competitors])


    def proclaim_winner(self, winners):
        """Set the winners of the current round.
        
        Set the winners of the current round preparing the jackpots for distribute the prize.
        
        Arguments:
            winners {List of competitors} -- List of Competitors objects
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
        """Distribute the gains to the bettors.
        
        Updates the bettors money with the prize obtained (is necessary to call proclaim winner function before).
        The house gains the money don't reparted.
        
        Arguments:
            winners {List of one or theree Competitors} -- Competitors objects which are the winners of the current round
        
        Returns:
            String -- Text with the prizes
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
                    if config.ROUND_COINS:
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
                if config.ROUNDS_COINS:
                        prize = int(prize)
                bet.bettor.move_money(prize)
                gains_for_house = round(gains_for_house - prize, 2)
                report += text.report_bets_results(bet.bettor.name, str(prize))
        report += text.report_bets_results("\n\nHouse", str(gains_for_house))
        self.register_event("distribute_prize", report)
        return report

    def load_npcs(self):
        """Loads npcs from npcs.txt file.
        
        Loads npcs so they can bet. The file <npcs.txt> conteins tuples <name;average;variance> that this function reads and used to instance Npc objects.
        """
        try:
            file_handle = open("{}/npcs.txt".format(LOCAL_PATH), "r")
        except:
            file_handle = open("{}/npcs.txt".format(LOCAL_PATH), "w")
            file_handle.close()
            return
        npcs_list = file_handle.readlines()[1:] # Remove first line (headers)
        for npc in npcs_list:
            npc = npc[:-1] # Remove line break
            npc_atributes = npc.split(';')
            self.npcs.append(Npc(npc_atributes[0], int(npc_atributes[1]),
                            float(npc_atributes[2])))
            file_handle.close()


    def generate_padding_bets(self, amount):
        """Generate the indicated amount of bets.
        
        So bets don't be makes only by users, this function generate x (where x = <amount>) bets used the npcs loaded previously.
        
        Arguments:
            amount {Integer} -- Amount of bets makes by npcs
        """
        competitors = list(self.competitors.values())
        for x in range(amount):
            npc = random.choice(self.npcs)
            if len(competitors) == 2: # Only winner bet is possible
                self.register_simple_bet(npc, npc.generate_amount(),
                                        random.choice(competitors), 1)
            else:
                if random.random() < config.SIMPLE_NPCS_BETS:
                    self.register_simple_bet(npc, npc.generate_amount(),
                                        random.choice(competitors),
                                        random.randrange(1,4))
                else:
                    random.shuffle(competitors)
                    self.register_composite_bet(npc, npc.generate_amount(),
                                                [competitors[0], competitors[1],
                                                competitors[2]])



## LOGs 
    def register_event(self, event_type, args):
        """Write log line.
        
        Whenever an event occurs that generates changes in the current round, this function registe that event. A special line is also builded that is written to an .apt file that can later be loaded to execute a round identical to the current one.
        
        Arguments:
            event_type {String} -- Name of the event that has been executed
            args {Truple} -- Tuple with arguments used in the instruction that has been executed
        """
        log_file = open("{}/report/{}.log".format(LOCAL_PATH, str(self.id)), "a+")
        apt_file = open("{}/report/{}.apt".format(LOCAL_PATH, str(self.id)), "a+")
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
            if len(args) == 1: # args = list of winners names
                log_file.write(text.log_proclaim_winner(args[0]))
                apt_file.write("\n{}".format(args[0]))
            else:
                log_file.write(text.log_proclaim_winners(args))
                apt_file.write("\n{},{},{}".format(args[0], args[1], args[2]))
        elif event_type == "distribute_prize":
            log_file.write(text.log_distribute_prize(args)) # args = report to distribute_prize function
        log_file.close()
        apt_file.close()


# APT files
def load_apt(file, npcs_bets, generates_log = False):
    """Loads an apt
    
    A apt file contains the information necessary to simulate a round.
    This can be used to generate a betting round from another application or manually and run in aposteitor after.
    It also allows a previous round to be run again with the apt file generated when that round was run.
    
    Arguments:
        file {String} -- File's name
        npcs_bets {Integer} -- Amount of new npcs bets to generate for execution
    
    Keyword Arguments:
        generates_log {bool} -- If True, a new log file is generated (default: {False})
    
    Raises:
        EnvironmentError -- The file doesn't exist in current directory
        EnvironmentError -- The number of the winners is inconsistent
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
    if(not generates_log):
        log_file = remove("{}/report/{}.log".format(LOCAL_PATH, str(simulation.id)))