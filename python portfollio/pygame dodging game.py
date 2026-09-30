import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(300, 350, 40, 40)
speed = 5

enemies = []
enemy_speed = 4

def spawn_enemy():
    x = random.randint(0, WIDTH - 40)
    enemies.append(pygame.Rect(x, -40, 40, 40))

running = True
spawn_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= speed
    if keys[pygame.K_d]:
        player.x += speed

    spawn_timer += 1
    if spawn_timer > 30:
        spawn_enemy()
        spawn_timer = 0

    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.colliderect(player):
            print("Game Over!")
            running = False

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (0, 150, 255), player)

    for enemy in enemies:
        pygame.draw.rect(screen, (255, 50, 50), enemy)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
