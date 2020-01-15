import random
import math
import text

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
        if (self.money - amount) >= 0:
            self.money = self.money - amount
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
        self.move_money(amount)
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

class Pnj(Player): # Para que no explote
    def __init__(self, name, average, variance, money = float("inf")):
        super(Pnj, self).__init__(name, money)
        self.average = average
        self.variance = variance

    def generate_amount(self):
        """
        All pngs generating their amount for bet with a normal function.
        """
        return math.ceil(random.normalvariate(self.average, self.variance))

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
        self.effective_amount = self.amount * 1.0
        self.type = 1

class BetPlaced(Bet):
    def __init__(self, bettor, amount):
        super(BetPlaced, self).__init__(bettor, amount)
        self.effective_amount = self.amount * 0.7
        self.type = 2

class BetThird(Bet):
    def __init__(self, bettor, amount):
        super(BetThird, self).__init__(bettor, amount)
        self.effective_amount = self.amount * 0.4
        self.type = 3

class BetTriplet(Bet):
    def __init__(self, bettor, amount, triplet):
        super(BetTriplet, self).__init__(bettor, amount)
        self.triplet = triplet


class Round():
    def __init__(self, competitors = []):
        self.bettors = [] # Creo que no vale para nada
        self.pnjs = []
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


    def add_competitors(self, competitors): ## Comprobar si se puede meter un participante en blanco o una lista
        """
        Adds competitors to list of the round.
        Each competitor must have a different name and cannot be added more than once.
        
        :param      competitors:  The competitors
        :type       competitors:  List of Competitor
        """
        for competitor in competitors:
            if self.exist_competitors([competitor]):
                raise NameError("El competidor {}ya está incluido en la ronda o ya existe un competidor con el mismo nombre".format(competitor.name))
            self.competitors[competitor.name] = competitor



    def register_simple_bet(self, bettor, amount, competitor, bet_type):
        """
        Build a simple bet and registres it in the pool of bets of the round.
        
        :param      bettor:      The bettor
        :type       bettor:      Player
        :param      amount:      The amount
        :type       amount:      Double
        :param      bet_type:    The bet_type
        :type       bet_type:    Integer 1-3
        :param      competitors: The competitor
        :type       competitors: Competitor
        """
        if not self.exist_competitors([competitor]):
            raise ReferenceError("El competidor por el que se realiza la apuesta no está participando en esta ronda")
        competitor.bets.append(bettor.bet(amount, bet_type))
        self.pot += amount
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
        """
        if not self.exist_competitors(competitors):
            raise ReferenceError("Uno o varios de los competidores por los que se realiza la apuesta no están participando en esta ronda")
        self.triplet_bets.append(bettor.bet(amount, competitors))
        self.triplet_pot += amount
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
            


    def distribute_prize(self, winners):
        """
        Updates the bettors money with the prize obtained.
        The house gains the money don't reparted. Don't implemented yet.
        
        :param      winners:  The winners
        :type       winners:  List of one or three Competitors
        """
        report = text.total_report
        # Simple bets
        proportion_simple_bets = self.pot/self.jackpot if self.jackpot >= 1 else 0
        winner_index = 0
        while winner_index < len(winners):
            report += text.report_bet_for(winners[winner_index].name)
            for bet in winners[winner_index].bets:
                if bet.type > winner_index:
                    prize = math.floor(bet.effective_amount*proportion_simple_bets*100)/100
                    bet.bettor.money += prize
                    report += text.report_bets_results(bet.bettor.name, str(prize))
            winner_index += 1
        # Triplet bets
        proportion_triplet_bets = self.triplet_pot/self.triplet_jackpot if self.triplet_jackpot >= 1 else 0
        if len(winners) == 3:
            for bet in self.triplet_winner_bets:
                report += text.report_bet_for(bet.bettor.name)
                prize = math.floor(bet.effective_amount*proportion_triplet_bets*100)/100
                bet.bettor.money += prize
                report += text.report_bets_results(bet.bettor.name, str(prize))

        return report

    def loadPNJs(self):
        """
        Loads pnjs so they can bet.
        """
        try:
            fileHandle = open("pnjs.txt", "r")
        except:     
            fileHandle = open("pnjs.txt", "w")
            fileHandle.close()
            return
        pnjs_list = fileHandle.readlines()[1:]# Remove first line (headers)
        for pnj in pnjs_list:
            pnj = pnj[:-1] # Remove line break
            pnj_atributes = pnj.split(';')
            self.pnjs.append(Pnj(pnj_atributes[0], int(pnj_atributes[1]), float(pnj_atributes[2])))
            fileHandle.close()


    def generate_padding_bets(self, amount):
        """
        Generate the indicated amount of bets.
        
        :param      amount:  The amount
        :type       amount:  Int
        """
        competitors = self.competitors.values()
        for x in range(1,amount):
            pnj = random.choice(self.pnjs)
            self.register_bet(pnj, pnj.generate_amount(), random.choice(competitors))