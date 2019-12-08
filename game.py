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

#!/usr/bin/python3
import pygame
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from deck import Deck
from hand import Hand
from card import Card
from colors import Colors
import logging

# Filler until translations come in
_ = lambda s: s

class Game:

    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()
        self.deck = Deck()
        self.playerHand = Hand()
        self.robotHand = Hand()

        self.deck.deal([self.playerHand, self.robotHand])
        
        # How many cards in our line
        self.cardsLength = 10
    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    # The main game loop.
    def run(self):
        self.running = True

        screen = pygame.display.get_surface()
        width = screen.get_width()
        height = screen.get_height()

        screen.fill(Colors["LIGHT_GREY"])
        pygame.display.update()

        drawn = self.deck.draw()
        # msg = "You drew " + str(drawn) + " from the deck."
        msg = _("You drew %i from the deck.") % drawn
        waitingForClick = True
        robotTurn = False
        timeStartedRobotTurn = None
        waitingForDiscardChoice = False
        robotDrew = False
        playerDrew = False
        playerIsDrawingFromDeck = False
        robotChoseDiscard = False
        while self.running:
            width, height = pygame.display.get_surface().get_size()
            mousePos = pygame.mouse.get_pos()

            if len(self.deck.deck) <= 2: 
                # msg = "You have " + str(self.playerHand.countPoints()) + " points, robot has " + str(self.robotHand.countPoints()) 
                msg = _("You have %i points, robot has %i points") % (self.playerHand.countPoints(), self.robotHand.countPoints())
                waitingForClick = False
                waitingForDiscardChoice = False
                robotDrew = False
                playerDrew = False
                playerIsDrawingFromDeck = False
                robotChoseDiscard = False

            dirty = []
            for i in range(self.cardsLength):
                test = Card(Colors["DARK_GREY"], width//self.cardsLength//2, 
                (height//100) + (height//self.cardsLength)*i, int((height//self.cardsLength) * 0.9), str(self.playerHand.hand[i]))
                test.draw(screen)
                dirty.append(test.getRect())

            if robotTurn:
                if(pygame.time.get_ticks() - timeStartedRobotTurn < 1500):
                    # msg = "It\'s the robot\'s turn."
                    msg = _("It\'s the robot\'s turn.")
                elif (pygame.time.get_ticks() - timeStartedRobotTurn < 3000):
                    print("running")
                    if not robotChoseDiscard:
                        old_card = self.robotHand.place(drawn)
            
                        if old_card == drawn and not self.deck.empty():
                            # msg = "The robot draws a card."
                            msg = _("The robot draws a card.")
                            drawn = self.deck.draw()
                            drawn = self.robotHand.place(drawn)
                        else:
                            # msg = "The robot picked up "+ str(drawn) + " from the pile."
                            msg = _("The robot picked up %i from the pile.") % drawn
                            drawn = old_card
                    robotChoseDiscard = True
                elif (pygame.time.get_ticks() - timeStartedRobotTurn < 4500):
                    # msg = "The robot discards "+str(drawn)
                    msg = "The robot discards %i" % drawn
                
                else:
                    if self.deck.empty():
                        pass
                    elif not playerDrew:
                        # msg = "You drew "+str(drawn)+ " from discard pile. Use?"
                        msg = "You drew %i from discard pile. Use?" % drawn
                        playerDrew = True
                        robotTurn = False
                        waitingForDiscardChoice = True
                                    
            font = pygame.font.SysFont('arial', width//20)
            text = font.render(msg, 1, (0,0,0))
            textX = (width//self.cardsLength//2) + width//10
            textY = height//10
            bottomRightX = textX + text.get_rect()[2]
            bottomRightY = textY + text.get_rect()[3]

            pygame.draw.rect(screen, Colors["LIGHT_GREY"], (textX, textY, width, bottomRightY))
            screen.blit(text, ((textX, textY)))
            dirty.append((textX, textY, width, bottomRightY))

            yesButton = None
            noButton = None
            if waitingForDiscardChoice:
                yesButton = Card(Colors["GREEN"], textX, bottomRightY + textY, width//8, _("Yes"))
                yesButton.draw(screen)
                noButton = Card(Colors["RED"], textX + abs(bottomRightX-textX)//4*2, bottomRightY + textY, width//8, _("No"))
                noButton.draw(screen)

                dirty.append(yesButton.getRect())
                dirty.append(noButton.getRect())

            # Pump GTK messages.
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    screen.fill(Colors["LIGHT_GREY"])
                    pygame.display.update()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(self.cardsLength):
                        card = Card(Colors["DARK_GREY"], width//self.cardsLength//2, 
                (height//100) + (height//self.cardsLength)*i, int((height//self.cardsLength) * 0.9), str(self.playerHand.hand[i]))
                        if(card.isOver(mousePos)):
                            if(waitingForClick):
                                print("clicked on card "+str(i))
                                self.playerHand.hand[i], drawn = drawn, self.playerHand.hand[i]
                                robotTurn = True
                                robotChoseDiscard = False
                                robotDrew = False
                                playerDrew = False
                                waitingForClick = False
                                timeStartedRobotTurn = pygame.time.get_ticks()
                    
                    if(waitingForDiscardChoice):
                        print("mouse down while waiting for discard choice")
                        if(yesButton.isOver(mousePos)):
                            waitingForDiscardChoice = False
                            waitingForClick = True
                            pygame.draw.rect(screen, Colors["LIGHT_GREY"], yesButton.getRect())
                            pygame.draw.rect(screen, Colors["LIGHT_GREY"], noButton.getRect())
                            # msg = "Pick card to replace."
                            msg = _("Pick card to replace.")

                        elif noButton.isOver(mousePos):
                            print("clicked no button")
                            # playerIsDrawingFromDeck = True
                            waitingForClick = True
                            waitingForDiscardChoice = False

                            drawn = self.deck.draw()
                            # msg = "You drew "+str(drawn)+" from the deck."
                            msg = _("You drew %i from the deck.") % drawn
                            pygame.draw.rect(screen, Colors["LIGHT_GREY"], yesButton.getRect())
                            pygame.draw.rect(screen, Colors["LIGHT_GREY"], noButton.getRect())





            # Try to stay at 30 FPS
            self.clock.tick(30)
            pygame.display.update(dirty)
            pygame.event.clear()

            ee = pygame.event.Event(24)
            try_post = 1

            # the pygame.event.post raises an exception if the event
            #   queue is full.  so wait a little bit, and try again.
            while try_post:
                try:
                    pygame.event.post(ee)
                    try_post = 0
                except:
                    pygame.time.wait(1)
                    try_post = 1

            



# This function is called when the game is run directly from the command line:
# ./Game.py
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = Game()
    game.run()


if __name__ == '__main__':
    main()