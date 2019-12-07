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
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.sideLen, self.sideLen), 0)
        font = pygame.font.SysFont('arial', int(self.sideLen*0.7))
        text = font.render(self.text, 1, (0,0,0))
        screen.blit(text, (self.x + (self.sideLen/2 - text.get_width()/2), self.y + (self.sideLen/2 - text.get_height()/2)))
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.sideLen:
            if pos[1] > self.y and pos[1] < self.y + self.sideLen:
                return True
        return False
    # Get card in rectangle format for dirty updating
    def getRect(self):
        return(self.x, self.y, self.sideLen, self.sideLen)