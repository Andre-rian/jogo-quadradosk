import pygame
import random
from config import *
from database import DatabaseManager
from entities.player import Player
from entities.enemy import Inimigo
from entities.projectiles import Tiro, TiroInimigo
from entities.world import Explosao, PowerUp
from core.ui import Botao

# Inicialização
pygame.init()
db = DatabaseManager()
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("QUADRADOXS")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 30)
fonte_titulo = pygame.font.SysFont("Arial", 60)

# Variáveis de Estado
estado = "menu"
nome, senha = "", ""
digitando_nome, digitando_senha = True, False
logado = False
score_salvo = False
inicio_timer = 180

def resetar_jogo():
    global player, inimigos, tiros, tiros_inimigos, explosoes, powerups
    global vida, score, dificuldade, inicio_timer, score_salvo
    player = Player()
    inimigos = []
    tiros = []
    tiros_inimigos = []
    explosoes = []
    powerups = []
    vida = 3
    score = 0
    dificuldade = 1
    inicio_timer = 180
    score_salvo = False

resetar_jogo()

rodando = True
while rodando:
    dt = clock.tick(60) 
    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    # ================= ESTADO: MENU =================
    if estado == "menu":
        tela.fill((10, 10, 10))
        btn_jogar = Botao(250, 300, 300, 60, "JOGAR")
        btn_rank = Botao(250, 380, 300, 60, "RANKING")

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if digitando_nome:
                    if evento.key == pygame.K_BACKSPACE: nome = nome[:-1]
                    elif evento.key == pygame.K_RETURN and nome:
                        digitando_nome, digitando_senha = False, True
                    else:
                        if len(nome) < 10 and evento.unicode.isprintable():
                            nome += evento.unicode
                elif digitando_senha:
                    if evento.key == pygame.K_BACKSPACE: senha = senha[:-1]
                    elif evento.key == pygame.K_RETURN and senha:
                        res = db.login(nome, senha)
                        if res in ["criado", "login"]:
                            logado = True
                            digitando_senha = False
                    else:
                        if len(senha) < 15 and evento.unicode.isprintable():
                            senha += evento.unicode

            if btn_jogar.clicado(evento) and logado:
                resetar_jogo()
                estado = "inicio"
                break
            if btn_rank.clicado(evento):
                estado = "ranking"
                break

        titulo = fonte_titulo.render("QUADRADOXS", True, (255, 255, 0))
        tela.blit(titulo, (220, 50))
        cor_n = (255, 255, 0) if digitando_nome else (255, 255, 255)
        cor_s = (255, 255, 0) if digitando_senha else (255, 255, 255)
        tela.blit(fonte.render(f"Nick: {nome}", True, cor_n), (250, 150))
        tela.blit(fonte.render(f"Senha: {'*' * len(senha)}", True, cor_s), (250, 200))
        
        if not logado:
            tela.blit(fonte.render("Pressione ENTER para Logar", True, (150,150,150)), (230, 260))
        else:
            tela.blit(fonte.render("LOGADO! Clique em JOGAR", True, (0,255,0)), (260, 260))
        
        btn_jogar.desenhar(tela, fonte)
        btn_rank.desenhar(tela, fonte)

    # ================= ESTADO: INICIO =================
    elif estado == "inicio":
        tela.fill((10, 10, 10))
        inicio_timer -= 1
        txt = "3" if inicio_timer > 120 else "2" if inicio_timer > 60 else "1" if inicio_timer > 10 else "VAI!"
        surf = fonte_titulo.render(txt, True, (255, 255, 255))
        tela.blit(surf, (400 - surf.get_width()//2, 300 - surf.get_height()//2))
        if inicio_timer <= 0: estado = "jogando"

    # ================= ESTADO: JOGANDO =================
    elif estado == "jogando":
        tela.fill((5, 5, 15))
        teclas = pygame.key.get_pressed()
        dificuldade = 1 + score // 100

        player.mover(teclas, tiros)
        player.x = max(0, min(player.x, 800 - 50))
        player.y = max(0, min(player.y, 600 - 50))

        if random.randint(1, max(20, 100 - dificuldade * 5)) == 1:
            inimigos.append(Inimigo(random.randint(0, 750), -50, random.choice(["basico", "sniper", "perseguidor"])))

        # Colisões Tiros Player
        for t in tiros[:]:
            t.mover()
            if not (0 < t.x < 800 and 0 < t.y < 600):
                tiros.remove(t)
                continue
            for i in inimigos[:]:
                if pygame.Rect(t.x, t.y, 8, 8).colliderect(pygame.Rect(i.x, i.y, 50, 50)):
                    if t in tiros: tiros.remove(t)
                    inimigos.remove(i)
                    explosoes.append(Explosao(i.x+25, i.y+25))
                    score += 10
                    if random.random() < 0.15:
                        powerups.append(PowerUp(i.x, i.y, random.choice(["Vida", "Tiro", "Velocidade", "Multishot"])))
                    break

        # Atualizar Inimigos
        for i in inimigos[:]:
            i.atualizar()
            i.y += 1 + (dificuldade * 0.1)
            if i.tipo == "basico": i.mover_lateral()
            elif i.tipo == "perseguidor": i.seguir_player(player)
            i.tentar_atirar(player, tiros_inimigos, dificuldade)
            if pygame.Rect(i.x, i.y, 50, 50).colliderect(pygame.Rect(player.x, player.y, 50, 50)) or i.y > 600:
                if i in inimigos: inimigos.remove(i)
                vida -= 1
                player.dano_timer = 30
                explosoes.append(Explosao(i.x+25, i.y+25))

        for ti in tiros_inimigos[:]:
            ti.mover()
            if pygame.Rect(ti.x, ti.y, 10, 10).colliderect(pygame.Rect(player.x, player.y, 50, 50)):
                tiros_inimigos.remove(ti)
                vida -= 1
                player.dano_timer = 30
            elif not (0 < ti.y < 600): tiros_inimigos.remove(ti)

        for p in powerups[:]:
            p.mover()
            if pygame.Rect(p.x, p.y, 20, 20).colliderect(pygame.Rect(player.x, player.y, 50, 50)):
                if p.tipo == "Vida": vida = min(vida + 1, 5)
                elif p.tipo == "Velocidade": player.vel += 0.5
                elif p.tipo == "Tiro": player.cooldown_max = max(5, player.cooldown_max - 2)
                elif p.tipo == "Multishot": player.multishot = min(2, player.multishot + 1)
                powerups.remove(p)

        for e in explosoes[:]:
            e.atualizar(); 
            if e.tempo <= 0: explosoes.remove(e)

        # Desenho das Entidades
        for i in inimigos: i.desenhar(tela)
        for t in tiros: t.desenhar(tela)
        for ti in tiros_inimigos: ti.desenhar(tela)
        for p in powerups: p.desenhar(tela)
        for e in explosoes: e.desenhar(tela)
        player.desenhar(tela)

        # --- UI GAMEPLAY (RESTAURADA) ---
        cor_vida = (0, 255, 0) if vida > 2 else (255, 255, 0) if vida == 2 else (255, 0, 0)
        txt_info = fonte.render(f"Player: {nome} | Vida: {vida} | Score: {score}", True, cor_vida)
        tela.blit(txt_info, (10, 10))
        
        if vida <= 0: estado = "gameover"

    # ================= ESTADO: GAMEOVER =================
    elif estado == "gameover":
        tela.fill((20, 0, 0))
        btn_retry = Botao(250, 350, 300, 60, "REINICIAR")
        btn_menu = Botao(250, 430, 300, 60, "MENU PRINCIPAL") # ADICIONADO
        
        if not score_salvo:
            db.save_score(nome, score)
            score_salvo = True

        tela.blit(fonte_titulo.render("GAME OVER", True, (255, 0, 0)), (240, 150))
        tela.blit(fonte.render(f"Score Final: {score}", True, (255,255,255)), (310, 230))
        
        for evento in eventos:
            if btn_retry.clicado(evento):
                resetar_jogo()
                estado = "inicio"
            if btn_menu.clicado(evento):
                resetar_jogo()
                estado = "menu"
        
        btn_retry.desenhar(tela, fonte)
        btn_menu.desenhar(tela, fonte)

    # ================= ESTADO: RANKING =================
    elif estado == "ranking":
        tela.fill((10, 10, 30))
        btn_voltar = Botao(250, 500, 300, 50, "VOLTAR")
        scores = db.get_top_scores()
        for i, (n, s) in enumerate(scores):
            txt = fonte.render(f"{i+1}. {n} - {s}", True, (255, 255, 255))
            tela.blit(txt, (300, 150 + i * 40))
        for evento in eventos:
            if btn_voltar.clicado(evento): estado = "menu"
        btn_voltar.desenhar(tela, fonte)

    pygame.display.flip()

pygame.quit()