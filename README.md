# Space Shooter - Pygame + POO

Implementação dos 4 TODOs do projeto base + itens de bônus.

## Como rodar

```
python Main.py
```

Ambiente já instalado nesta máquina: Python 3.12.10 e pygame 2.6.1
(`python -m pip install pygame` caso precise reinstalar).

Controles: `<-` `->` (ou `A`/`D`) movem a nave, `ESPACO` atira, `ESC` sai,
`R` reinicia após o fim de jogo.

## TODOs implementados

| TODO | Arquivo             | Método              | O que foi feito                                                                 |
|------|---------------------|---------------------|---------------------------------------------------------------------------------|
| 1    | `Nave.py`           | `atirar()`          | Cria um `pygame.Rect(centerx - 2, top - 10, 4, 10)` e o adiciona a `self.tiros` |
| 2    | `Nave.py`           | `atualizar_tiros()` | Sobe cada tiro em 12 px/frame e remove da lista os que têm `bottom < 0`         |
| 3    | `Asteroid.py`       | `iniciar_status()`  | Sorteia `x` dentro da tela, `y` entre -150 e -50 e velocidade entre 3 e 7       |
| 4    | `Main.py`           | `checar_colisoes()` | (A) tiro x asteroide: remove tiro, aplica dano/reset e pontua. (B) asteroide x nave: fim de jogo |

Observação sobre o TODO 2: a remoção é feita iterando sobre uma **cópia** da lista
(`self.nave.tiros[:]`), evitando pular elementos ao remover durante o laço.

## Bônus

- **Nave customizada**: fuselagem poligonal, asas, dois canhões laterais, cabine
  e propulsor com chama animada (`Nave.desenhar`).
- **Asteroide customizado**: polígono irregular gerado aleatoriamente a cada
  surgimento, com crateras e rotação contínua (`Asteroid.desenhar` / `_gerar_contorno`).
- **Dano gradual com mudança visual**: 3 pontos de vida com troca de cor
  cinza -> laranja -> vermelho (`Asteroid.CORES_DANO` / `receber_dano`).
- **Explosão**: efeito de anel de choque + estilhaços ao destruir o asteroide
  (`Explosao.py`).
- **Extras**: fundo estrelado, HUD com pontuação e barra de vida do asteroide,
  tela de fim de jogo com reinício.

## Alteração fora dos TODOs

`Main.py`: `self.fps` foi alterado de `10` para `60`. Com 10 FPS o jogo fica
travado e o disparo praticamente não é visível; as velocidades dos elementos
foram mantidas como o enunciado pede.
