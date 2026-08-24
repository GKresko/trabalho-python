import math
import random
import pygame
from ElementoJogo import ElementoJogo


class Asteroid(ElementoJogo):
    """Asteroide que cai do topo da tela e aguenta 3 tiros antes de explodir."""

    # BÔNUS: cores por estágio de dano (cinza -> laranja -> vermelho)
    CORES_DANO = [
        (125, 128, 140),  # intacto
        (214, 126, 44),   # 1 tiro recebido
        (198, 52, 44)     # 2 tiros recebidos (o proximo tiro destroi)
    ]

    def __init__(self, largura_tela, altura_tela, velocidade=5, cor=(200, 50, 50)):
        self.largura_tela = largura_tela   # usado para sortear o X dentro da tela
        self.altura_tela = altura_tela     # usado para saber quando saiu por baixo
        self.raio = 20
        self.vida_maxima = 3               # quantos tiros aguenta

        # Herança: nasce em (0, 0); a posicao real e sorteada em iniciar_status()
        super().__init__(
            x=0,
            y=0,
            largura=self.raio * 2,
            altura=self.raio * 2,
            cor=cor,
            velocidade=velocidade
        )
        self.iniciar_status()

    def iniciar_status(self):
        # =========================================================================
        # TODO 3 - RESOLVIDO
        # Sorteia a posição horizontal (dentro da tela), a posição vertical
        # (acima do topo) e a velocidade de queda do asteroide.
        # =========================================================================
        # Limite = largura da tela menos a largura do asteroide, para nao passar da borda
        self.rect.x = random.randint(0, self.largura_tela - self.rect.width)
        self.rect.y = random.randint(-150, -50)   # y negativo = acima da tela
        self.velocidade = random.randint(3, 7)    # queda mais lenta ou mais rapida

        # --- BÔNUS: reseta vida, forma e rotação a cada novo surgimento ---
        self.vida = self.vida_maxima
        self.cor = self._cor_do_dano()                    # volta para o cinza
        self.angulo = random.uniform(0, math.tau)         # rotacao inicial
        self.vel_rotacao = random.uniform(-0.09, 0.09)    # sentido/velocidade do giro
        self.contorno = self._gerar_contorno()            # nova forma irregular
        self.crateras = self._gerar_crateras()            # novas crateras

    def receber_dano(self):
        """Aplica 1 ponto de dano. Retorna True se o asteroide foi destruído."""
        self.vida -= 1
        self.cor = self._cor_do_dano()  # muda de cor conforme a vida cai
        return self.vida <= 0

    def mover(self):
        """Cai na vertical e gira; se passar do fundo, reaparece no topo."""
        self.rect.y += self.velocidade
        self.angulo += self.vel_rotacao  # BÔNUS: rotação contínua

        # Reinicia no topo caso passe reto pelo fundo da tela
        if self.rect.top > self.altura_tela:
            self.iniciar_status()

    def desenhar(self, tela):
        # BÔNUS: polígono irregular rotacionado, com contorno e crateras
        pontos = [self._ponto_absoluto(dx, dy) for dx, dy in self.contorno]
        cor_escura = tuple(int(c * 0.55) for c in self.cor)               # crateras
        cor_clara = tuple(min(255, int(c * 1.35) + 20) for c in self.cor)  # contorno

        pygame.draw.polygon(tela, self.cor, pontos)     # corpo preenchido
        pygame.draw.polygon(tela, cor_clara, pontos, 2)  # borda iluminada

        for dx, dy, raio_cratera in self.crateras:
            centro = self._ponto_absoluto(dx, dy)        # cratera gira junto com a rocha
            pygame.draw.circle(tela, cor_escura, centro, raio_cratera)

    # ------------------------------------------------------------------
    # Métodos auxiliares (privados, por convenção o nome começa com _)
    # ------------------------------------------------------------------
    def _cor_do_dano(self):
        """Escolhe a cor da lista CORES_DANO conforme a vida restante."""
        # vida 3 -> indice 0 (cinza); vida 2 -> 1 (laranja); vida 1 ou 0 -> 2 (vermelho)
        indice = min(len(self.CORES_DANO) - 1, self.vida_maxima - self.vida)
        return self.CORES_DANO[indice]

        #gera o asteroide com formato irregular
    def _gerar_contorno(self):
        """Gera os vértices (relativos ao centro) de um polígono irregular."""
        lados = random.randint(9, 12)   #usa um random p verificar quantas vertices vai existir o asteroide
        pontos = []
        for i in range(lados):
            ang = math.tau * i / lados          # distribui os vertices no circulo
            fator = random.uniform(0.72, 1.0)   # "amassa" o raio -> forma irregular
            pontos.append((
                math.cos(ang) * self.raio * fator,
                math.sin(ang) * self.raio * fator
            ))
        return pontos

    def _gerar_crateras(self):
        """Gera crateras: deslocamento relativo ao centro + raio."""
        crateras = []
        for _ in range(random.randint(3, 5)):
            ang = random.uniform(0, math.tau)
            dist = random.uniform(0, self.raio * 0.5)  # mantem a cratera dentro da rocha
            crateras.append((
                math.cos(ang) * dist,
                math.sin(ang) * dist,
                random.randint(2, 5)
            ))
        return crateras

    def _ponto_absoluto(self, dx, dy):
        """Rotaciona um ponto relativo pelo ângulo atual e converte para a tela."""
        cos_a = math.cos(self.angulo)
        sen_a = math.sin(self.angulo)
        cx, cy = self.rect.center
        return (
            int(cx + dx * cos_a - dy * sen_a),  # matriz de rotacao 2D
            int(cy + dx * sen_a + dy * cos_a)
        )
