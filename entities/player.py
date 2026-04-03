import pygame
import math
import random

class Player:
    def __init__(self):
        self.x = 400 - 25
        self.y = 300 - 25
        self.vel = 5
        self.cooldown = 0
        self.cooldown_max = 20
        self.dano_timer = 0
        self.multishot = 0 # 0, 1 ou 2

    def disparar(self, tiros, angulo_base):
        from .projectiles import Tiro # Import local para evitar erro circular
        qtd = 1 + (self.multishot * 2)
        abertura = 60
        passo = abertura / (qtd - 1) if qtd > 1 else 0
        inicio = angulo_base - (abertura / 2) if qtd > 1 else angulo_base

        for i in range(qtd):
            ang = math.radians(inicio + (passo * i))
            dx = math.cos(ang) * 10
            dy = math.sin(ang) * 10
            tiros.append(Tiro(self.x + 21, self.y + 21, dx, dy))
        self.cooldown = self.cooldown_max

    def mover(self, teclas, tiros):
        if teclas[pygame.K_a]: self.x -= self.vel
        if teclas[pygame.K_d]: self.x += self.vel
        if teclas[pygame.K_w]: self.y -= self.vel
        if teclas[pygame.K_s]: self.y += self.vel

        if self.cooldown > 0: self.cooldown -= 1
        else:
            if teclas[pygame.K_UP]: self.disparar(tiros, 270)
            elif teclas[pygame.K_DOWN]: self.disparar(tiros, 90)
            elif teclas[pygame.K_LEFT]: self.disparar(tiros, 180)
            elif teclas[pygame.K_RIGHT]: self.disparar(tiros, 0)

    def desenhar(self, tela):
        cor = (255, 0, 0)
        ox, oy = 0, 0
        if self.dano_timer > 0:
            self.dano_timer -= 1
            ox, oy = random.randint(-4, 4), random.randint(-4, 4)
            cor = (255, 255, 255) if self.dano_timer % 4 < 2 else (255, 0, 0)
        pygame.draw.rect(tela, cor, (self.x + ox, self.y + oy, 50, 50))