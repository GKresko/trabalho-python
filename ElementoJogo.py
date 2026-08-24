import pygame


class ElementoJogo:
    """Classe base (superclasse) de todos os objetos do jogo."""

    # refine as areas e posicoes usadas nas colisoes, bem como cor de desenho e 
    #pixels por frame (velocidade) de cada elemento do jogo.
    def __init__(self, x, y, largura, altura, cor=(255, 255, 255), velocidade=5):
        self.rect = pygame.Rect(x, y, largura, altura)  # area/posicao usada nas colisoes
        self.cor = cor                                  # cor de desenho
        self.velocidade = velocidade                    # pixels por frame

    def mover(self):
        """Movimentação: cada subclasse sobrescreve com sua própria regra."""
        pass

    def desenhar(self, tela):
        """Desenho padrão (retângulo); as subclasses sobrescrevem (polimorfismo)."""
        pygame.draw.rect(tela, self.cor, self.rect)
