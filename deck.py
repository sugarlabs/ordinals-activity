# Taken from https://github.com/walterbender/ordinals.activity
from random import randrange

class Deck:
    deck = []

    def __init__(self):
        if len(self.deck) == 0:
            for i in range(60):
                self.deck.append(i + 1)
        else:
            for i in range(60):
                self.deck[i] = i + 1
        self.shuffle()

    def shuffle(self):
        for i in range(60):
            self.swap(i, randrange(60))

    def swap(self, i, j):
        k = self.deck[i]
        self.deck[i] = self.deck[j]
        self.deck[j] = k

    def deal(self, hands):
        for hand in hands:
            for i in range(10):
                hand.hand.append(self.deck.pop())

    def draw(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        return None

    def empty(self):
        if len(self.deck) == 0:
            return True
        return False