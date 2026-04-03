import pygame

class Explosao:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tempo = 20  # Frames de duração
        self.raio = 10

    def atualizar(self):
        self.tempo -= 1
        self.raio += 2  # A explosão cresce enquanto some

    def desenhar(self, tela):
        # Desenha um círculo laranja com borda amarela para efeito de fogo
        pygame.draw.circle(tela, (255, 165, 0), (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, (255, 255, 0), (int(self.x), int(self.y)), self.raio // 2)

class PowerUp:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.vel = 1.5
        self.rect = pygame.Rect(x, y, 20, 20)

    def mover(self):
        self.y += self.vel
        self.rect.y = self.y

    def desenhar(self, tela):
        # Cores baseadas no tipo para o jogador identificar rápido
        cores = {
            "Vida": (0, 255, 0),        # Verde
            "Tiro": (0, 100, 255),      # Azul
            "Velocidade": (255, 255, 0), # Amarelo
            "Multishot": (0, 255, 200)   # Ciano
        }
        cor = cores.get(self.tipo, (255, 255, 255))
        
        # Desenha o quadrado do item
        pygame.draw.rect(tela, cor, self.rect)
        # Desenha uma borda branca para destacar
        pygame.draw.rect(tela, (255, 255, 255), self.rect, 1)