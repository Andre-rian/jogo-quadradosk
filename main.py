import pygame
import random
import math
from classes import Player, Inimigo, Tiro, Tiro_inimigo, Explosão, Power_ups, Botao
from dados import DatabaseManager

pygame.init()
db = DatabaseManager()

tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste")

clock = pygame.time.Clock()




tiros = []
tiros_inimigos = []
inimigos = []
player = Player()
spawn_timer = 0
explosões = []
powerups = []
vida = 3 
dificuldade = 1
fonte = pygame.font.SysFont("Arial", 30)
fonte_titulo = pygame.font.SysFont("Arial", 60)
score = 0
inicio_timer = 180
nome = ""
senha = ""
digitando_nome = True
digitando_senha = False
piscar = 0
logado = False
estado = "menu"
rodando = True
def resetar_jogo():
    global tiros, tiros_inimigos, player, explosões, vida, score, inimigos, dificuldade, powerups, score_salvo, nome, digitando_nome, senha, digitando_senha, logado, inicio_timer
    tiros_inimigos = []
    inimigos = []
    explosões = []
    vida = 3
    inicio_timer = 180
    score = 0
    dificuldade = 1
    powerups = []
    player = Player()
    score_salvo = False
    logado = False

while rodando:
    clock.tick(60)
    spawn_timer += 1

    # ================= MENU =================
    if estado == "menu":

        botao_jogar = Botao(250, 300, 300, 60, "JOGAR")
        botao_ranking = Botao(250, 400, 300, 60, "Ranking")

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if digitando_nome:
                    if evento.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]

                    elif evento.key == pygame.K_RETURN:
                        if nome != "":
                            digitando_nome = False
                            digitando_senha = True

                    else:
                        if len(nome) < 10:
                            nome += evento.unicode

                elif digitando_senha:
                    if evento.key == pygame.K_BACKSPACE:
                        senha = senha[:-1]

                    elif evento.key == pygame.K_RETURN:
                        if nome != "":
                            resultado = db.login(nome, senha)

                            if resultado in ["criado", "login"]:
                                logado = True
                                resetar_jogo()
                                estado = "inicio"

                            elif resultado == "erro":
                                print("Senha errada")

                    else:
                        if len(senha) < 10:
                            senha += evento.unicode

            if botao_jogar.clicado(evento) and logado:
                resetar_jogo()
                estado = "inicio"


            if botao_ranking.clicado(evento):
                estado = "ranking"

        tela.fill((10, 10, 10))

        texto_nick = fonte.render(f"Nick: {nome}", True, (255, 255, 255))
        tela.blit(texto_nick, (250, 150))

        senha_oculta = "*" * len(senha)
        texto_senha = fonte.render(f"Senha: {senha_oculta}", True, (255, 255, 255))
        tela.blit(texto_senha, (250, 200))

        titulo = fonte_titulo.render("Quadradoxs", True, (255, 255, 0))
        tela.blit(titulo, (250, 60))

        if not logado and botao_jogar.clicado(evento):
            texto = fonte.render("Faça login para jogar", True, (255, 0, 0))
            tela.blit(texto, (250, 240))
            pygame.draw.rect(tela, (80, 80, 80), botao_jogar.rect) 


        botao_jogar.desenhar(tela, fonte)
        botao_ranking.desenhar(tela, fonte)

        pygame.display.flip()

    # ================= RANKING =================
    elif estado == "ranking":

        pygame.event.clear()

        botao_voltar = Botao(250, 450, 300, 60, "VOLTAR")

        tela.fill((10, 10, 10))

        titulo = fonte_titulo.render("RANKING", True, (255, 255, 0))
        tela.blit(titulo, (250, 50))

        top = db.get_top_scores()

        y = 150
        for i ,(nick, pontos) in enumerate(top):

            if i == 0:
                cor = (255, 215, 0)
            elif i == 1:
                cor = (192, 192, 192)
            elif i == 2:
                 cor = (205, 127, 50) 
            else:
                cor = (255, 255, 255)


            texto = fonte.render(f"{i + 1}. {nick} -- {pontos}", True, cor)
            tela.blit(texto, (280, y))
            y += 40

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if botao_voltar.clicado(evento):
                estado = "menu"

        botao_voltar.desenhar(tela, fonte)

        pygame.display.flip()



# ================= timer inicial =================



    elif estado == "inicio":
            
        tela.fill((0, 0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            
        inicio_timer -= 1 


        if inicio_timer > 120:
            texto = "3"

        elif inicio_timer > 60:
            texto = "2"

        elif inicio_timer > 30:
            texto = "1"
        else:
            texto = "JÁ"

        texto_render = fonte_titulo.render(texto, True, (255, 255, 255))

        tela.blit(texto_render, (358, 250))      


        if inicio_timer <= 0:
            estado = "jogando"

        pygame.display.flip()   
        




    # ================= JOGO =================
    elif estado == "jogando":
    
    

        tela.fill((0, 0, 0))
        rect_player = pygame.Rect(player.x, player.y, 50, 50)

        texto_player = fonte.render(f"Player:  {nome}", True, (255, 255, 255))
        tela.blit(texto_player, (10, 70))
        dificuldade = 1 + score // 100
        teclas = pygame.key.get_pressed()
        score_salvo = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # tiros player
        for tiro in tiros[:]:
            tiro.mover()

            for inimigo in inimigos[:]:
                rect_tiro = pygame.Rect(tiro.x, tiro.y, 10, 20)
                rect_inimigo = pygame.Rect(inimigo.x, inimigo.y, 50, 50)

                if rect_tiro.colliderect(rect_inimigo):
                    tiros.remove(tiro)
                    inimigos.remove(inimigo)
                    explosões.append(Explosão(inimigo.x + 25, inimigo.y + 25))
                    score += 10

                    if random.random() < 0.2:
                        tipo = random.choice(["Vida", "Tiro", "Velocidade", "Multishot"])
                        powerups.append(Power_ups(inimigo.x, inimigo.y, tipo))
                    break

                if rect_inimigo.colliderect(rect_player):
                    inimigos.remove(inimigo)
                    vida -= 1
                    player.dano_timer = 20
                    explosões.append(Explosão(inimigo.x + 25, inimigo.y + 25))
                    break

        # tiros inimigos
        for tiro in tiros_inimigos[:]:
            tiro.mover()
            if tiro.y > 600:
                tiros_inimigos.remove(tiro)

        for tiro in tiros_inimigos[:]:
            rect_tiro = pygame.Rect(tiro.x, tiro.y, 10, 20)
            if rect_tiro.colliderect(rect_player):
                tiros_inimigos.remove(tiro)
                vida -= 1
                player.dano_timer = 20

        # inimigos
        for inimigo in inimigos[:]:
            inimigo.atualizar()
            inimigo.y += 1

            if inimigo.y > 600:
                inimigos.remove(inimigo)
                vida -= 1
                player.dano_timer = 20
                explosões.append(Explosão(inimigo.x + 25, inimigo.y + 25))

            if inimigo.tipo == "basico":
                inimigo.mover()
                inimigo.atirar(player, tiros_inimigos, dificuldade)

            elif inimigo.tipo == "sniper":
                inimigo.atirar(player, tiros_inimigos, dificuldade)

            elif inimigo.tipo == "perseguidor":
                inimigo.seguir_player(player)
                inimigo.atirar(player, tiros_inimigos, dificuldade)

        # explosões
        for explosao in explosões[:]:
            explosao.atualizar()
            if explosao.tempo <= 0:
                explosões.remove(explosao)


    
        
        # spawn
        if spawn_timer > max(40, 150 - dificuldade * 10):
            x = random.randint(0, 750)
            spawn_timer = 0

            tipo = random.choice(["basico", "sniper", "perseguidor"])
            inimigo = Inimigo(x, 0, tipo)
            inimigo.vel_x += dificuldade
            inimigos.append(inimigo)

        # powerups
        for p in powerups[:]:
            if p.y > 600:
                powerups.remove(p)

        for p in powerups[:]:
            rect_p = pygame.Rect(p.x, p.y, 20, 20)
            p.mover()

            if rect_p.colliderect(rect_player):
                if p.tipo == "Vida":
                    vida = min(vida + 1, 5)

                if p.tipo == "Velocidade":
                    player.vel += 1

                if p.tipo == "Tiro":
                    player.cooldown = max(5, player.cooldown - 5)

                if p.tipo == "Multishot":
                    player.multishot = min(3, player.multishot + 1)

                powerups.remove(p)

        # desenhar tudo
        for inimigo in inimigos:
            inimigo.desenhar(tela)

        player.desenhar(tela)

        for tiro in tiros:
            tiro.desenhar(tela)

        for tiro in tiros_inimigos:
            tiro.desenhar(tela)

        for explosao in explosões:
            explosao.desenhar(tela)

        for p in powerups:
            p.desenhar(tela)

        texto_score = fonte.render(f"score: {score}", True, (255, 255, 255))
        tela.blit(texto_score, (10, 40))

        cor = (0, 255, 0)
        if vida == 2:
            cor = (255, 255, 0)
        elif vida == 1:
            cor = (255, 0, 0)

        texto_vida = fonte.render(f"Vida: {vida}", True, cor)
        tela.blit(texto_vida, (10, 10))

        pygame.display.flip()

        player.mover(teclas, tiros)

        if vida <= 0:
            estado = "gamerover"

    # ================= GAME OVER =================
    elif estado == "gamerover":

        botao_reniciar = Botao(250, 300, 300, 60, "REINICIAR")
        botao_menu = Botao(250, 380, 300, 60, "MENU")

        tela.fill((0, 0, 0))

        texto = fonte.render("Game Over", True, (255, 0, 0))
        tela.blit(texto, (300, 250))

        if not score_salvo:
            db.save_score(nome, score)
            score_salvo = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if botao_reniciar.clicado(evento):
                resetar_jogo()
                estado = "jogando"

            elif botao_menu.clicado(evento):
                nome = ""
                senha = ""
                digitando_nome = True
                digitando_senha = False
                estado = "menu"
                pygame.event.clear()

        botao_reniciar.desenhar(tela, fonte)
        botao_menu.desenhar(tela, fonte)

        pygame.display.flip()

pygame.quit()