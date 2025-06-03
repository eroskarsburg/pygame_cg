import pygame
import sys
import time

# Inicialização
pygame.init()
TILE_SIZE = 40
ROWS, COLS = 13, 15
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Bomberman")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 150, 255)

# Mapa (W = parede, " " = espaço livre)
level = [
    "WWWWWWWWWWWWWWW",
    "W             W",
    "W WWW WWWWWWW W",
    "W W   W     W W",
    "W W W W WWW W W",
    "W W W W   W W W",
    "W WWWWWWWWW W W",
    "W           W W",
    "WWWWWWWWWWWWWWW"
]

# Personagem
player = pygame.Rect(60, 60, TILE_SIZE - 10, TILE_SIZE - 10)
player_speed = TILE_SIZE

# Bombas
bombs = []

# Funções utilitárias
def draw_level():
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if cell == "W":
                pygame.draw.rect(screen, GRAY, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

def is_wall(pos):
    x, y = pos
    col, row = x // TILE_SIZE, y // TILE_SIZE
    try:
        return level[row][col] == "W"
    except IndexError:
        return True

# Loop principal
while True:
    screen.fill(WHITE)
    draw_level()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Colocar bomba
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bx = (player.x + 5) // TILE_SIZE * TILE_SIZE
            by = (player.y + 5) // TILE_SIZE * TILE_SIZE
            bombs.append({"rect": pygame.Rect(bx, by, TILE_SIZE, TILE_SIZE), "time": time.time()})

    # Movimento
    keys = pygame.key.get_pressed()
    move_x = move_y = 0
    if keys[pygame.K_LEFT]:
        move_x = -player_speed
    if keys[pygame.K_RIGHT]:
        move_x = player_speed
    if keys[pygame.K_UP]:
        move_y = -player_speed
    if keys[pygame.K_DOWN]:
        move_y = player_speed

    # Atualizar posição se não colidir com parede
    new_pos = player.move(move_x, move_y)
    if not is_wall((new_pos.x + 5, new_pos.y + 5)):
        player = new_pos

    # Atualizar bombas
    for bomb in bombs[:]:
        pygame.draw.rect(screen, BLUE, bomb["rect"])
        if time.time() - bomb["time"] > 2:  # 2 segundos até explodir
            # Desenhar explosão
            cx, cy = bomb["rect"].x, bomb["rect"].y
            pygame.draw.rect(screen, ORANGE, bomb["rect"])  # centro
            for dx, dy in [(TILE_SIZE, 0), (-TILE_SIZE, 0), (0, TILE_SIZE), (0, -TILE_SIZE)]:
                expl_rect = pygame.Rect(cx + dx, cy + dy, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, RED, expl_rect)
            bombs.remove(bomb)

    # Desenhar jogador
    pygame.draw.rect(screen, (0, 200, 0), player)

    pygame.display.flip()
    clock.tick(10)
