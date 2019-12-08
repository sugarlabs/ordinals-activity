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

import pygame


class Card():
    def __init__(self, color, x, y, sideLen, text):
        pygame.init()
        self.color = color
        self.x = x
        self.y = y
        self.sideLen = sideLen
        self.text = text

    def draw(self, screen):
        bounds = (self.x, self.y, self.sideLen, self.sideLen)
        pygame.draw.rect(screen, self.color, bounds, 0)
        fontSz = int(self.sideLen*0.7)
        if(len(self.text) > 2):
            fontSz = int(fontSz*0.75)
        font = pygame.font.SysFont('arial', fontSz)
        text = font.render(self.text, 1, (0, 0, 0))
        screen.blit(text, (self.x + (self.sideLen/2 - text.get_width()/2),
                    self.y + (self.sideLen/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.sideLen:
            if pos[1] > self.y and pos[1] < self.y + self.sideLen:
                return True
        return False

    # Get card in rectangle format for dirty updating
    def getRect(self):
        return(self.x, self.y, self.sideLen, self.sideLen)
