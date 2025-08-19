#this is the 5 senses game which is the easiest level
# setting up pygame n bits
#
import pygame
import os
import sys
import subprocess
import constants

# need to start pygame and the fonts
pygame.init()
pygame.font.init()

# fonts in all the sizes we'll use
FONT = pygame.font.Font(constants.FONT_NAME, 24)
SMALL_FONT = pygame.font.Font(constants.FONT_NAME, 16)
BIG_FONT = pygame.font.Font(constants.FONT_NAME, 36)
BUTTON_FONT = pygame.font.Font(constants.FONT_NAME, 20)

# set up screen size and title
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("5 Senses Crossword")

# the grid size and spacing
GRID_SIZE = 50
MARGIN_LEFT = 150
MARGIN_TOP = 100
ROWS, COLS = 9, 9  # 9x9 grid

# make an empty grid (filled later when typing letters)
grid = [["" for _ in range(COLS)] for _ in range(ROWS)]

# here are all the crossword answers and where they go
answers = [
    ("SMELL", 1, 4, "across"),
    ("TOUCH", 4, 0, "across"),
    ("HEARING", 0, 6, "down"),
    ("SIGHT", 1, 4, "down"),
    ("TASTE", 4, 0, "down"),
]

# clue numbers displayed on the grid
clue_numbers = {
    (0, 6): "1",    # HEARING
    (1, 4): "2",    # SMELL & SIGHT
    (4, 0): "3",    # TOUCH & TASTE
}

# load image assets for the clues
image_assets = {}
for word, _, _, _ in answers:
    name = word.lower()
    path = os.path.join("..", "assets", "images", f"{name}.png")
    if os.path.exists(path):
        image_assets[name] = pygame.transform.scale(pygame.image.load(path), (60, 60))

selected_cell = None  # current selected cell
valid_cells = set()   # cells that are part of any answer

# figure out which grid cells belong to valid words
for word, row, col, direction in answers:
    for i in range(len(word)):
        r = row + i if direction == "down" else row
        c = col + i if direction == "across" else col
        valid_cells.add((r, c))

# function to check if the user's answers match the real ones
def check_answers():
    for word, row, col, direction in answers:
        for i, char in enumerate(word):
            r = row + i if direction == "down" else row
            c = col + i if direction == "across" else col
            if grid[r][c] != char:
                return False
    return True

# draws a button with a label
def draw_button(text, x, y):
    btn_rect = pygame.Rect(x, y, 160, 40)
    pygame.draw.rect(screen, constants.CARD_FRONT_COLOR, btn_rect)
    pygame.draw.rect(screen, constants.TEXT_COLOR, btn_rect, 2)
    label = BUTTON_FONT.render(text, True, constants.TEXT_COLOR)
    label_rect = label.get_rect(center=btn_rect.center)
    screen.blit(label, label_rect)
    return btn_rect

# draws the crossword grid, letters, clues etc
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(MARGIN_LEFT + c * GRID_SIZE, MARGIN_TOP + r * GRID_SIZE, GRID_SIZE, GRID_SIZE)

            if (r, c) in valid_cells:
                pygame.draw.rect(screen, constants.CARD_BACK_COLOR, rect)
            else:
                pygame.draw.rect(screen, constants.CARD_FRONT_COLOR, rect)

            pygame.draw.rect(screen, constants.TEXT_COLOR, rect, 2)

            if (r, c) in clue_numbers:
                num = SMALL_FONT.render(clue_numbers[(r, c)], True, constants.TEXT_COLOR)
                screen.blit(num, (rect.x + 3, rect.y + 1))

            if grid[r][c]:
                letter = FONT.render(grid[r][c], True, constants.TEXT_COLOR)
                screen.blit(letter, (rect.x + 10, rect.y + 5))

            if selected_cell == (r, c):
                pygame.draw.rect(screen, constants.MATCH_HIGHLIGHT, rect, 3)

# draw all the clue images underneath
def draw_images():
    positions = {
        "hearing": (80, 630),
        "smell": (250, 630),
        "sight": (400, 630),
        "taste": (550, 630),
        "touch": (700, 630),
    }
    for word, _, _, _ in answers:
        name = word.lower()
        if name in image_assets and name in positions:
            screen.blit(image_assets[name], positions[name])

# draw the labels next to the images (like "1 Down")
def draw_clue_labels():
    labels = {
        "hearing": "1 Down",
        "smell": "2 Across",
        "sight": "2 Down",
        "touch": "3 Across",
        "taste": "3 Down"
    }
    positions = {
        "hearing": (80, 610),
        "smell": (250, 610),
        "sight": (400, 610),
        "taste": (550, 610),
        "touch": (700, 610)
    }
    for name, label in labels.items():
        screen.blit(SMALL_FONT.render(label, True, constants.TEXT_COLOR), positions[name])

# big title banner
def draw_title():
    title = "A Crossword of Senses"
    title_surface = BIG_FONT.render(title, True, constants.TEXT_COLOR)
    rect = title_surface.get_rect(center=(constants.SCREEN_WIDTH // 2, 40))
    screen.blit(title_surface, rect)

# figure out which cell was clicked
def get_cell_at_pos(pos):
    x, y = pos
    if x < MARGIN_LEFT or y < MARGIN_TOP:
        return None
    col = (x - MARGIN_LEFT) // GRID_SIZE
    row = (y - MARGIN_TOP) // GRID_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS and (row, col) in valid_cells:
        return (row, col)
    return None

# determine the word that the current cell belongs to
def get_word_at_cell(row, col):
    for word, start_row, start_col, direction in answers:
        for i in range(len(word)):
            r = start_row + i if direction == "down" else start_row
            c = start_col + i if direction == "across" else start_col
            if r == row and c == col:
                return word, start_row, start_col, direction
    return None

# main game loop
def main():
    global selected_cell
    feedback_message = ""
    message_color = (0, 0, 0)
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(constants.BACKGROUND_COLOR)
        draw_title()
        draw_grid()
        draw_images()
        draw_clue_labels()

        # draw buttons
        check_btn = draw_button("Check Answers", 100, 700)
        back_btn = draw_button("Back to Menu", 300, 700)
        next_btn = draw_button("Next Level", 500, 700)

        # draw feedback message if any
        if feedback_message:
            feedback_surface = FONT.render(feedback_message, True, message_color)
            screen.blit(feedback_surface, (100, 570))

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

                elif next_btn.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.run(["python3", "planets.py"])
                    sys.exit()

            elif event.type == pygame.KEYDOWN and selected_cell:
                r, c = selected_cell
                if event.key == pygame.K_BACKSPACE:
                    grid[r][c] = ""
                elif event.unicode.isalpha() and len(event.unicode) == 1:
                    grid[r][c] = event.unicode.upper()

                    # move to next cell in the same word
                    result = get_word_at_cell(r, c)
                    if result:
                        _, start_row, start_col, direction = result
                        if direction == "across":
                            next_c = c + 1
                            if (r, next_c) in valid_cells:
                                selected_cell = (r, next_c)
                        elif direction == "down":
                            next_r = r + 1
                            if (next_r, c) in valid_cells:
                                selected_cell = (next_r, c)

        pygame.display.flip()
        clock.tick(constants.FPS)

    pygame.quit()
    sys.exit()

# run the game
if __name__ == "__main__":
    main()
