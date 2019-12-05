#!/usr/bin/python3
import pygame
import gi
import math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from deck import Deck
from hand import Hand

class Game:

    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()

        self.deck = Deck()
        self.playerHand = Hand()
        self.robotHand = Hand()
        self.deck.deal([self.playerHand, self.robotHand])

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

        dirty = []
        dirty.append(pygame.draw.rect(screen, (255, 255, 255),
                                      pygame.Rect(0, 0, width, height)))
        pygame.display.update(dirty)

        while self.running:
            width, height = pygame.display.get_surface().get_size()

            dirty = []

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
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    width = screen.get_width()
                    height = screen.get_height()

            # Each row of cards is 33% of game height
            
            textRect = pygame.Rect(0, 0, width, height//3)
            playerRect = pygame.Rect(0, textRect.bottom, width, height//3)
            # testRect = pygame.Rect(0, 0, 50, 50)

            dirty.append(textRect)
            dirty.append(pygame.draw.rect(screen, (100, 0, 0), playerRect))
            # dirty.append(testRect)

            # Update Display
            pygame.display.update(dirty)

            # Try to stay at 30 FPS
            self.clock.tick(30)


# This function is called when the game is run directly from the command line:
# ./Game.py
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = Game()
    game.run()


if __name__ == '__main__':
    main()