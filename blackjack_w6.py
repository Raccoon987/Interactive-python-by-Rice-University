# Mini-project #6 - Blackjack

import simplegui
import random


# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
score = 1

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class - object of this class is a card with caracteristics "suit", "rank"
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    # we "cut" required card from big picture of all cards using its location in array
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class - object of class "Hand" is array(list) of "Card" objects
class Hand:
    def __init__(self):
        self.card_collection = []

    def __str__(self):
        st = "Hand contains"
        for i in self.card_collection:
            st = st + " " + str(i)
        return st

    def add_card(self, card):
        # add a card object to a hand
        self.card_collection.append(card)

    def get_value(self):
        global special_index
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand
        
        # if we get "Ace" then count it as "1" from VALUES dictionary if after adding "1", value is
        # less that 11 - add more "10" and make "special_index" as "1" - so it means that we have 
        # one "Ace" counted as "11". Then if later we went busted, but we have "Ace" counted as "11"
        # and if "-10" will save us - then subtrac 10 from value and decrease counter "special_index"
        
        #it is more complicated than Joe show in video, but it works.
        value = 0
        special_index = 0 
        for i in self.card_collection:
            if (i.get_rank() ==  'A'):
                value = value + VALUES[i.get_rank()]
                if value <= 11:
                    value = value + 10
                    special_index = special_index + 1
            else:  
                if ((value + VALUES[i.get_rank()]) > 21) and ((value + VALUES[i.get_rank()] - 10) <= 21) and (special_index > 0):
                    value = value + VALUES[i.get_rank()] - 10
                    special_index = special_index - 1
                else:
                    value = value + VALUES[i.get_rank()]
                
        return value    
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        # all "i" in "self.card_collection" are objects of "Card" class, so when we
        # apply "draw" method to the "i" object, "draw" method is a method defined
        # in "Card" class
        for i in self.card_collection:
            i.draw(canvas, (pos[0] + (73 + 10) * self.card_collection.index(i), pos[1]))
            
       
# define deck class - big collection(array) of "Card" objects
class Deck:
    def __init__(self):
        # create a Deck object
        self.card_deck = []
        for i in SUITS:
            for j in RANKS:
                self.card_deck.append(str(i) + str(j))
               #self.card_deck.append([i, j])

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card_deck)

    # I take the first card from card_deck, but in video ones takes the last card
    def deal_card(self):
        # deal a card object from the deck
        # self.card_deck consist of "card objects", but appear to be a list of strings "RANKSUIT"
        card = Card(self.card_deck[0][0:1], self.card_deck[0][1:2])
        self.card_deck.pop(0)
        return card
    
    def __str__(self):
        # return a string representing the deck
        st = ""
        for i in self.card_deck:
            st = st + " " + str(i)
        return st



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, players_hand, dealers_hand, string, string_1, score

    # Pressing the "Deal" button in the middle of the round causes the player to 
    # lose the current round
    # if during the play, player decide to re-deal cards before "stand", then player lose.
    # that why score at the begining of the game set to "1". First deal will make it 0 immediately
    if in_play != True:
        score = score - 1
        
    in_play = False
    # "strings" are information displayed on canvas
    string = ""
    string_1 = "HIT OR STAND?"
    
    deck = Deck()
    deck.shuffle()
    #create "players_hand" and "dealers_hand" - 2 objects of the same class Hand
    players_hand = Hand()
    dealers_hand = Hand()
    # deal card - both hands get a card and "deck" loose 2 cards
    players_hand.add_card(deck.deal_card())
    dealers_hand.add_card(deck.deal_card())
    
    players_hand.add_card(deck.deal_card())
    dealers_hand.add_card(deck.deal_card())
    # you can check deck shuffling
    print players_hand
    print dealers_hand
    print deck
    print
    

def hit():
    global string, string_1
    # add one more card to player
    if (players_hand.get_value()) <= 21:
        players_hand.add_card(deck.deal_card())
        #print players_hand
        if (players_hand.get_value()) > 21:
            #string = "YOU WENT BUSTED"
            stand()
            string_1 = "NEW DEAL?"
               
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global string, in_play, string_1, score
    #in_play keeps track of whether the player's hand is still being played
    in_play = True
    
    if (players_hand.get_value()) > 21:
        string = "YOU BUSTED AND LOSE"
        score = score - 1
                
        #while (dealers_hand.get_value()) < 17:
        #    dealers_hand.add_card(deck.deal_card())
            #print dealers_hand
        
        #if dealers_hand.get_value() > 21:
        #    string = "dealer has also busted" + " Tie!"
            
            #print "dealer has busted also"  
        #else:    
        #    string = "dealer wins!"
            
            
    else:
        while (dealers_hand.get_value()) < 17:
            dealers_hand.add_card(deck.deal_card())
            #print dealers_hand
        if dealers_hand.get_value() > 21:
            string = "DEALER BUSTED YOU WIN"
            score = score + 1            
        else:
            if dealers_hand.get_value() < players_hand.get_value():
                string = "YOU WIN"
                score = score + 1                
            elif dealers_hand.get_value() > players_hand.get_value():
                string = "YOU LOSE"
                score = score - 1                   
            else:
                string = "YOU LOSE"
                score = score - 1
        
        string_1 = "NEW DEAL?"        
                    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", (30, 80), 50, "Red")
    canvas.draw_text("DEALER", (30, 190), 30, "Red")
    canvas.draw_text("PLAYER", (30, 430), 30, "Red")
    canvas.draw_text(string, (230, 190), 27, "Black")
    canvas.draw_text(string_1, (230, 430), 27, "Black")
    canvas.draw_text("SCORE: " + str(score), (380, 80), 35, "Red")
    players_hand.draw(canvas, [30, 600 - 30 - 98])
    if in_play == False:
        dealers_hand.draw(canvas, [30, 230])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [30 + 73 + 10 + 73/2, 230 + 98/2], (73, 98))
    else:
        dealers_hand.draw(canvas, [30, 230])
        
   
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
