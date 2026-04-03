import pygame

class Botao:
    def __init__(self, x, y, w, h, texto):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto

    def desenhar(self, tela, fonte):
        m_pos = pygame.mouse.get_pos()
        cor = (150, 150, 150) if self.rect.collidepoint(m_pos) else (100, 100, 100)
        pygame.draw.rect(tela, cor, self.rect, border_radius=5)
        
        txt = fonte.render(self.texto, True, (255, 255, 255))
        tela.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

    def clicado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                return True
        return False