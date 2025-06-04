import pygame
import sys
import time
import requests
import io

# Mapa
level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W     W     W       W     W     W     W",
    "W WWW W WWW W WWWWW W WWW W WWW W WWW W",
    "W W   W   W     W   W W   W W   W W   W",
    "W W WWWWW WWWWW W WWW W WWW W WWW W W W",
    "W W     W     W W     W     W       W W",
    "W WWWWW W WWW W WWWWW   WWWWW W W W W W",
    "W     W W   W W       W       W W W W W",
    "WWWWW W WWW W WWWWWWW W WWWWW W W W W W",
    "W     W             W W     W W   W   W",
    "W WWWWW W WWW W WWW W WWWWW W WWWWWWWWW",
    "W       W     W W   W     W W         W",
    "WWWWWWW W WWWWW W WWWWWWW W WWWWW WWW W",
    "W       W     W W     W   W       W   W",
    "W WWWWWWW WWWWW WWWWW W WWWWWWWWW W W W",
    "W     W             W W         W W W W",
    "W WWW W WWWWWWW W W W W WWWWWWW W W W W",
    "W W   W       W W W               W W W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# Inicialização
pygame.init()
TILE_SIZE = 40
ROWS, COLS = len(level), len(level[0])
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boomberman Game")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 150, 255)

# Personagem
player = pygame.Rect(60, 60, TILE_SIZE - 10, TILE_SIZE - 10)

# Imagem do jogador
url = "https://i.ytimg.com/vi/6eax30dd-OQ/sddefault.jpg"
response = requests.get(url)
image_file = io.BytesIO(response.content)
player_img = pygame.image.load(image_file).convert_alpha()
player_img = pygame.transform.scale(player_img, (player.width, player.height))

# Imagem da bomba
bomb_url = "https://cdn-icons-png.flaticon.com/512/112/112683.png"
response = requests.get(bomb_url)
bomb_file = io.BytesIO(response.content)
bomb_img = pygame.image.load(bomb_file).convert_alpha()
bomb_img = pygame.transform.scale(bomb_img, (TILE_SIZE, TILE_SIZE))

player_speed = TILE_SIZE
bombs = []


# Funções
def draw_level():
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE,
                               TILE_SIZE)
            pygame.draw.rect(screen, GRAY if cell == "W" else WHITE, rect)


def is_bomb(pos):
    x, y = pos
    px = x // TILE_SIZE * TILE_SIZE
    py = y // TILE_SIZE * TILE_SIZE
    for bomb in bombs:
        if bomb["pos"] == (px, py):
            return True
    return False


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
            # Garante que só uma bomba por tile seja colocada
            bx = player.x // TILE_SIZE * TILE_SIZE
            by = player.y // TILE_SIZE * TILE_SIZE
            bomb_pos = (bx, by)

            # Verifica se já existe bomba nesse local
            if all(bomb["pos"] != bomb_pos for bomb in bombs):
                bombs.append({
                    "rect": pygame.Rect(bx, by, TILE_SIZE, TILE_SIZE),
                    "time": time.time(),
                    "pos": bomb_pos
                })

    keys = pygame.key.get_pressed()
    move_x = move_y = 0
    if keys[pygame.K_LEFT]: move_x = -player_speed
    if keys[pygame.K_RIGHT]: move_x = player_speed
    if keys[pygame.K_UP]: move_y = -player_speed
    if keys[pygame.K_DOWN]: move_y = player_speed

    new_pos = player.move(move_x, move_y)
    new_center = (new_pos.x + player.width // 2, new_pos.y + player.height // 2)

    if not is_wall(new_center) and not is_bomb(new_center):
        player = new_pos

    for bomb in bombs[:]:
        screen.blit(bomb_img, bomb["rect"].topleft)
        if time.time() - bomb["time"] > 5:  # 5 segundos
            bombs.remove(bomb)

    screen.blit(player_img, player.topleft)
    pygame.display.flip()
    clock.tick(10)
