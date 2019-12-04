# Taken from https://github.com/walterbender/ordinals.activity

class Hand:
    hand = []

    def __init__(self):
        self.hand = []

    def show_hand(self):
        for i in range(len(self.hand)):
            print('%2d: %d' % (i * 5 + 5, self.hand[i]))

    def test_hand(self):
        for i in range(len(self.hand)):
            if i == 0:
                continue
            if self.hand[i] < self.hand[i - 1]:
                return False
        return True

    def place(self, n):
        discard = n
        i = int(n / 5.5)
        if i > 9:
            i = 9
        if abs(i * 5.5 + 5.5 - n) < abs(i * 5.5 + 5.5 - self.hand[i]):
            discard = self.hand[i]
            self.hand[i] = n
        return discard

    def replace(self, n, nn):
        for i in range(len(self.hand)):
            if self.hand[i] == n:
                self.hand[i] = nn
                return n
        return nn
