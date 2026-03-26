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
        self.x = 800 // 2 - 25
        self.y = 800 // 2 - 25
        self.vel = 5
        self.cooldown = 0 
        self.dano_timer = 0
        self.multishot = 1
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
        if teclas [pygame.K_UP] and self.cooldown == 0:
            
            if self.multishot == 1:
                tiros.append(Tiro(self.x + 25, self.y, 0, -10))

            elif self.multishot == 2:
                tiros.append(Tiro(self.x + 15, self.y, 0, -10))
                tiros.append(Tiro(self.x + 35, self.y, 0, -10))

            elif self.multishot == 3:
                tiros.append(Tiro(self.x + 10, self.y, -2, -10))
                tiros.append(Tiro(self.x + 25, self.y, 0, -10))
                tiros.append(Tiro(self.x + 40, self.y, 2, -10))
            self.cooldown = 20
    
    
    
    
    def desenhar(self, tela):
        offset_x = 0
        offset_y = 0
        
        if self.dano_timer > 0:
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            self.dano_timer -= 1
        
            if self.dano_timer % 4 < 2:
                cor = (255, 255, 0)
            else:
                cor = (255, 0, 0)

        else:
            cor = (255, 0, 0)    
        
        pygame.draw.rect(tela, cor, (self.x + offset_x, self.y + offset_y, 50, 50))

   

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

        if self.x < 0:
            self.y = 0
        elif self.x > 750:
            self.x = 750
    
    
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
        elif self.tipo == "Velocidade":
            cor = (255, 255, 0)
        elif self.tipo == "Multishot":
            cor = (0, 255, 0)



        pygame.draw.rect(tela, cor, (self.x, self.y, 20, 20))


class Botao():
    def __init__(self, x , y, w, h, texto):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto

    def desenhar(self, tela, fonte):
        mouse_pos = pygame.mouse.get_pos()

        cor = (100, 100, 100)
        if self.rect.collidepoint(mouse_pos):
            cor = (150, 150, 150)

        pygame.draw.rect(tela, cor, self.rect)

        texto_render = fonte.render(self.texto, True, (0, 0, 0))

        tela.blit(
            texto_render,
            (
                self.rect.x + (self.rect.width // 2 - texto_render.get_width() // 2),
                self.rect.y + (self.rect.height // 2 - texto_render.get_height() // 2)
            )
        )

    def clicado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos)