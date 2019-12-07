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

        self.deck.deal([self.playerHand])
        
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

        while self.running:
            width, height = pygame.display.get_surface().get_size()
            mousePos = pygame.mouse.get_pos()

            dirty = []
            for i in range(self.cardsLength):
                test = Card(Colors["DARK_GREY"], width//self.cardsLength//2, 
                (height//100) + (height//self.cardsLength)*i, int((height//self.cardsLength) * 0.9), str(self.playerHand.hand[i]))
                test.draw(screen)
                dirty.append(test.getRect())

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
                            print("clicked on card "+str(i))

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