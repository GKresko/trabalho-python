#importação das bibliotecas necessárias
import random
import pygame
from Nave import Nave #import da classe nave asterior e explosão, que obviamente foi chamada na main
from Asteroid import Asteroid 
from Explosao import Explosao

#criação da classe 'jogo',
class Jogo:
    """Controlador do jogo: guarda os elementos e roda o loop principal."""

    def __init__(self, largura=800, altura=600): #metodo construtor da classe
        #recebendo altura = 600 e largura = 800, por padrão para criar a tela do jogo
        pygame.init()  # liga os modulos do pygame
        self.largura = largura #self = valor recebido será guardado no largura, pelo self.largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))  # cria a janela do jogo
        pygame.display.set_caption("Space Shooter - POO com Pygame") #método do pygame

        self.clock = pygame.time.Clock()  # controla a taxa de quadros
        self.fps = 60                     # quadros por segundo
        self.rodando = True               # False encerra o programa
        self.pontos = 0
        self.fim_de_jogo = False          # True congela a partida e mostra o placar

        self.fonte = pygame.font.SysFont("consolas", 22, bold=True)
        self.fonte_grande = pygame.font.SysFont("consolas", 48, bold=True)

        # Fundo estrelado (bônus visual): posicoes sorteadas uma unica vez
        self.estrelas = [
            (random.randint(0, largura), random.randint(0, altura), random.randint(1, 2))
            for _ in range(90)
        ]
        #.random = valores aleatorios
        # randint = retorna um valor inteiro aleatorio entre os valores passados como parametro
        # range = retorna uma sequencia de numeros, nesse caso de 0 a 90

        # Elementos do jogo
        self.nave = Nave(self.largura, self.altura) 
        #instanciando nave + asteroide, passando largura e altura da tela como parametro
        self.asteroide = Asteroid(self.largura, self.altura)
        self.explosoes = []  # efeitos visuais ativos

    # método p reiniciar partida, mantendo a janela aberta
    def reiniciar(self):
        """Reinicia a partida do zero, mantendo a janela aberta."""
        self.pontos = 0 #reiniciar sem fechar/abrir
        self.fim_de_jogo = False #pontuacao zerada, fim de jogo falso
        self.nave = Nave(self.largura, self.altura) #instanciando nave + 
        # asteroide, passando largura e altura da tela como parametro
        self.asteroide = Asteroid(self.largura, self.altura) #instanciando asteroide
        self.explosoes = [] #instanciando explosoes


#leitura de todos os eventos do game (teclas e movimentações do usuário) 
    def processar_eventos(self):
        """Lê a fila de eventos do pygame (fechar janela, teclado)."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:        # clicou no X da janela, encerrando o jogo
                self.rodando = False
                continue

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.rodando = False              # ESC sai a qualquer momento
                continue

            if self.fim_de_jogo:
                # Na tela de fim de jogo, so a tecla R tem efeito
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    self.reiniciar()
                continue

            self.nave.processar_evento(evento)    # repassa a tecla para a nave

    def checar_colisoes(self):
        # =========================================================================
        # TODO 4 - RESOLVIDO
        # A) Tiro vs Asteroide  B) Asteroide vs Nave
        # =========================================================================

        # A) Tiro vs Asteroide
        for tiro in self.nave.tiros[:]:                     # copia da lista (ver TODO 2)
            if tiro.colliderect(self.asteroide.rect):       # os retangulos se sobrepoem?
                self.nave.tiros.remove(tiro)                # 1. remove o tiro
                self.pontos += 1                            # 3. soma pontuacao

                # BÔNUS: o asteroide só é resetado quando a vida acaba,
                # trocando de cor a cada tiro recebido.
                if self.asteroide.receber_dano():           # True = foi destruido
                    self.explosoes.append(  
                    #append sendo usado p inserir explosão na lista de explosões
                    #append = inserir elemento no final da lista
                        Explosao(self.asteroide.rect.center, self.asteroide.raio)
                    )
                    self.asteroide.iniciar_status()         # 2. reseta o asteroide
                    self.pontos += 5                        # bonus por destruicao

        # B) Asteroide vs Nave
        if self.nave.rect.colliderect(self.asteroide.rect):
            self.explosoes.append(Explosao(self.nave.rect.center, 26))
            self.fim_de_jogo = True                         # encerra a partida

    def atualizar(self):
        """Avança um frame de toda a lógica do jogo."""
        for explosao in self.explosoes[:]:  #self.explosoes = explosao sendo atualizada
            # pois o self = representa o próprio objeto que está usando aquele método
            explosao.atualizar()
            if explosao.terminou:
                self.explosoes.remove(explosao)  # limpa efeitos que acabaram

        if self.fim_de_jogo:
            return  # congela nave e asteroide, mas as explosoes acima continuam

        self.nave.atualizar()
        self.asteroide.mover()
        self.checar_colisoes()

    def desenhar_hud(self):
        """Desenha o placar e as informações na tela."""
        texto_pontos = self.fonte.render(f"Pontos: {self.pontos}", True, (235, 235, 245))
        #.render = transforma texto em imagem
        self.tela.blit(texto_pontos, (16, 14))
        #blit = coloca a imagem na tela, na posicao '16, 14' 
        # Barra de vida do asteroide: quadrado cheio = vida restante
        rotulo = self.fonte.render("Asteroide:", True, (150, 155, 170))
        self.tela.blit(rotulo, (16, 42))
        for i in range(self.asteroide.vida_maxima):
            barra = pygame.Rect(140 + i * 22, 46, 16, 12)
            if i < self.asteroide.vida:
                pygame.draw.rect(self.tela, self.asteroide.cor, barra)  # cheio
            else:
                pygame.draw.rect(self.tela, (60, 62, 74), barra, 1)     # vazio

        # Controles no topo a direita, longe da nave
        ajuda = self.fonte.render("<- ->  mover    ESPACO  atirar    ESC  sair",
                                  True, (110, 115, 130))
        self.tela.blit(ajuda, (self.largura - ajuda.get_width() - 16, 14))

    def desenhar_fim_de_jogo(self):
        """Escurece a tela e mostra o placar final."""
        veu = pygame.Surface((self.largura, self.altura))
        veu.set_alpha(170)              # transparencia do veu
        veu.fill((10, 10, 18))
        self.tela.blit(veu, (0, 0))

        titulo = self.fonte_grande.render("FIM DE JOGO", True, (240, 80, 70))
        placar = self.fonte.render(f"Pontuacao final: {self.pontos}", True, (235, 235, 245))
        dica = self.fonte.render("R para jogar de novo    ESC para sair", True, (170, 175, 190))

        # get_rect(center=...) centraliza o texto na horizontal
        self.tela.blit(titulo, titulo.get_rect(center=(self.largura // 2, self.altura // 2 - 40)))
        self.tela.blit(placar, placar.get_rect(center=(self.largura // 2, self.altura // 2 + 15)))
        self.tela.blit(dica, dica.get_rect(center=(self.largura // 2, self.altura // 2 + 55)))

    def desenhar(self):
        """A cada repetição do jogo, o quadro inteiro é desenhado do zero, de trás para frente"""
        self.tela.fill((15, 15, 25))  # limpa a tela (fundo do espaco)

        for x, y, tam in self.estrelas:
            pygame.draw.circle(self.tela, (90, 95, 120), (x, y), tam)

        # Polimorfismo: cada elemento sabe se desenhar do seu jeito
        self.nave.desenhar(self.tela)
        self.asteroide.desenhar(self.tela)

        for explosao in self.explosoes:
            explosao.desenhar(self.tela)

        self.desenhar_hud()

        if self.fim_de_jogo:
            self.desenhar_fim_de_jogo()  # por cima de tudo

        pygame.display.flip()  # joga o quadro pronto na janela

    def executar(self):
        """Loop principal: repete processar -> atualizar -> desenhar."""
        while self.rodando:
            self.clock.tick(self.fps)  # espera para nao passar de 60 FPS
            self.processar_eventos()
            self.atualizar()
            self.desenhar()

        pygame.quit()  # fecha a janela e libera os recursos


if __name__ == "__main__":  # so executa se este arquivo for o principal
    jogo = Jogo()
    jogo.executar()
