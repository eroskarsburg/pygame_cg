import pygame
import sys
import time
import requests
import io
import math

# Mapa
level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
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
HUD_HEIGHT = 60
HEIGHT = ROWS * TILE_SIZE + HUD_HEIGHT
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
player = pygame.Rect(45, 45 + HUD_HEIGHT, TILE_SIZE - 10, TILE_SIZE - 10)
player2 = pygame.Rect(WIDTH - 2 * TILE_SIZE + 5, 45 + HUD_HEIGHT, TILE_SIZE - 10, TILE_SIZE - 10)

# Imagem do jogador
url = "https://media-photos.depop.com/b1/5754313/2034110705_e4f1b78520f242ed872deb783e159acf/P0.jpg"
response = requests.get(url)
image_file = io.BytesIO(response.content)
player_img = pygame.image.load(image_file).convert_alpha()
player_img = pygame.transform.scale(player_img, (player.width, player.height))

# Imagem do segundo jogador
url2 = "https://i.ytimg.com/vi/6eax30dd-OQ/sddefault.jpg"
response = requests.get(url2)
image_file2 = io.BytesIO(response.content)
player2_img = pygame.image.load(image_file2).convert_alpha()
player2_img = pygame.transform.scale(player2_img, (player2.width, player2.height))

# Imagem da bomba
bomb_url = "https://cdn-icons-png.flaticon.com/512/112/112683.png"
response = requests.get(bomb_url)
bomb_file = io.BytesIO(response.content)
bomb_img = pygame.image.load(bomb_file).convert_alpha()
bomb_img = pygame.transform.scale(bomb_img, (TILE_SIZE, TILE_SIZE))

# Imagem de coração (vida)
heart_url = "https://cdn-icons-png.flaticon.com/512/833/833472.png"
response = requests.get(heart_url)
heart_file = io.BytesIO(response.content)
heart_img = pygame.image.load(heart_file).convert_alpha()
heart_img = pygame.transform.scale(heart_img, (30, 30))

player_speed = TILE_SIZE
bombs = []
explosions = []
vidas = 3
vidas2 = 3

# Funções
def draw_level():
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + HUD_HEIGHT, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY if cell == "W" else WHITE, rect)


def is_bomb(pos):
    x, y = pos
    px = x // TILE_SIZE * TILE_SIZE
    py = (y - HUD_HEIGHT) // TILE_SIZE * TILE_SIZE + HUD_HEIGHT
    for bomb in bombs:
        if bomb["pos"] == (px, py):
            return True
    return False


def is_wall(pos):
    x, y = pos
    col = x // TILE_SIZE
    row = (y - HUD_HEIGHT) // TILE_SIZE  # subtrai a altura da HUD para alinhar com o mapa
    try:
        return level[row][col] == "W"
    except IndexError:
        return True


def mostrar_vencedor(vencedor):
    fonte = pygame.font.SysFont(None, 60)
    msg1 = fonte.render(f"{vencedor} venceu!", True, BLUE)
    msg2 = pygame.font.SysFont(None, 40).render("Pressione R para reiniciar ou ESC para sair", True, (0, 0, 0))

    screen.fill((255, 255, 255))
    screen.blit(msg1, ((WIDTH - msg1.get_width()) // 2, HEIGHT // 2 - 60))
    screen.blit(msg2, ((WIDTH - msg2.get_width()) // 2, HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# Loop principal
while True:
    screen.fill(WHITE)
    # HUD
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, HUD_HEIGHT))  # fundo cinza

    # Mostrar vidas do player 1
    for i in range(vidas):
        screen.blit(heart_img, (10 + i * 40, 15))

    # Mostrar vidas do player 2
    for i in range(vidas2):
        screen.blit(heart_img, (WIDTH - (i + 1) * 40 - 10, 15))

    draw_level()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Jogador 1 coloca bomba com ESPAÇO
            if event.key == pygame.K_SPACE:
                if len(bombs) < 10:
                    bx = player.x // TILE_SIZE * TILE_SIZE
                    by = (player.y - HUD_HEIGHT) // TILE_SIZE * TILE_SIZE + HUD_HEIGHT
                    bomb_pos = (bx, by)
                    if all(bomb["pos"] != bomb_pos for bomb in bombs):
                        bombs.append({
                            "rect": pygame.Rect(bx, by, TILE_SIZE, TILE_SIZE),
                            "time": time.time(),
                            "pos": bomb_pos,
                            "owner": "p1"
                        })

            # Jogador 2 coloca bomba com tecla E
            if event.key == pygame.K_e:
                if len(bombs) < 10:
                    bx = player2.x // TILE_SIZE * TILE_SIZE
                    by = (player2.y - HUD_HEIGHT) // TILE_SIZE * TILE_SIZE + HUD_HEIGHT
                    bomb_pos = (bx, by)
                    if all(bomb["pos"] != bomb_pos for bomb in bombs):
                        bombs.append({
                            "rect": pygame.Rect(bx, by, TILE_SIZE, TILE_SIZE),
                            "time": time.time(),
                            "pos": bomb_pos,
                            "owner": "p2"
                        })


     # Movimento do player 1
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

    # Movimento do player 2 (WASD)
    move2_x = move2_y = 0
    if keys[pygame.K_a]: move2_x = -player_speed
    if keys[pygame.K_d]: move2_x = player_speed
    if keys[pygame.K_w]: move2_y = -player_speed
    if keys[pygame.K_s]: move2_y = player_speed

    new_pos2 = player2.move(move2_x, move2_y)
    new_center2 = (new_pos2.x + player2.width // 2, new_pos2.y + player2.height // 2)
    if not is_wall(new_center2) and not is_bomb(new_center2):
        player2 = new_pos2

    if not is_wall(new_center) and not is_bomb(new_center):
        player = new_pos

    for bomb in bombs[:]:
        elapsed = time.time() - bomb["time"]

        if elapsed > 5:
            # Gera explosão
            bx, by = bomb["pos"]
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            explosions.append({
                "rect": pygame.Rect(bx, by, TILE_SIZE, TILE_SIZE),
                "time": time.time(),
                "damaged": False
            })

            for dx, dy in directions:
                for i in range(1, 4):
                    nx = bx + dx * TILE_SIZE * i
                    ny = by + dy * TILE_SIZE * i
                    if is_wall((nx + TILE_SIZE // 2, ny + TILE_SIZE // 2)):
                        break
                    explosions.append({
                        "rect": pygame.Rect(nx, ny, TILE_SIZE, TILE_SIZE),
                        "time": time.time(),
                        "damaged": False
                    })

            bombs.remove(bomb)
            continue

        # Animação de escala usando seno
        scale_factor = 1 + 0.1 * math.sin(elapsed * 5)
        scaled_size = int(TILE_SIZE * scale_factor)
        scaled_bomb = pygame.transform.scale(bomb_img, (scaled_size, scaled_size))

        bx, by = bomb["rect"].topleft
        offset_x = (TILE_SIZE - scaled_size) // 2
        offset_y = (TILE_SIZE - scaled_size) // 2
        screen.blit(scaled_bomb, (bx + offset_x, by + offset_y))

    for explosion in explosions[:]:
        if time.time() - explosion["time"] > 0.4:
            explosions.remove(explosion)
            continue
        pygame.draw.rect(screen, ORANGE, explosion["rect"])

    for explosion in explosions:
        if not explosion["damaged"]:
            if explosion["rect"].colliderect(player):
                vidas -= 1
                explosion["damaged"] = True
            elif explosion["rect"].colliderect(player2):
                vidas2 -= 1
                explosion["damaged"] = True

    if vidas <= 0:
        if mostrar_vencedor("Jogador 2"):
            vidas = vidas2 = 3
            player.x, player.y = 45, 45 + HUD_HEIGHT
            player2.x, player2.y = WIDTH - 2*TILE_SIZE + 5, 45 + HUD_HEIGHT
            bombs.clear()
            explosions.clear()
            continue

    if vidas2 <= 0:
        if mostrar_vencedor("Jogador 1"):
            vidas = vidas2 = 3
            player.x, player.y = 45, 45 + HUD_HEIGHT
            player2.x, player2.y = WIDTH - 2*TILE_SIZE + 5, 45 + HUD_HEIGHT
            bombs.clear()
            explosions.clear()
            continue

    screen.blit(player_img, player.topleft)
    screen.blit(player2_img, player2.topright)
    pygame.display.flip()
    clock.tick(10)
