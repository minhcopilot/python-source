# suit laf co ro chuon bich,
# value la 2,3,4,5,..
class Card():
    def __init__(self,suit,value):
        self.suit = suit
        self.value = value
    
class Deck():
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for value in range(1,14):
                card = Card(suit,value)
                self.cards.remove(card)

# Tao 1 class Deck voi 52 la vai duoc tao ra tu class o tren. Deck se xao 52 la va loai 1 la ra khoi Deck
                