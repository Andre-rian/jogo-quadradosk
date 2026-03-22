import pygame
import random
import math

class Tiro():
    def __init__(self, x, y, dx, dy):
        self.x = x 
        self.y = y
        self.vel = -10
        self.dx = dx 
        self.dy = dy


    def mover(self):
        self.x += self.dx
        self.y += self.dy

    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 255, 0), (self.x, self.y, 10, 20))
 

class Player():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.vel = 5
        self.cooldown = 0 
    def mover(self, teclas, tiros):
        if teclas [pygame.K_d]:
            self.x += self.vel
        if teclas [pygame.K_a]:
            self.x -= self.vel
        if teclas [pygame.K_s]:
            self.y += self.vel
        if teclas [pygame.K_w]:
            self.y -= self.vel

        if self.cooldown > 0:
            self.cooldown -= 1


        if teclas [pygame.K_UP] and self.cooldown == 0:
            tiros.append(Tiro(self.x + 25, self.y, 0, -10))
            self.cooldown = 20

        if teclas [pygame.K_LEFT] and self.cooldown == 0:
            tiros.append(Tiro(self.x, self.y + 25, -10, 0))
            self.cooldown = 20

        if teclas [pygame.K_DOWN] and self.cooldown == 0:
            tiros.append(Tiro(self.x + 25, self.y, 0, 10))
            self.cooldown = 20

        if teclas [pygame.K_RIGHT] and self.cooldown == 0:
            tiros.append(Tiro(self.x + 50, self.y + 25, 10, 0))
            self.cooldown = 20
    
    
    
    
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 0, 0), (self.x, self.y, 50, 50))

   

class Inimigo():
    def __init__(self, x, y, tipo):
        self.x = x 
        self.y = y 
        self.cooldown = 0 
        self.vel_x = 2
        self.direction_timer = random.randint(30, 120)
        self.tipo = tipo
    

    def mover(self):
        self.direction_timer -= 1 
        
        if self.direction_timer <= 0:
            self.vel_x = random.choice([-2, 2])
            self.direction_timer = random.randint(30, 120) 
    
        self.x += self.vel_x
    
    
    def atirar(self, player, tiros_inimigos, dificuldade):
        
        if self.cooldown <= 0 and self.pode_atirar(player):
            tiros_inimigos.append(Tiro_inimigo(self.x + 25, self.y + 50, player.x, player.y))
            self.cooldown = max(20, 60 - dificuldade * 5)
    
    
    
    def pode_atirar(self, player):
        return abs (self.x - player.x) < 30 

    def seguir_player(self, player):

        if self.x < player.x:
            self.x += 2
        elif self.x > player.x:
            self.x -= 2

    def atualizar(self):
        if self.cooldown > 0:
                self.cooldown -= 1


    def desenhar(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), (self.x, self.y, 50, 50))
    

class Tiro_inimigo():
        def  __init__(self, x, y, alvo_x, alvo_y):
            self.x = x 
            self.y = y

            dx = alvo_x - x 
            dy = alvo_y - y 

            distancia = math.sqrt(dx**2 + dy**2)
            self.vel = 5
            if distancia == 0:
                distancia = 1

            self.dx = (dx / distancia) * self.vel
            self.dy = (dy / distancia) *  self.vel

        def mover(self):
            self.x +=  self.dx 
            self.y +=  self.dy 

        def desenhar(self, tela):
            pygame.draw.rect(tela, (255, 0, 255), (self.x, self.y, 10, 10))

class Explosão():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tempo = 20
        self.raio = 10

    def atualizar(self):
        self.tempo -= 1
        self.raio += 2
    
    def desenhar(self, tela):
        pygame.draw.circle(tela, (255, 165, 0), (self.x, self.y), self.raio)

class Power_ups():
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.vel = 0.5 

    def mover(self):
        self.y += self.vel
        
    def desenhar(self, tela):
        cor = (0, 255, 0)

        if self.tipo == "Vida":
            cor = (0, 255, 0)
        elif self.tipo == "Tiro":
            cor = (0, 0, 255)

        pygame.draw.rect(tela, cor, (self.x, self.y, 20, 20))