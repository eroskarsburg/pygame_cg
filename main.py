import pygame
import sys
import time
import requests
import io

# Inicialização
pygame.init()
TILE_SIZE = 40
ROWS, COLS = 13, 30
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

# Mapa
level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWW", "W               WWWW      WWW",
    "W WWW WWWWWWW W WWWWWWWWW WWW", "W W   W     W W           WWW",
    "W W W W WWW W WWWWWW WWWWWWWW", "W W W W   W W     WW     WW W",
    "W WWWWWWWWW W WWW  W WWW WW W", "W           W WW   WWWWW    W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# Personagem
player = pygame.Rect(60, 60, TILE_SIZE - 10, TILE_SIZE - 10)

# Carregar imagem do jogador da internet
url = "https://i.ytimg.com/vi/6eax30dd-OQ/sddefault.jpg"
response = requests.get(url)
image_file = io.BytesIO(response.content)
player_img = pygame.image.load(image_file).convert_alpha()
player_img = pygame.transform.scale(player_img, (player.width, player.height))

player_speed = TILE_SIZE
bombs = []


# Funções
def draw_level():
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE,
                               TILE_SIZE)
            pygame.draw.rect(screen, GRAY if cell == "W" else WHITE, rect)


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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bx = (player.x + 5) // TILE_SIZE * TILE_SIZE
            by = (player.y + 5) // TILE_SIZE * TILE_SIZE
            bombs.append({
                "rect": pygame.Rect(bx, by, TILE_SIZE, TILE_SIZE),
                "time": time.time()
            })

    keys = pygame.key.get_pressed()
    move_x = move_y = 0
    if keys[pygame.K_LEFT]: move_x = -player_speed
    if keys[pygame.K_RIGHT]: move_x = player_speed
    if keys[pygame.K_UP]: move_y = -player_speed
    if keys[pygame.K_DOWN]: move_y = player_speed

    new_pos = player.move(move_x, move_y)
    if not is_wall((new_pos.x + 5, new_pos.y + 5)):
        player = new_pos

    for bomb in bombs[:]:
        pygame.draw.rect(screen, BLUE, bomb["rect"])
        if time.time() - bomb["time"] > 2:
            cx, cy = bomb["rect"].x, bomb["rect"].y
            pygame.draw.rect(screen, ORANGE, bomb["rect"])
            for dx, dy in [(TILE_SIZE, 0), (-TILE_SIZE, 0), (0, TILE_SIZE),
                           (0, -TILE_SIZE)]:
                expl_rect = pygame.Rect(cx + dx, cy + dy, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, RED, expl_rect)
            bombs.remove(bomb)

    screen.blit(player_img, player.topleft)
    pygame.display.flip()
    clock.tick(10)
