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
        msg = "You drew " + str(drawn) + " from the deck."
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

            dirty = []
            for i in range(self.cardsLength):
                test = Card(Colors["DARK_GREY"], width//self.cardsLength//2, 
                (height//100) + (height//self.cardsLength)*i, int((height//self.cardsLength) * 0.9), str(self.playerHand.hand[i]))
                test.draw(screen)
                dirty.append(test.getRect())
            if robotTurn:
                if(pygame.time.get_ticks() - timeStartedRobotTurn < 1500):
                    msg = "It\'s the robot\'s turn."
                elif (pygame.time.get_ticks() - timeStartedRobotTurn < 3000):
                    print("running")
                    if not robotChoseDiscard:
                        old_card = self.robotHand.place(drawn)
            
                        if(old_card == drawn):
                            msg = "The robot draws a card."
                        else:
                            msg = "The robot picked up "+ str(drawn) + " from the pile."
                    robotChoseDiscard = True
                elif (pygame.time.get_ticks() - timeStartedRobotTurn < 4500):
                    msg = "The robot discards "+str(drawn)
                
                else:
                    if not playerDrew:
                        msg = "You drew "+str(drawn)+ " from discard pile. Use?"
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
                yesButton = Card(Colors["GREEN"], textX, bottomRightY + textY, width//5, "Yes")
                yesButton.draw(screen)
                noButton = Card(Colors["RED"], textX + abs(bottomRightX-textX)//4*2, bottomRightY + textY, width//5, "No")
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
                            msg = "Pick card to replace."

                        elif noButton.isOver(mousePos):
                            print("clicked no button")
                            # playerIsDrawingFromDeck = True
                            waitingForClick = True
                            waitingForDiscardChoice = False

                            drawn = self.deck.draw()
                            msg = "You drew "+str(drawn)+" from the deck."
                            pygame.draw.rect(screen, Colors["LIGHT_GREY"], yesButton.getRect())
                            pygame.draw.rect(screen, Colors["LIGHT_GREY"], noButton.getRect())





            # Try to stay at 30 FPS
            self.clock.tick(30)
            pygame.display.update(dirty)
            



# This function is called when the game is run directly from the command line:
# ./Game.py
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = Game()
    game.run()


if __name__ == '__main__':
    main()