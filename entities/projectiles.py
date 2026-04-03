import pygame

class Tiro:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = pygame.Rect(x, y, 8, 8)

    def mover(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x
        self.rect.y = self.y

    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 255, 0), self.rect)

class TiroInimigo(Tiro):
    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 0, 255), self.rect)