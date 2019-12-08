# Copyright (C) 2019, Sugar Labs
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from random import randrange


class Deck:
    deck = []

    def __init__(self):
        if len(self.deck) == 0:
            for i in range(50):
                self.deck.append(i + 1)
        else:
            for i in range(50):
                self.deck[i] = i + 1
        self.shuffle()

    def shuffle(self):
        for i in range(50):
            self.swap(i, randrange(50))

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
