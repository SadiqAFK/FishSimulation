import pygame

class Obstacle:
    def __init__(self, pos):
        self.pos = pos
        self.width = 25
        self.height = 25

    def draw(self, screen):
        rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        pygame.draw.rect(screen, (136, 227, 182), rect)