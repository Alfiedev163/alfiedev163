import pygame
import json
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Task Manager")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont(None, 28)
FONT_BIG = pygame.font.SysFont(None, 40)

TASKS_FILE = "tasks.json"

# -----------------------------
# DATA
# -----------------------------
tasks = []  # each task: {"text": str, "done": bool}
selected_index = None
scroll_offset = 0
INPUT_ACTIVE = False
input_text = ""

BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (90, 150, 200)
BG_COLOR = (240, 240, 240)
TASK_BG = (255, 255, 255)
TASK_DONE = (200, 255, 200)
TASK_SELECTED = (255, 230, 180)
TEXT_COLOR = (0, 0, 0)

# -----------------------------
# LOAD / SAVE
# -----------------------------
def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except Exception:
            tasks = []
    else:
        tasks = []

def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

load_tasks()

# -----------------------------
# UI HELPERS
# -----------------------------
def draw_text(text, x, y, font=FONT, color=TEXT_COLOR):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

def make_button(rect, label, mouse_pos):
    x, y, w, h = rect
    hovered = pygame.Rect(rect).collidepoint(mouse_pos)
    color = BUTTON_HOVER if hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=6)
    draw_text(label, x + 10, y + h//2 - 10)
    return hovered

# -----------------------------
# MAIN LOOP
# -----------------------------
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_tasks()
            running = False

        if event.type == pygame.KEYDOWN:
            if INPUT_ACTIVE:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        tasks.append({"text": input_text.strip(), "done": False})
                        save_tasks()
                    input_text = ""
                    INPUT_ACTIVE = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 60:
                        input_text += event.unicode
            else:
                if event.key == pygame.K_UP:
                    if selected_index is not None and selected_index > 0:
                        selected_index -= 1
                if event.key == pygame.K_DOWN:
                    if selected_index is not None and selected_index < len(tasks) - 1:
                        selected_index += 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # scroll up
                scroll_offset = max(scroll_offset - 30, 0)
            if event.button == 5:  # scroll down
                scroll_offset = max(scroll_offset + 30, 0)

    # -----------------------------
    # LOGIC: BUTTONS
    # -----------------------------
    screen.fill(BG_COLOR)

    # Layout
    list_rect = pygame.Rect(40, 80, 480, 480)
    input_rect = pygame.Rect(40, 20, 480, 40)
    add_btn_rect = (550, 80, 200, 50)
    done_btn_rect = (550, 150, 200, 50)
    del_btn_rect = (550, 220, 200, 50)
    save_btn_rect = (550, 290, 200, 50)
    load_btn_rect = (550, 360, 200, 50)

    # Input box
    pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius=6)
    pygame.draw.rect(screen, (180, 180, 180), input_rect, 2, border_radius=6)
    draw_text("New task:", 50, 26)
    draw_text(input_text if input_text else "(click here to type)", 150, 26,
              FONT, (0, 0, 0) if input_text else (150, 150, 150))

    # Click to activate input
    if mouse_pressed and input_rect.collidepoint(mouse_pos):
        INPUT_ACTIVE = True

    # Buttons
    add_hover = make_button(add_btn_rect, "Add Task", mouse_pos)
    done_hover = make_button(done_btn_rect, "Toggle Done", mouse_pos)
    del_hover = make_button(del_btn_rect, "Delete Task", mouse_pos)
    save_hover = make_button(save_btn_rect, "Save Tasks", mouse_pos)
    load_hover = make_button(load_btn_rect, "Load Tasks", mouse_pos)

    if mouse_pressed:
        if add_hover and not INPUT_ACTIVE:
            INPUT_ACTIVE = True
        if done_hover and selected_index is not None:
            tasks[selected_index]["done"] = not tasks[selected_index]["done"]
            save_tasks()
        if del_hover and selected_index is not None:
            tasks.pop(selected_index)
            if selected_index >= len(tasks):
                selected_index = len(tasks) - 1 if tasks else None
            save_tasks()
        if save_hover:
            save_tasks()
        if load_hover:
            load_tasks()
            selected_index = None
            scroll_offset = 0

    # -----------------------------
    # TASK LIST
    # -----------------------------
    pygame.draw.rect(screen, (220, 220, 220), list_rect, border_radius=6)
    pygame.draw.rect(screen, (180, 180, 180), list_rect, 2, border_radius=6)

    start_y = list_rect.y + 10 - scroll_offset
    item_height = 40

    for i, task in enumerate(tasks):
        item_rect = pygame.Rect(list_rect.x + 10, start_y + i * item_height,
                                list_rect.width - 20, item_height - 5)

        if item_rect.bottom < list_rect.y or item_rect.top > list_rect.bottom:
            continue  # skip off-screen

        bg = TASK_DONE if task["done"] else TASK_BG
        if selected_index == i:
            bg = TASK_SELECTED

        pygame.draw.rect(screen, bg, item_rect, border_radius=4)
        pygame.draw.rect(screen, (200, 200, 200), item_rect, 1, border_radius=4)

        text = task["text"]
        if task["done"]:
            text = "[DONE] " + text

        draw_text(text, item_rect.x + 8, item_rect.y + 8)

        # Click to select
        if mouse_pressed and item_rect.collidepoint(mouse_pos):
            selected_index = i

    # -----------------------------
    # HEADER
    # -----------------------------
    draw_text("Pygame Task Manager", 40, 560, FONT_BIG, (50, 50, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
