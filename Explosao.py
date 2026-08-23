import math
import random
import pygame


class Explosao:
    """BÔNUS: efeito visual de explosão exibido quando o asteroide é destruído."""

    def __init__(self, centro, raio_base=20, duracao=18):
        self.centro = centro          # onde a explosao acontece
        self.raio_base = raio_base    # tamanho inicial do anel
        self.duracao = duracao        # quantos frames o efeito dura
        self.frame = 0                # frame atual do efeito
        self.particulas = []

        # Cria estilhacos saindo do centro em direcoes aleatorias
        for _ in range(14):
            ang = random.uniform(0, math.tau)     # direcao
            vel = random.uniform(2.0, 6.0)        # velocidade
            self.particulas.append({
                "x": float(centro[0]),
                "y": float(centro[1]),
                "vx": math.cos(ang) * vel,        # decompoe a velocidade em X
                "vy": math.sin(ang) * vel,        # e em Y
                "tam": random.randint(2, 4)
            })

    @property
    def terminou(self):
        """True quando o efeito acabou e pode ser removido da lista."""
        return self.frame >= self.duracao

    def atualizar(self):
        """Avança um frame e move os estilhaços."""
        self.frame += 1
        for p in self.particulas:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vx"] *= 0.94   # atrito: os estilhacos vao desacelerando
            p["vy"] *= 0.94

    def desenhar(self, tela):
        progresso = self.frame / self.duracao  # 0.0 no inicio, quase 1.0 no fim

        # Anel de choque: cresce e vai afinando/escurecendo conforme o progresso
        raio = int(self.raio_base * (1 + progresso * 1.8))
        espessura = max(1, int(4 * (1 - progresso)))
        cor_anel = (255, int(200 - 140 * progresso), 60)
        pygame.draw.circle(tela, cor_anel, self.centro, raio, espessura)

        # Estilhacos: diminuem e esfriam de cor ao longo do efeito
        cor_particula = (255, int(230 - 150 * progresso), int(120 - 100 * progresso))
        for p in self.particulas:
            tam = max(1, int(p["tam"] * (1 - progresso)))
            pygame.draw.circle(tela, cor_particula, (int(p["x"]), int(p["y"])), tam)
