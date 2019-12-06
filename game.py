#!/usr/bin/python3
import pygame
import gi
import math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from deck import Deck
from hand import Hand
from card import Card
from colors import Colors

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

        while self.running:
            width, height = pygame.display.get_surface().get_size()

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

            screen.fill(Colors["LIGHT_GREY"])
            test = Card(Colors["DARK_GREY"], 200, 200, 80, "1")
            test.draw(screen)

            # Try to stay at 30 FPS
            self.clock.tick(30)
            pygame.display.flip();


# This function is called when the game is run directly from the command line:
# ./Game.py
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = Game()
    game.run()


if __name__ == '__main__':
    main()