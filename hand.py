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

    def countPoints(self):
        points = 0
        for i in range(1, len(self.hand)):
            if(self.hand[i] > self.hand[i-1]):
                points += 5
            else:
                break

        return points
