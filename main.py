import pygame
import random
import math
from classes import Player, Inimigo, Tiro, Tiro_inimigo, Explosão, Power_ups
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
nome = ""
senha = ""
digitando_nome = True
digitando_senha = False
piscar = 0 
estado = "menu"
rodando = True
def resetar_jogo():
    global tiros, tiros_inimigos, player, explosões, vida, score, inimigos, dificuldade, powerups, score_salvo, nome, digitando_nome, senha, digitando_senha
    tiros_inimigos = []
    inimigos = []
    explosões = []
    vida = 3
    score = 0
    dificuldade = 1
    powerups = []
    player = Player()
    score_salvo = False

while rodando:
    clock.tick(60)
    spawn_timer += 1

    if estado == "menu":

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

                            if resultado == "criado":
                                print("Conta criada")

                                estado = "jogando"

                            elif resultado == "login":
                                print("Login ok")
                            
                                estado = "jogando"


                            elif resultado == "erro":
                                print("Senha errada")
                    else:
                        if len(senha) < 10:
                            senha += evento.unicode


        tela.fill((10, 10, 10))
        piscar += 1

        texto_nick = fonte.render(f"Nick: {nome}", True, (255, 255, 255))
        tela.blit(texto_nick, (250, 150))

        senha_oculta = "*" * len(senha)
        texto_senha = fonte.render(f"Senha: {senha_oculta}", True, (255, 255, 255))
        tela.blit(texto_senha, (250, 260))


        botao_jogar = pygame.Rect(250, 70, 230, 60)
        pygame.draw.rect(tela, (50, 50, 200), botao_jogar)

        titulo = fonte_titulo.render("Quadradoxs", True, (255, 255, 0))
        tela.blit(titulo, (250, 100))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_jogar.collidepoint(evento.pos):
                resetar_jogo()
                estado = "jogando"


        if botao_jogar.collidepoint(mouse_pos):
            pygame.draw.rect(tela, (80, 140, 255), botao_jogar)


        texto_botao = fonte.render("JOGAR", True, (255, 255, 255))
        tela.blit(texto_botao, (330, 295))

        pygame.display.flip()

    elif estado == "jogando":

        tela.fill((0, 0, 0))
        rect_player = pygame.Rect(player.x, player.y, 50, 50)
        dificuldade = 1 + score // 100
        teclas = pygame.key.get_pressed()
        score_salvo = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

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
                        tipo = random.choice(["Vida", "Tiro"])
                        powerups.append(Power_ups(inimigo.x, inimigo.y, tipo))
                    break

                if rect_inimigo.colliderect(rect_player):
                    inimigos.remove(inimigo)
                    vida -= 1
                    explosões.append(Explosão(inimigo.x + 25, inimigo.y + 25))
                    break

        for tiro in tiros_inimigos[:]:
            tiro.mover()
            if tiro.y > 600:
                tiros_inimigos.remove(tiro)

        for tiro in tiros_inimigos[:]:
            rect_tiro_inimigo = pygame.Rect(tiro.x, tiro.y, 10, 20)
            if rect_tiro_inimigo.colliderect(rect_player):
                tiros_inimigos.remove(tiro)
                vida -= 1

        for inimigo in inimigos[:]:

            inimigo.atualizar()
            inimigo.y += 1

            if inimigo.y > 600:
                inimigos.remove(inimigo)
                vida -= 1
                explosões.append(Explosão(inimigo.x + 25, inimigo.y + 25))

            if inimigo.tipo == "basico":
                inimigo.mover()
                inimigo.atirar(player, tiros_inimigos, dificuldade)

            elif inimigo.tipo == "sniper":
                inimigo.atirar(player, tiros_inimigos, dificuldade)

            elif inimigo.tipo == "perseguidor":
                inimigo.seguir_player(player)
                inimigo.atirar(player, tiros_inimigos, dificuldade)

        for explosao in explosões[:]:
            explosao.atualizar()

            if explosao.tempo <= 0:
                explosões.remove(explosao)

        if spawn_timer > max(40, 150 - dificuldade * 10):
            x = random.randint(0, 750)
            spawn_timer = 0

            tipo = random.choice(["basico", "sniper", "perseguidor"])
            inimigo = Inimigo(x, 0, tipo)
            inimigo.vel_x += dificuldade
            inimigos.append(inimigo)

        for p in powerups[:]:
            if p.y > 600:
                powerups.remove(p)

        for p in powerups[:]:
            rect_p = pygame.Rect(p.x, p.y, 20, 20)
            p.mover()

            if rect_p.colliderect(rect_player):

                if p.tipo == "Vida":
                    vida += 1

                elif p.tipo == "Tiro":
                    player.cooldown = max(5, player.cooldown - 5)

                powerups.remove(p)

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

        texto_score = fonte.render(f"score:{score} ", True, (255, 255, 255))
        tela.blit(texto_score, (10, 40))

        cor = (0, 255, 0)
        if vida == 2:
            cor = (255, 255, 0)
        elif vida == 1:
            cor = (255, 0, 0)

        texto_vida = fonte.render(f"Vida: {vida}", True, cor)
        tela.blit(texto_vida, (10, 10))

        pygame.display.flip()

        teclas = pygame.key.get_pressed()
        player.mover(teclas, tiros)

        if vida <= 0:
            estado = "gamerover"

    elif estado == "gamerover":

        tela.fill((0, 0, 0))

        texto1 = fonte.render("Gamer over", True, (255, 0, 0))
        tela.blit(texto1, (300, 250))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        botao_reniciar = pygame.Rect(250, 300, 300, 60)


        botao_menu = pygame.Rect(250, 380, 300, 60)


        if not score_salvo:
            db.save_score(nome, score)
            score_salvo = True

        top = db.get_top_scores()


        


        cor_menu = (200, 200, 0)
        if botao_menu.collidepoint(mouse_pos):
            cor_menu = (255, 255, 0)
        pygame.draw.rect(tela, cor_menu, botao_menu)


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_reniciar.collidepoint(evento.pos):
                    resetar_jogo()
                    estado = "jogando"
                
                elif botao_menu.collidepoint(evento.pos):
                    nome = ""
                    digitando_nome = True
                    estado = "menu"
                    pygame.event.clear()


        mouse_pos = pygame.mouse.get_pos()
        cor_reniciar = (0, 200, 0)
        if botao_reniciar.collidepoint(mouse_pos):
            cor_reniciar = (0, 255, 0)

        pygame.draw.rect(tela, cor_reniciar, botao_reniciar )



        texto_botao_reniciar = fonte.render("Reniciar", True, (0, 0, 0))
        tela.blit(texto_botao_reniciar, (botao_reniciar.x + 90, botao_reniciar.y + 15))


        texto_botao_menu = fonte.render("Ir para o menu", True, (0, 0, 0))
        tela.blit(texto_botao_menu, (botao_menu.x + 110, botao_menu.y + 15))

        y = 200
        for nick, pontos in top:
            texto = fonte.render(f'{nick}  = {pontos}', True, (255, 255, 255))
            tela.blit(texto, (300, y))
            y += 40

        pygame.display.flip()

pygame.quit()