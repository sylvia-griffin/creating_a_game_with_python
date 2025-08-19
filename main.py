# this is a simple crossword game for primary kids
# i ditched tkinter & pycrossword cos they were a bit clunky
# pygame gives us better visuals and more control tbh
# this is the hardest level

import pygame
import os
import sys
import subprocess

# importing our colour/font constants from another file
import constants

# init pygame and fonts
pygame.init()
pygame.font.init()

# fonts in diff sizes – used all over the place
FONT = pygame.font.Font(constants.FONT_NAME, 24)
SMALL_FONT = pygame.font.Font(constants.FONT_NAME, 16)
BIG_FONT = pygame.font.Font(constants.FONT_NAME, 36)
BUTTON_FONT = pygame.font.Font(constants.FONT_NAME, 20)

# screen setup – size is controlled in constants
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Sports Crossword")

# draws a little button with a label on it
def draw_button(text, x, y):
    btn_rect = pygame.Rect(x, y, 160, 40)
    pygame.draw.rect(screen, constants.CARD_FRONT_COLOR, btn_rect)
    pygame.draw.rect(screen, constants.TEXT_COLOR, btn_rect, 2)

    label = BUTTON_FONT.render(text, True, constants.TEXT_COLOR)
    label_rect = label.get_rect(center=btn_rect.center)
    screen.blit(label, label_rect)
    return btn_rect

# grid settings and layout stuff
GRID_SIZE = 40
MARGIN_LEFT = 100
MARGIN_TOP = 150
ROWS, COLS = 14, 16  # increased grid size for spacing

# blank grid to start with
grid = [["" for _ in range(COLS)] for _ in range(ROWS)]

# crossword answers with coordinates and directions
answers = [
    ("FOOTBALL", 0, 8, "across"),
    ("TENNIS", 5, 5, "across"),
    ("VOLLEYBALL", 8, 3, "across"),
    ("SOCCER", 11, 0, "across"),
    ("BASKETBALL", 0, 12, "down"),
    ("BASEBALL", 3, 10, "down"),
    ("HOCKEY", 7, 4, "down"),
    ("GOLF", 10, 1, "down"),
]

# clue numbers for grid corners
clue_numbers = {
    (0, 8): "1",
    (5, 5): "2",
    (8, 3): "3",
    (11, 0): "4",
    (0, 12): "5",
    (3, 10): "6",
    (7, 4): "7",
    (10, 1): "8",
}

# load images for each word if available
image_assets = {}
for word, _, _, _ in answers:
    name = word.lower()
    path = os.path.join("..", "assets", "images", f"{name}.png")
    if os.path.exists(path):
        image_assets[name] = pygame.transform.scale(pygame.image.load(path), (60, 60))

selected_cell = None
valid_cells = set()

# mark valid grid cells
for word, row, col, direction in answers:
    for i in range(len(word)):
        r = row + i if direction == "down" else row
        c = col + i if direction == "across" else col
        valid_cells.add((r, c))

# check if player's answers match the actual ones
def check_answers():
    for word, row, col, direction in answers:
        for i, char in enumerate(word):
            r = row + i if direction == "down" else row
            c = col + i if direction == "across" else col
            if grid[r][c] != char:
                return False
    return True

# draw the crossword grid
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(MARGIN_LEFT + c * GRID_SIZE, MARGIN_TOP + r * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, constants.CARD_BACK_COLOR if (r, c) in valid_cells else constants.CARD_FRONT_COLOR, rect)
            pygame.draw.rect(screen, constants.TEXT_COLOR, rect, 2)

            if (r, c) in clue_numbers:
                screen.blit(SMALL_FONT.render(clue_numbers[(r, c)], True, constants.TEXT_COLOR), (rect.x + 3, rect.y + 1))

            if grid[r][c]:
                screen.blit(FONT.render(grid[r][c], True, constants.TEXT_COLOR), (rect.x + 10, rect.y + 5))

            if selected_cell == (r, c):
                pygame.draw.rect(screen, constants.MATCH_HIGHLIGHT, rect, 3)

# display word images to the right of the grid
def draw_images():
    positions = {
        "baseball": (10, 80),
        "golf": (250, 80),
        "football": (500, 80),
        "basketball": (700, 80),
        "tennis": (800, 170),
        "volleyball": (800, 280),
        "hockey": (800, 400),
        "soccer": (800, 520),
    }
    for word, _, _, _ in answers:
        name = word.lower()
        if name in image_assets and name in positions:
            screen.blit(image_assets[name], positions[name])

# clue labels beside images
def draw_clue_labels():
    clue_texts = {
        "baseball": "6 Down",
        "golf": "8 Down",
        "football": "1 Across",
        "basketball": "5 Down",
        "tennis": "2 Across",
        "volleyball": "3 Across",
        "hockey": "7 Down",
        "soccer": "4 Across"
    }
    label_positions = {
        "baseball": (80, 80),
        "golf": (320, 80),
        "football": (570, 80),
        "basketball": (770, 80),
        "tennis": (870, 170),
        "volleyball": (870, 280),
        "hockey": (870, 400),
        "soccer": (870, 520)
    }
    for name, label in clue_texts.items():
        if name in label_positions:
            screen.blit(SMALL_FONT.render(label, True, constants.TEXT_COLOR), label_positions[name])

# show game title at top
def draw_title():
    title_surface = BIG_FONT.render("Field Day: The Crossword Edition!", True, constants.TEXT_COLOR)
    title_rect = title_surface.get_rect(center=(constants.SCREEN_WIDTH // 2, 20))
    screen.blit(title_surface, title_rect)

# find which grid cell was clicked
def get_cell_at_pos(pos):
    x, y = pos
    if x < MARGIN_LEFT or y < MARGIN_TOP:
        return None
    col = (x - MARGIN_LEFT) // GRID_SIZE
    row = (y - MARGIN_TOP) // GRID_SIZE
    return (row, col) if (row, col) in valid_cells else None

# auto moves to next cell in current word
def get_word_at_cell(row, col):
    for word, start_row, start_col, direction in answers:
        for i in range(len(word)):
            r = start_row + i if direction == "down" else start_row
            c = start_col + i if direction == "across" else start_col
            if r == row and c == col:
                return word, start_row, start_col, direction
    return None

# 🔁 main loop
def main():
    global selected_cell
    clock = pygame.time.Clock()
    feedback_message = ""
    message_color = (0, 0, 0)
    running = True

    while running:
        screen.fill(constants.BACKGROUND_COLOR)
        draw_title()
        draw_grid()
        draw_images()
        draw_clue_labels()

        # draw bottom buttons (only check and back)
        check_btn = draw_button("Check Answers", 100, 750)
        back_btn = draw_button("Back to Menu", 300, 750)

        # draw feedback text
        if feedback_message:
            feedback_surface = FONT.render(feedback_message, True, message_color)
            screen.blit(feedback_surface, (100, 720))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_cell = get_cell_at_pos(event.pos)

                if check_btn.collidepoint(event.pos):
                    if check_answers():
                        feedback_message = "All correct!"
                        message_color = (0, 128, 0)
                    else:
                        feedback_message = "Some letters are incorrect."
                        message_color = (200, 0, 0)

                elif back_btn.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.run(["python3", "menu.py"])
                    sys.exit()

            elif event.type == pygame.KEYDOWN and selected_cell:
                r, c = selected_cell
                if event.key == pygame.K_BACKSPACE:
                    grid[r][c] = ""
                elif event.unicode.isalpha() and len(event.unicode) == 1:
                    grid[r][c] = event.unicode.upper()
                    result = get_word_at_cell(r, c)
                    if result:
                        _, start_row, start_col, direction = result
                        if direction == "across" and (r, c + 1) in valid_cells:
                            selected_cell = (r, c + 1)
                        elif direction == "down" and (r + 1, c) in valid_cells:
                            selected_cell = (r + 1, c)

        pygame.display.flip()
        clock.tick(constants.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
