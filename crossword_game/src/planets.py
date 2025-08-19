#this is the planets/solar systems game which is the medium level

# setting up pygame and importing our files
import pygame
import os
import sys
import subprocess
import constants

# initialise pygame and font modules
pygame.init()
pygame.font.init()

# different font sizes we'll use
FONT = pygame.font.Font(constants.FONT_NAME, 24)
SMALL_FONT = pygame.font.Font(constants.FONT_NAME, 16)
BIG_FONT = pygame.font.Font(constants.FONT_NAME, 36)
BUTTON_FONT = pygame.font.Font(constants.FONT_NAME, 20)

feedback_message = ""
message_color = (0, 0, 0)

# setup game window
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Our Place in Space")  # title up top

# setting up grid spacing and layout
GRID_SIZE = 50
MARGIN_LEFT = 100
MARGIN_TOP = 80
ROWS, COLS = 12, 12  # grid size

# blank crossword grid to start with
grid = [["" for _ in range(COLS)] for _ in range(ROWS)]

# all our planet-related answers with starting row/col and direction
answers = [
    ("MARS", 0, 2, "across"),
    ("NEPTUNE", 2, 0, "across"),
    ("JUPITER", 5, 0, "across"),
    ("SATURN", 9, 6, "across"),
    ("SUN", 0, 5, "down"),
    ("MERCURY", 1, 1, "down"),
    ("URANUS", 4, 6, "down"),
    ("EARTH", 6, 8, "down"),
    ("VENUS", 7, 11, "down"),
]

# clue number positions that match grid squares
clue_numbers = {
    (0, 2): "1",    # MARS
    (2, 0): "4",    # NEPTUNE
    (5, 0): "6",    # JUPITER
    (9, 6): "9",    # SATURN
    (0, 5): "2",    # SUN
    (1, 1): "3",    # MERCURY
    (4, 6): "5",    # URANUS
    (6, 8): "7",    # EARTH
    (7, 11): "8"    # VENUS
}

# load all the little planet pictures into image_assets
image_assets = {}
for word, _, _, _ in answers:
    name = word.lower()
    path = os.path.join("..", "assets", "images", f"{name}.png")
    if os.path.exists(path):
        image_assets[name] = pygame.transform.scale(pygame.image.load(path), (60, 60))

# keep track of what's selected
selected_cell = None

# build the list of cells that contain actual crossword letters
valid_cells = set()
for word, row, col, direction in answers:
    for i in range(len(word)):
        r = row + i if direction == "down" else row
        c = col + i if direction == "across" else col
        valid_cells.add((r, c))

# function to check if all letters typed in match the answers
def check_answers():
    for word, row, col, direction in answers:
        for i, char in enumerate(word):
            r = row + i if direction == "down" else row
            c = col + i if direction == "across" else col
            if grid[r][c] != char:
                return False
    return True

# helper function to auto-advance typing to the next cell in a word
def get_word_at_cell(row, col):
    for word, start_row, start_col, direction in answers:
        for i in range(len(word)):
            r = start_row + i if direction == "down" else start_row
            c = start_col + i if direction == "across" else start_col
            if r == row and c == col:
                return word, start_row, start_col, direction
    return None

# function to draw a button (used for check and back)
def draw_button(text, x, y):
    btn_rect = pygame.Rect(x, y, 160, 40)
    pygame.draw.rect(screen, constants.CARD_FRONT_COLOR, btn_rect)
    pygame.draw.rect(screen, constants.TEXT_COLOR, btn_rect, 2)
    label = BUTTON_FONT.render(text, True, constants.TEXT_COLOR)
    label_rect = label.get_rect(center=btn_rect.center)
    screen.blit(label, label_rect)
    return btn_rect

# draws the grid, letters, numbers and selection outlines
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

# draws the title banner at the top
def draw_title():
    title = "Our Place in Space"
    title_surface = BIG_FONT.render(title, True, constants.TEXT_COLOR)
    rect = title_surface.get_rect(center=(constants.SCREEN_WIDTH // 2, 30))
    screen.blit(title_surface, rect)

# draws clue text like "2 Down" next to each image
def draw_clue_labels():
    clue_texts = {
        "mars": "1 Across",
        "sun": "2 Down",
        "mercury": "3 Down",
        "neptune": "4 Across",
        "uranus": "5 Down",
        "jupiter": "6 Across",
        "earth": "7 Down",
        "venus": "8 Down",
        "saturn": "9 Across"
    }

    positions = {
        "sun": (800, 100),
        "uranus": (800, 160),
        "earth": (800, 220),
        "venus": (800, 280),
        "mars": (800, 340),
        "jupiter": (800, 400),
        "saturn": (800, 460),
        "mercury": (800, 520),
        "neptune": (800, 580)
    }

    for name, label in clue_texts.items():
        if name in positions:
            screen.blit(SMALL_FONT.render(label, True, constants.TEXT_COLOR), positions[name])

# draw the images for each planet/celestial body
def draw_images():
    positions = {
        "sun": (740, 90),
        "uranus": (740, 150),
        "earth": (740, 210),
        "venus": (740, 270),
        "mars": (740, 330),
        "jupiter": (740, 390),
        "saturn": (740, 450),
        "mercury": (740, 510),
        "neptune": (740, 570)
    }

    for word, _, _, _ in answers:
        name = word.lower()
        if name in image_assets and name in positions:
            screen.blit(image_assets[name], positions[name])

# convert mouse position into grid cell position
def get_cell_at_pos(pos):
    x, y = pos
    if x < MARGIN_LEFT or y < MARGIN_TOP:
        return None
    col = (x - MARGIN_LEFT) // GRID_SIZE
    row = (y - MARGIN_TOP) // GRID_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS and (row, col) in valid_cells:
        return (row, col)
    return None

# main loop that runs the planets crossword
def main():
    global selected_cell, feedback_message, message_color
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(constants.BACKGROUND_COLOR)
        draw_title()
        draw_grid()
        draw_images()
        draw_clue_labels()

        # draw the 3 buttons
        check_btn = draw_button("Check Answers", 100, 700)
        back_btn = draw_button("Back to Menu", 300, 700)
        next_btn = draw_button("Next Level", 500, 700)

        if feedback_message:
            msg_surface = FONT.render(feedback_message, True, message_color)
            screen.blit(msg_surface, (100, 760))

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
                    subprocess.run(["python3", "main.py"])
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

# run the game if this file is the one being executed
if __name__ == "__main__":
    main()