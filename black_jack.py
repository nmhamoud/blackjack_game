'''
This script simulates a simple version of the Black Jack game
'''
import random
# a player:
#     - take action: stand or hit
#     - pick betting amount
#     - track total money
#     - alert of wins, losses or busts
# cards:
#     - values
#     - suits
# winnings:
#     - player gets 21 (Black Jack)
#     - player gets higher than dealer
#     - dealer exceeds 21 (busted)
# procedure:
#     - player receive 2 cards
#     - dealer shows 1 card only
#     - player hits or stands
#     - after standing the dealer play until his card values exceed 16

class Card():
    def __init__(self, face, value, suit):
        self.face = face
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.suit}_{self.face}"

class Player():

    def __init__(self, name, hand=[], last_move=False, hide_score=False):
        self.name = name
        self.hand = hand
        self.last_move = last_move
        self.hide_score = hide_score

    def update_hand(self, cards):
        self.hand = cards

    def update_last_move(self, last_move):
        self.last_move = last_move

class Computer(Player):
    def __init__(self, name='Computer', hand=[], last_move=False, hide_score=True):
        # super(Computer, self).__init__(name=name, hide_score=hide_score)
        super(Computer, self).__init__(name=name, hand=hand, last_move=last_move, hide_score=hide_score)
        self.score = 0

    def make_move(self):
        deal(self)

class Human(Player):
    def __init__(self, name='Player1', total_money=100, hand=[], last_move=False, hide_score=False):
        # super(Human, self).__init__(name=name)
        super(Human, self).__init__(name=name, hand=hand, last_move=last_move, hide_score=hide_score)
        self.score = 0
        self.total_money = total_money
        self.bet_amount = 0

    def bet(self):
        while True:
            if self.total_money > 0:
                print(f"Your balance is ${self.total_money}")
                while True:
                    try:
                        self.bet_amount = int(input("How much is your bet? "))
                        break
                    except ValueError:
                        print("Please inter an integer!")
                if self.bet_amount <= self.total_money:
                    self.total_money -= self.bet_amount
                    break
                else:
                    print(f"Your bet is higher than your available fund of ${self.total_money}!")
            else:
                print("You exauhsted all your funds, buddy!")
                if input("How about I take your car for $1000?(y/n) ")=='y':
                    self.total_money = 1000
                else:
                    print("Okay, get out of here!")
                    exit()
        return

    def make_move(self):
        if input('\nhit or stand? ').lower()== "hit":
            deal(self)
        else:
            self.update_last_move(True)
            print('* STAND *')

def play():
    print('*'*20 + "\n*" + " "*3 + "GAME STARTS " + " "*3 + "*\n" + '*'*20)
    player1.bet()
    # initial moves
    for pl in [computer, player1]:
        deal(pl)
        pl.score = compute_score(pl)
        display_side(pl)
    # next plaeyer moves
    while not player1.last_move:
        player1.make_move()
        player1.score = compute_score(player1)
        if check_blackjack(player1):
            # display and reveal 2nd card of computer
            display_table()
            if check_blackjack(computer):
                print(f"Push! YOU GET YOUR ${player1.bet_amount} BACK")
                player1.total_money += player1.bet_amount
            else:
                print(f"BLACKJACK! YOU WON ${player1.bet_amount*2}!")
                player1.total_money += player1.bet_amount*2
            play_again()
        elif check_bust(player1):
            # display and reveal 2nd card of computer
            display_table()
            if check_bust(computer):
                print(f"Push! YOU GET YOUR ${player1.bet_amount} BACK")
                player1.total_money += player1.bet_amount
            else:
                print(f"BUST! YOU LOST ${player1.bet_amount}!")
            play_again()
        else:
            display_table(True)
            pass
    # next computer moves
    while not computer.last_move:
        if max(computer.score) < 16:
            computer.make_move()
        else:
            computer.update_last_move(True)
        computer.score = compute_score(computer)
        if check_blackjack(computer):
            # display and reveal 2nd card of computer
            display_table()
            print(f"YOU LOST ${player1.bet_amount}!")
            play_again()

        elif check_bust(computer):
            # display and reveal 2nd card of computer
            display_table()
            print(f"YOU WON ${player1.bet_amount*2}!")
            player1.total_money += player1.bet_amount*2
            play_again()
        else:
            pass
    compare_scores()

def deal(player):
    global deck
    if player.hand == []:
        if len(deck) <= 2:
            print("New Deck Coming!")
            deck = create_deck()
        selected_cards = random.sample(deck, 2)
        deck = list(set(deck) - set(selected_cards))
        player.update_hand(selected_cards + player.hand)
    else:
        if len(deck) <= 1:
            print("New Deck Coming!")
            deck = create_deck()
        selected_card = random.sample(deck, 1)
        deck = list(set(deck) - set(selected_card)) # TODO: doesn't work for >1 deck
        player.update_hand(selected_card + player.hand)

    # SCORES
    # computer.score = compute_score(computer)
    # player1.score = compute_score(player1)

    # CHECK WINNING/LOSING
    # display_side(player)
    # check_score()

def create_deck(num=1):
    suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
    face_val = {'Ace':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
                '10':10, 'Jack':10, 'Queen':10, 'King':10}
    deck = [Card(key, value, suit) for suit in suits for key, value in face_val.items()]
    random.shuffle(deck)
    return deck*num

def compute_score(player):
    score = [sum(card.value for card in player.hand)]
    for card in player.hand:
        if "Ace" in card.face:
            score.append(score[0] + 10)
            break
    return score

def check_blackjack(player):
    # check BLACKJACK
    if 21 in player.score:
        return True

def check_bust(player):
    # check BLACKJACK
    if min(player.score) > 21:
        return True

def compare_scores():    # check after computer's score > 16
    if any(s > max(player1.score) for s in computer.score): # TODO:
        display_table()
        print(f"YOU LOST ${player1.bet_amount}!")
        play_again()
    elif any(s > max(computer.score) for s in player1.score): # TODO:
        display_table()
        print(f"YOU WON ${player1.bet_amount*2}!")
        player1.total_money += player1.bet_amount*2
        play_again()
    else:
        display_table()
        print(f"Push! YOU GET YOUR ${player1.bet_amount} BACK")
        player1.total_money += player1.bet_amount

'''def check_score(computer_last_move=False):
    # check BLACKJACK
    if 21 in computer.score and 21 in player1.score:
        print(f"Push! YOU GET YOUR ${player1.bet_amount} BACK")
        player1.total_money += player1.bet_amount
        play_again()
    elif 21 in computer.score and 21 not in player1.score:
        print(f"YOU LOST ${player1.bet_amount}!")
        play_again()
    elif 21 not in computer.score and 21 in player1.score:
        print(f"BLACKJACK! YOU WON ${player1.bet_amount*2}!")
        player1.total_money += player1.bet_amount*2
        play_again()
    # check BUST
    elif any(s < 21 for s in computer.score) and min(player1.score) > 21:
        print(f"BUST! YOU LOST ${player1.bet_amount}!")
        play_again()
    elif min(computer.score) > 21 and any(s < 21 for s in player1.score):
        print(f"YOU WON ${player1.bet_amount*2}!")
        player1.total_money += player1.bet_amount*2
        play_again()
    else:
        pass
    # check after computer's score > 16
    if computer_last_move:
        if any(s > max(player1.score) for s in computer.score): # TODO:
            print(f"YOU LOST ${player1.bet_amount}!")
            play_again()
        elif any(s > max(computer.score) for s in player1.score): # TODO:
            print(f"YOU WON ${player1.bet_amount*2}!")
            player1.total_money += player1.bet_amount*2
            play_again()
        else:
            print(f"Push! YOU GET YOUR ${player1.bet_amount} BACK")
            player1.total_money += player1.bet_amount
'''
def display_side(player):
    if len(player.name)%2==0:
        pl = player.name.upper()
    else:
        pl = player.name.upper() + " "
    print()
    frame = 20*"*"
    pad = int((18-len(player.name))/2)*" "
    print(frame)
    print("*" + pad + f"{pl}" + pad + "*")
    print(frame)
    if player.hide_score:
        print(f"Score: {player.score[0]-player.hand[0].value}")
        for i, card in enumerate(player.hand):
            if i==0:
                print(f"Card #{i+1}:  XXXXXXXXX")
            else:
                print(f"Card #{i+1}: ", card)
    else:
        print(f"Score: {player.score}")
        for i, card in enumerate(player.hand):
            print(f"Card #{i+1}: ", card)

def display_table(hide=False):
    computer.hide_score = hide
    display_side(computer)
    display_side(player1)

def play_again():
    computer.hide_score = True
    while True:
        again = input("Play again?(y/n):  ").lower()
        if again == "y":
            cards = []
            for pl in [computer, player1]:
                pl.update_hand(cards)
                pl.update_last_move(False)
            play()
        elif again == "n":
            print("Come again. Goodbye!")
            exit()
        else:
            print("Wrong entry!")


# INTRO TO THE GAME
# def start_game():
print('*'*30)
print('*'+' '*4 + 'WELCOME TO BLACKJACK' + ' '*4 + '*')
print('*'*30)
print('\nThe rules of the game:\n\nWELL, WHY WOULD YOU PLAY IF YOU DO NOT KNOW THE RULES!\n')
print("Let's play!\n")

# setup player(s)
computer = Computer()
name_input = input('What is your name? ')
while True:
    try:
        balance_input = int(input("How much money do you have? ") or 100)
        break
    except ValueError:
        print("Please inter an integer!")

player1 = Human(name=name_input, total_money=balance_input)
print(f"Hello, {player1.name}. Let's see if you can keep your account from going to zero!")

# SETUP DECKS
deck = create_deck()

# PLAY
play()

# if __name__=="__main__":
#     start_game()
