import random


class Card():
    """
    Class that will be used inside the Deck class
    """
    def __init__(self, card_type, name, value, faceUp=True):
        self.card_type = card_type
        self.name = name
        self.value = value
        self.faceUp = faceUp

class Deck():
    """
    Creates a deck of card with class Card

    shuffle_pick: takes out one random card of the deck and removes it
        returns the random card
    """
    name = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
    card_type = ['hearts','clubs','diamonds','spades']
    def __init__(self):
        self.cards = {'hearts':{}, 'clubs':{}, 'diamonds':{}, 'spades':{}}
        for i in range(len(Deck.card_type)):
            for j in range(len(Deck.name)):
                if j==0:
                    self.cards[Deck.card_type[i]][Deck.name[j]] = Card(Deck.card_type[i], Deck.name[j], [1,11], True)
                elif j<10:
                    self.cards[Deck.card_type[i]][Deck.name[j]] = Card(Deck.card_type[i], Deck.name[j], [j+1], True)
                else:
                    self.cards[Deck.card_type[i]][Deck.name[j]] = Card(Deck.card_type[i], Deck.name[j], [10], True)

    def __str__(self):
        all_cards = ''
        for i in self.cards:
            for j in self.cards[i]:
                all_cards+=j+' of '+i+'\n'
        return all_cards

    def shuffle_pick(self):
        remaining_card_type_keys = [key for key in self.cards.keys()]
        random_card_type = random.randint(0,len(remaining_card_type_keys)-1)

        remaining_card_keys = [name for name in self.cards[remaining_card_type_keys[random_card_type]].keys()]
        random_card = random.randint(0,len(remaining_card_keys)-1)

        selected_card = self.cards[remaining_card_type_keys[random_card_type]][remaining_card_keys[random_card]]
        del self.cards[remaining_card_type_keys[random_card_type]][remaining_card_keys[random_card]]
        if len(self.cards[remaining_card_type_keys[random_card_type]])==0:
            del self.cards[remaining_card_type_keys[random_card_type]]
        return selected_card

class Player():
    """
    Player class creates a player to play black Jack

    hit: picks a random card from the provided deck and gives it to the player
        This removes the card from the deck
    """
    def __init__(self, name, balance, cards):
        self.name = name
        self.balance = balance
        self.score = 0
        self.cards = cards
        self.hit_state = True
        self.bust = False

    def __str__(self):
        all_cards = ''
        for i in self.cards:
            for j in self.cards[i]:
                all_cards+=j+' of '+i+'\n'
        return all_cards

    def hit(self, deck):
        selected_card = deck.shuffle_pick()
        self.cards.append(selected_card)

        # get player score
        temp_score = 0
        temp_multi_score=[]
        for i in self.cards:
            if len(i.value)==1:
                temp_score += i.value[0]
            else:
                temp_multi_score.append(i.value)

        # go through all the possiblities or combination score based on how many
            # cards have double possible values
            # (kind of too complex, but is very general if the max points is not
            # 21 anymore)
        multi_score = []
        counter=0
        possible_value = [1,11]
        binary_counter = bin(counter).split('0b')[1]
        while len(binary_counter)<=len(temp_multi_score):
            binary_counter = '0'*(len(temp_multi_score)-len(binary_counter))+binary_counter
            multi_score.append(sum([possible_value[int(x)] for x in binary_counter])+temp_score)
            counter+=1
            binary_counter = bin(counter).split('0b')[1]

        if len(multi_score)==0:
            self.score = temp_score
            if temp_score>21:
                self.bust=True
        else:
            best_score = 0
            for i in multi_score:
                if i>21 and i==multi_score[0]:
                    self.bust = True
                    self.score = i
                if i<=21 and i>best_score:
                    best_score = i
                    self.score=best_score
            if best_score>21:
                self.bust = True

    def stay(self):
        self.hit_state = False


def winner_display(winner):

    winner_string = winner + ' WINS!!!'

    space = 50

    spaces_between_title = (space-len(winner_string)-2)/2
    print('\n'*5)
    print('#'*space)
    print('#' + ' '*(space-2) + '#')
    print('#' + ' '*round(spaces_between_title-0.01) + winner_string + ' '*round(spaces_between_title+0.1) + '#')
    print('#' + ' '*(space-2) + '#')
    print('#'*space)



def display_board(computer, player, computer_1st_hidden=True):
    print('\n'*5)
    print('Computer house: \n')
    if computer_1st_hidden:
        first_string = '(first card hidden)'
        second_string = '?'
        print(first_string + ' '*(25-len(first_string)) + '?'+ ' '*(9-len(second_string)) +'points')

        first_string = f'{computer.cards[1].name} of {computer.cards[1].card_type}'
        second_string = f'{computer.cards[1].value}'
        print(first_string + ' '*(25-len(first_string)) + second_string + ' '*(9-len(second_string)) +'points')
    else:
        for i in range(len(computer.cards)):
            first_string = f'{computer.cards[i].name} of {computer.cards[i].card_type}'
            second_string = f'{computer.cards[i].value}'
            print(first_string + ' '*(25-len(first_string)) + second_string + ' '*(9-len(second_string)) +'points')
        first_string = 'Best_score'
        second_string = f'{computer.score}'
        print('\n'+first_string + ' '*(25-len(first_string)) + second_string + ' '*(9-len(second_string)) + 'points')

    print('\n'*2)
    print('-'*30)
    print('\n'*2)

    print('Your cards: \n')
    for i in range(len(player.cards)):
        first_string = f'{player.cards[i].name} of {player.cards[i].card_type}'
        second_string = f'{player.cards[i].value}'
        print(first_string + ' '*(25-len(first_string)) + second_string + ' '*(9-len(second_string)) +'points')
    first_string = 'Best_score'
    second_string = f'{player.score}'
    print('\n'+first_string + ' '*(25-len(first_string)) + second_string + ' '*(9-len(second_string)) + 'points')

def verify_bet(player):

    while True:
        try:
            bet = int(input(f'What amount do you bet for this round? (you have {player.balance} dollars) '))
        except:
            print('Enter a valid number')
        else:
            if bet>player.balance:
                print('This amount exceeds your balance')
            else:
                return bet

def game(computer, player, bet):

    while player.hit_state:

        if player.score == 21:
            player.balance += bet
            return winner_display(player.name)
        print('\n'*5)
        hit_again = input('Do you want to hit (h) or stay (s)? ')
        if hit_again == 'h':
            player.hit(deck)
            display_board(computer,player)
            if player.bust:
                print('\n21 WAS BUSTED! YOU LOST.')
                player.balance -= bet
                return winner_display(computer.name)
            if player.score == 21:
                player.balance += bet
                return winner_display(player.name)

        elif hit_again == 's':
            player.stay()

    print('All cards revealed!')
    display_board(computer, player, False)

    player_wait = input('Hit any key to continue')

    if computer.score == 21:
        player.balance -= bet
        return winner_display(computer.name)

    while computer.score <= player.score:
        computer.hit(deck)
        display_board(computer, player, False)
        if computer.score>21:
            print('\nCOMPUTER HOUSE BUSTED! YOU WON!')
            player.balance += bet
            return winner_display(player.name)
        if computer.score>player.score:
            player.balance -= bet
            return winner_display(computer.name)
        player_wait = input('Hit any key to continue')

    player.balance -= bet
    return winner_display(computer.name)

if __name__ == '__main__':

    print('\n'*100)
    player_name = input('What is your name: ')
    player_money = int(input('What amount do you have? '))
    comuter_name = input('What name do you want to give to the computer house? ')

    player1 = Player(name=player_name, balance=player_money, cards=[])
    computer = Player(name=comuter_name, balance=0, cards=[])

    again = True
    while again and player1.balance!=0:

        bet = verify_bet(player1)

        deck = Deck()

        computer.hit(deck)
        computer.hit(deck)
        computer.cards[0].faceUp=False

        player1.hit(deck)
        player1.hit(deck)

        display_board(computer, player1)

        game(computer, player1, bet)

        print('\n'*5)
        again_ask = input('Do you still want to play? (y or n) ')
        if again_ask=='n':
            print(f'your new balance is {player1.balance}')
            again=False
        print('\n'*100)

        player1.cards = []
        player1.bust = False
        player1.hit_state = True
        computer.cards = []
    if player1.balance==0:
        print('\nNot enough funds. Balance to 0!')
