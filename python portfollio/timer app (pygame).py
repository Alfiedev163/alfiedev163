import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

timer_seconds = 10  # 10 second timer
start_time = pygame.time.get_ticks()  # time when game started

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # work out how much time has passed
    current_time = pygame.time.get_ticks()
    elapsed_ms = current_time - start_time
    elapsed_seconds = elapsed_ms // 1000

    time_left = timer_seconds - elapsed_seconds
    if time_left < 0:
        time_left = 0

    # draw
    screen.fill((30, 30, 30))

    timer_text = font.render(f"Time left: {time_left}", True, (255, 255, 255))
    screen.blit(timer_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
