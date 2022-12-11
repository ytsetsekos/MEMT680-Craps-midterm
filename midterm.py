# -*- coding: utf-8 -*-
"""
Yanni Tsetsekos

CRAPS Midterm exam
"""
import random

class Dice: # holds current value of two dice 
    def __init__(self):
        self.diceA = 0
        self.diceB = 0
    def roll(self):
         self.diceA = random.randint(1, 6)
         self.diceB = random.randint(1, 6)
     
class Table(Dice): # inherits Dice class and determines if point has been set in game
    def __init__(self):
        super().__init__() # inheritance call to parent class
        self.comeout = True # first roll is always a comeout roll
        self.point = False # set point starts as false
        self.point_val = 0 # point value starts at 0
    def resetTable(self):
        self.point = False # Removes point from table
        self.point_val = 0 # point value goes back to 0 for new round
        self.oddsPlaced = False # odds returns to false state
        
class Player(Table):
    def __init__(self):
        super().__init__() # the use of super() makes this class inheritable from the Table class
        self.name = input('What is your name?  ') # gets name from player via input
        self.isShooter = False # player starts as not shooter until non-zero bets are placed
        
        # the following try-except and while loop ensure the user bankroll input is a positive integer
        try:
            self.bankroll = int(input('How much money in dollars do you have on the table? Enter a positive integer  ')) # gets bankroll from player via input, as an integer
        except ValueError: # if user enters a non-integer, this line catches that error 
            print("Please make sure you're entering an integer (no decimals/cents)")
        while type(self.bankroll) != int or self.bankroll <= 0:
            self.bankroll = int(input('How much money do you have on the table? Please enter a positive dollar amount (no cents)  ')) # gets bankroll from player via input, as an integer
        
        self.startBankroll = int(self.bankroll) # to compare how much is gained/lost at end of game
        
class bets(Player):
    def __init__(self):
        super().__init__() # makes bets class inheritable from the player class
        
        self.currentBets = { # tracking all possible and current bets and how many have been made
                                    "pass line": 0,
                                    "do not pass": 0,
                                    "odds_bet": 0
                                    }
        
    def insufficient_funds(self,bet_amount):
        print(self.name+" has insufficient funds to place a bet. Bet amount:")
        newBet = int(input('Player, please place another valid integer bet:  '))
        while type(newBet) != int or newBet <= 0:
            newBet = int(input('Please enter a valid bet amount:  ')) # keeps asking player for valid bet
        return newBet
        
    def pass_line(self): # make pass line bet
        if self.point == False: # can only make bet if point has not been established
            bet_amount = input("How much would you like to bet on a pass line?") # get bet amount from player
            if self.bankroll - bet_amount < 0: # checks if player has enough to make the bet
                bet_amount = self.insufficient_funds(self) # returns a new bet that the player can afford
            
            self.currentBets['pass_line'] = self.currentBets['pass_line'] + bet_amount # update bet tracking dictionary
            self.bankroll = self.bankroll - bet_amount # update bankroll
            
            print(self.name, " has placed a bet on the pass line for ", str(bet_amount)) # announces bet to "the table"
            print(self.currentBets) # print all current bets. make better later
            
        else: # point has already been established
            print("Point has already been set, pass line bet can't be placed")

    def do_not_pass(self): # make a do not pass bet
        if self.point == False: # can only make bet if point has not been established
            bet_amount = input("How much would you like to bet on the do not pass line?") # get bet amount from player
            if self.bankroll - bet_amount < 0: # checks if player has enough to make the bet
                bet_amount = self.insufficient_funds(self) # returns a new bet that the player can afford
            
            self.currentBets['do not pass'] = self.currentBets['do not pass'] + bet_amount # update bet tracking dictionary
            self.bankroll = self.bankroll - bet_amount # update bankroll
            
            print([self.name, " has placed a bet on the do not pass for ", str(bet_amount)]) # announces bet to "the table"
            print(self.currentBets) # print all current bets. make better later
            
        else: # point has already been established
            print("Point has already been set, do not pass line bet can't be placed")
    
    def betting_turn(self): # starts the betting phase
        betting = str.lower(input("Would you like to place a bet? Please enter yes or no:  ")) # casting input to lowercase to make case insensitive
        while betting not in ['yes', 'y', 'no','n']: # if response is not a yes/no, then keep asking until 
            print("Please enter a valid response: 'yes' or 'no'")
            betting = str.lower(input("Would you like to place a bet?  "))
        if betting == 'no' or betting == 'n':
            print(self.name, " will not place a bet for this round")
        else:
            betLocation = str.lower(input("Where would you like to place a bet? 'Pass Line', 'Do Not Pass Line', 'Odds Bet' ?  "))
            while betLocation not in ['pass line', 'do not pass line', 'odds bet']: # if response does not match the betting locations, keep asking
                print("Please enter a valid response: 'Pass Line', 'Do Not Pass Line', or 'Odds Bet'")
                betLocation = str.lower(input("Where would you like to place a bet? 'Pass Line', 'Do Not Pass Line', 'Odds Bet' ?  "))
                
            if betLocation == 'pass line':
                self.pass_line() # places a bet on the pass line
            elif betLocation == 'do not pass line':
                self.do_not_pass() # places a bet on the do not pass line
            elif betLocation == 'Odds Bet':
                self.oddsPlaced() # places an odds bet
            
    def ingest_bet(self):
        try:
            bet_prompt = int(input("Please place a bet, enter a positive integer value:  ")) # asks user for bet
        except ValueError: # if user enters a non-integer, this line catches that error 
            print("Please make sure you're entering an integer (no decimals/cents)")
        while type(bet_prompt) != int or bet_prompt <= 0:  # checks that entered bet is an integer and is greater than 0
            bet_prompt = int(input('Enter your bet here, enter a positive integer value: ')) # this while loop keeps prompting player for acceptable bet input
        
        while self.bankroll < bet_prompt: # player can only bet as much money as they have
            print('Your current bankroll is ',self.bankroll, ". You can wager up to this amount") # prints how much they currently have
            bet_prompt = int(input('Enter your bet here, make sure to wager less than what your bankroll is: ')) # this while loop keeps prompting player for acceptable bet input
        
        return bet_prompt
    
    def printBets(self): 
        print("Current bets:")
        print("Bet Type:\tBet Amount:\n") # listing the bet types and amounts
        for key,value in self.currentBets.items():
            print(f"{key}\t${value}") # prints all the bet amounts
        if self.point:
            print("The point has been set to: ", self.point_val)
        print('Current bankroll is ',self.bankroll) # prints how much they currently have
        
player = bets() # creates a new player to play the game with
player.betting_turn() # lets player begin placing bets