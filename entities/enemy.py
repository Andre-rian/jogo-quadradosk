import pygame
import random
import math
from .projectiles import TiroInimigo

class Inimigo:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.cooldown = 0
        self.vel_x = random.choice([-2, 2])
        self.timer_direcao = 60

    def mover_lateral(self):
        self.timer_direcao -= 1
        if self.timer_direcao <= 0:
            self.vel_x *= -1
            self.timer_direcao = 60
        self.x += self.vel_x

    def seguir_player(self, player):
        if self.x < player.x: self.x += 1.5
        else: self.x -= 1.5

    def tentar_atirar(self, player, tiros_inimigos, dificuldade):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        pode_atirar = False
        if self.tipo == "basico" and abs(self.x - player.x) < 50: pode_atirar = True
        elif self.tipo == "sniper" or self.tipo == "perseguidor": pode_atirar = True

        if pode_atirar:
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy) or 1
            tiros_inimigos.append(TiroInimigo(self.x + 20, self.y + 20, (dx/dist)*5, (dy/dist)*5))
            self.cooldown = max(20, 100 - dificuldade * 5)
    def atualizar(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def desenhar(self, tela):
        cor = (0, 255, 0) # Basico
        if self.tipo == "sniper": cor = (0, 200, 255)
        elif self.tipo == "perseguidor": cor = (255, 100, 0)
        pygame.draw.rect(tela, cor, (self.x, self.y, 50, 50))