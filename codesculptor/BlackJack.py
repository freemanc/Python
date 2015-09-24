# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            # print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []
        self.value = 0

    def __str__(self):
        string = 'Hand contains'
        for card in self.card_list:
            string += (' ' + card.get_suit() + card.get_rank())
        return string

    def add_card(self, card):
        self.card_list.append(card)

    def get_value(self):
        self.value = 0
        have_ace = False
        for card in self.card_list:
            if card.get_rank() == 'A':
                have_ace = True
            self.value += VALUES[card.get_rank()]
        if have_ace and self.value + 10 <= 21:
            self.value += 10
        return self.value
   
    def draw(self, canvas, pos):
        for card in self.card_list:
            card.draw(canvas, pos)
            pos[0] += 100
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.card_list = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card_list)

    def deal_card(self):
        return self.card_list.pop()
    
    def __str__(self):
        string = 'Deck contains'
        for card in self.card_list:
            string += (' ' + card.get_suit() + card.get_rank())
        return string



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, score
    
    if in_play:
        score -= 10
        outcome = 'You lose... Click Deal again to start a new game.'
        in_play = False
        return None
    
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    if player_hand.get_value() < 21:
        outcome = 'Hit or stand?'
    
    # print 'Dealer' + str(dealer_hand)
    # print 'Player' + str(player_hand)
    
    in_play = True

def hit():
    global in_play, outcome, score
    
    # if the hand is in play, hit the player
    if in_play:
        if player_hand.get_value() < 21:
            player_hand.add_card(deck.deal_card())
            # print 'Player' + str(player_hand)
            if player_hand.get_value() < 21:
                outcome = 'Hit or stand?'
            elif player_hand.get_value() == 21:
                outcome = 'You are 21!  ... Click Stand button'
            else:
                # if busted, assign a message to outcome, update in_play and score
                score -= 10
                outcome = 'You have busted... New deal?'
                in_play = False
       
       
def stand():
    global in_play, outcome, score
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            # print 'Dealer' + str(dealer_hand)

        # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            score += 10
            outcome = 'Dealer has busted... New deal?'
            in_play = False
        elif dealer_hand.get_value() < player_hand.get_value():
            score += 10
            outcome = 'You wins! ... New deal?'
            in_play = False
        else:
            score -= 10
            outcome = 'Dealer wins... New deal?'
            in_play = False

# draw handler    
def draw(canvas):
    canvas.draw_text('Blackjack', [30, 30], 30, 'Black')
    canvas.draw_text('Your score: ' + str(score), [300, 30], 30, 'Black')
    canvas.draw_text(outcome, [150, 200], 20, 'Blue')
    player_hand.draw(canvas, [50, 450])
    dealer_hand.draw(canvas, [50, 50])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + 36, 50 + 48], CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric