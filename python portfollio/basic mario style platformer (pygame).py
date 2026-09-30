import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

MENU = 0
GAME = 1
DEATH = 2
WIN = 3
state = MENU

current_level = 0
lives = 3
score = 0

TILE_SIZE = 40
FLOOR_Y = 7 * TILE_SIZE  # 280

LEVELS = [
    {
        "map": [
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "11111111111111111111"
        ],
        "coins": [
            (150, FLOOR_Y - 20),
            (250, FLOOR_Y - 20),
            (350, FLOOR_Y - 20)
        ],
        "enemies": [
            (200, FLOOR_Y - 40),
        ],
        "goal": (500, FLOOR_Y - 200, 40, 200)
    },
    {
        "map": [
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "11111111111111111111"
        ],
        "coins": [
            (150, FLOOR_Y - 20),
            (250, FLOOR_Y - 20),
            (350, FLOOR_Y - 20),
            (450, FLOOR_Y - 20)
        ],
        "enemies": [
            (200, FLOOR_Y - 40),
            (350, FLOOR_Y - 40)
        ],
        "goal": (600, FLOOR_Y - 200, 40, 200)
    }
]

player = pygame.Rect(100, 100, 40, 50)
player_speed = 5
player_vel_y = 0
gravity = 0.5
jump_power = -12
on_ground = False

tiles = []
coins = []
enemies = []
goal = pygame.Rect(0, 0, 40, 200)
enemy_speed = 2

def load_level(index):
    global tiles, coins, enemies, goal, player, player_vel_y
    level = LEVELS[index]

    tiles = []
    for y, row in enumerate(level["map"]):
        for x, tile in enumerate(row):
            if tile == "1":
                tiles.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    coins = [pygame.Rect(x, y, 20, 20) for (x, y) in level["coins"]]
    enemies = [pygame.Rect(x, y, 40, 40) for (x, y) in level["enemies"]]

    gx, gy, gw, gh = level["goal"]
    goal = pygame.Rect(gx, gy, gw, gh)

    player.x, player.y = 100, 100
    player_vel_y = 0

load_level(current_level)

font_big = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 30)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if state == MENU:
        screen.fill((0, 0, 0))
        title = font_big.render("MARIO-STYLE PLATFORMER", True, (255, 255, 255))
        prompt = font_small.render("Press SPACE to start", True, (200, 200, 200))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2))

        if keys[pygame.K_SPACE]:
            lives = 3
            score = 0
            current_level = 0
            load_level(current_level)
            state = GAME

        pygame.display.flip()
        clock.tick(60)
        continue

    if state == DEATH:
        screen.fill((0, 0, 0))
        msg = font_big.render("YOU DIED", True, (255, 0, 0))
        info = font_small.render("Press SPACE to continue", True, (255, 255, 255))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 60))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2))

        if keys[pygame.K_SPACE]:
            if lives > 0:
                load_level(current_level)
                state = GAME
            else:
                state = MENU

        pygame.display.flip()
        clock.tick(60)
        continue

    if state == WIN:
        screen.fill((0, 0, 0))
        msg = font_big.render("YOU WIN!", True, (0, 255, 0))
        info = font_small.render("Press SPACE to return to menu", True, (255, 255, 255))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 60))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2))

        if keys[pygame.K_SPACE]:
            state = MENU

        pygame.display.flip()
        clock.tick(60)
        continue

    if state == GAME:
        if keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_d]:
            player.x += player_speed

        if keys[pygame.K_SPACE] and on_ground:
            player_vel_y = jump_power
            on_ground = False

        player_vel_y += gravity
        player.y += player_vel_y

        on_ground = False
        for tile in tiles:
            if player.colliderect(tile):
                if player_vel_y > 0:
                    player.bottom = tile.top
                    player_vel_y = 0
                    on_ground = True
                elif player_vel_y < 0:
                    player.top = tile.bottom
                    player_vel_y = 0

        camera_x = player.x - WIDTH // 2

        for enemy in enemies[:]:
            enemy.x += enemy_speed
            for tile in tiles:
                if enemy.colliderect(tile):
                    enemy_speed *= -1

            if player.colliderect(enemy):
                if player_vel_y > 0:
                    enemies.remove(enemy)
                    player_vel_y = jump_power / 2
                    score += 100
                else:
                    lives -= 1
                    state = DEATH

        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                score += 10

        if player.colliderect(goal):
            current_level += 1
            if current_level >= len(LEVELS):
                state = WIN
            else:
                load_level(current_level)

        screen.fill((135, 206, 235))

        for tile in tiles:
            pygame.draw.rect(screen, (100, 100, 100),
                             pygame.Rect(tile.x - camera_x, tile.y, tile.width, tile.height))

        for coin in coins:
            pygame.draw.rect(screen, (255, 255, 0),
                             pygame.Rect(coin.x - camera_x, coin.y, coin.width, coin.height))

        for enemy in enemies:
            pygame.draw.rect(screen, (200, 50, 50),
                             pygame.Rect(enemy.x - camera_x, enemy.y, enemy.width, enemy.height))

        pygame.draw.rect(screen, (0, 255, 0),
                         pygame.Rect(goal.x - camera_x, goal.y, goal.width, goal.height))

        pygame.draw.rect(screen, (255, 50, 50),
                         pygame.Rect(player.x - camera_x, player.y, player.width, player.height))

        hud_score = font_small.render(f"Score: {score}", True, (0, 0, 0))
        hud_level = font_small.render(f"Level: {current_level + 1}", True, (0, 0, 0))
        hud_lives = font_small.render(f"Lives: {lives}", True, (0, 0, 0))
        screen.blit(hud_score, (10, 10))
        screen.blit(hud_level, (10, 35))
        screen.blit(hud_lives, (10, 60))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
