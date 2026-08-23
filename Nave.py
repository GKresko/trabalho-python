import pygame
from ElementoJogo import ElementoJogo


class Nave(ElementoJogo):
    """Nave do jogador: move na horizontal e dispara tiros para cima."""

    def __init__(self, largura_tela, altura_tela, velocidade=6, cor=(0, 255, 100)):
        # Herança: inicializa a classe base já centralizada na parte de baixo da tela
        super().__init__(
            x=largura_tela // 2 - 20,
            y=altura_tela - 60,
            largura=40,
            altura=40,
            cor=cor,
            velocidade=velocidade
        )
        self.largura_tela = largura_tela   # limite direito para travar o movimento
        self.altura_tela = altura_tela
        self.vel_x = 0                     # -vel (esquerda), 0 (parado), +vel (direita)
        self.tiros = []                    # lista de pygame.Rect com os tiros ativos

        # Parametros do disparo e da animacao do propulsor
        self.largura_tiro = 4
        self.altura_tiro = 10
        self.velocidade_tiro = 12          # pixels que o tiro sobe por frame
        self.frame_animacao = 0            # contador usado para "pulsar" a chama

    def processar_evento(self, evento):
        """Traduz as teclas do teclado em movimento e disparo."""
        if evento.type == pygame.KEYDOWN:          # tecla pressionada
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self.vel_x = -self.velocidade      # comeca a ir para a esquerda
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.vel_x = self.velocidade       # comeca a ir para a direita
            elif evento.key == pygame.K_SPACE:
                self.atirar()                      # 1 tiro por toque no espaco

        elif evento.type == pygame.KEYUP:          # tecla solta -> para de mover
            # Confere o sinal de vel_x para nao cancelar o movimento da outra tecla
            if evento.key in (pygame.K_LEFT, pygame.K_a) and self.vel_x < 0:
                self.vel_x = 0
            elif evento.key in (pygame.K_RIGHT, pygame.K_d) and self.vel_x > 0:
                self.vel_x = 0

    def mover(self):
        """Aplica o deslocamento horizontal e trava nas bordas da tela."""
        self.rect.x += self.vel_x

        if self.rect.left < 0:                          # bateu na borda esquerda
            self.rect.left = 0
        elif self.rect.right > self.largura_tela:       # bateu na borda direita
            self.rect.right = self.largura_tela

    def atirar(self):
        # =========================================================================
        # TODO 1 - RESOLVIDO
        # Cria um projétil (pygame.Rect) centralizado no topo da nave e o
        # adiciona à lista de tiros ativos.
        # =========================================================================
        # centerx menos metade da largura -> tiro alinhado ao centro da nave
        x_tiro = self.rect.centerx - self.largura_tiro // 2
        # top menos a altura -> o tiro nasce logo ACIMA da nave, sem sobrepor
        y_tiro = self.rect.top - self.altura_tiro

        tiro = pygame.Rect(x_tiro, y_tiro, self.largura_tiro, self.altura_tiro)
        self.tiros.append(tiro)  # entra na lista de tiros ativos

    def atualizar_tiros(self):
        # =========================================================================
        # TODO 2 - RESOLVIDO
        # Move cada tiro para cima e remove da lista (libera a memória) os que
        # saírem pelo topo da tela.
        # =========================================================================
        # O [:] cria uma COPIA da lista: sem isso, remover itens durante o laco
        # faria o Python pular o elemento seguinte.
        for tiro in self.tiros[:]:
            tiro.y -= self.velocidade_tiro  # y menor = mais para cima na tela

            if tiro.bottom < 0:             # saiu inteiro pelo topo
                self.tiros.remove(tiro)     # remove da memoria

    def atualizar(self):
        """Um passo da nave por frame: mover, atualizar tiros e animar."""
        self.mover()
        self.atualizar_tiros()
        self.frame_animacao = (self.frame_animacao + 1) % 12  # ciclo de 0 a 11

    # ------------------------------------------------------------------
    # BÔNUS: customização visual da nave (fuselagem, asas, canhões,
    # cabine e propulsor animado) em vez do triângulo simples.
    # ------------------------------------------------------------------
    def desenhar(self, tela):
        r = self.rect
        cx = r.centerx
        # Tons derivados da cor principal, para dar volume ao desenho
        cor_escura = tuple(int(c * 0.55) for c in self.cor)
        cor_clara = tuple(min(255, int(c * 0.4) + 140) for c in self.cor)

        # Propulsor: o tamanho varia com o frame, criando o efeito de chama viva
        tamanho_chama = 8 + (self.frame_animacao % 6)
        chama_externa = [                                  # chama laranja (maior)
            (cx - 7, r.bottom - 4),
            (cx + 7, r.bottom - 4),
            (cx, r.bottom - 4 + tamanho_chama)
        ]
        chama_interna = [                                  # nucleo amarelo (menor)
            (cx - 3, r.bottom - 4),
            (cx + 3, r.bottom - 4),
            (cx, r.bottom - 6 + tamanho_chama // 2)
        ]
        pygame.draw.polygon(tela, (255, 140, 30), chama_externa)
        pygame.draw.polygon(tela, (255, 235, 120), chama_interna)

        # Canhões laterais (dois retangulos verticais)
        pygame.draw.rect(tela, cor_escura, pygame.Rect(r.left + 3, r.top + 12, 4, 16))
        pygame.draw.rect(tela, cor_escura, pygame.Rect(r.right - 7, r.top + 12, 4, 16))

        # Asas: triangulos que saem do corpo em direcao as bordas de baixo
        asa_esquerda = [
            (cx - 8, r.top + 20),
            (r.left, r.bottom - 2),
            (cx - 6, r.bottom - 6)
        ]
        asa_direita = [
            (cx + 8, r.top + 20),
            (r.right, r.bottom - 2),
            (cx + 6, r.bottom - 6)
        ]
        pygame.draw.polygon(tela, cor_escura, asa_esquerda)
        pygame.draw.polygon(tela, cor_escura, asa_direita)

        # Fuselagem: corpo principal em forma de bico (5 vertices)
        fuselagem = [
            (cx, r.top),              # ponta da nave
            (cx + 9, r.top + 22),
            (cx + 6, r.bottom - 4),
            (cx - 6, r.bottom - 4),
            (cx - 9, r.top + 22)
        ]
        pygame.draw.polygon(tela, self.cor, fuselagem)       # preenchimento
        pygame.draw.polygon(tela, cor_clara, fuselagem, 2)   # contorno claro

        # Cabine do piloto
        pygame.draw.circle(tela, (150, 225, 255), (cx, r.top + 16), 5)
        pygame.draw.circle(tela, (40, 80, 110), (cx, r.top + 16), 5, 1)

        # Tiros ativos: halo ciano (rect um pouco maior) + nucleo branco
        for tiro in self.tiros:
            pygame.draw.rect(tela, (90, 220, 255), tiro.inflate(4, 4))
            pygame.draw.rect(tela, (255, 255, 255), tiro)
