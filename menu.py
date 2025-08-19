# setting up pygame and importing our own files
import pygame
import sys
import constants
import subprocess  # used to launch the other game files

# init pygame and fonts
pygame.init()
pygame.font.init()

# font setup – one for buttons, one for the title
FONT = pygame.font.Font(constants.FONT_NAME, 28)
TITLE_FONT = pygame.font.Font(constants.FONT_NAME, 40)

# create the screen
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Crossword Menu")

WHITE = (255, 255, 255)  # unused but handy if needed later

# settings for all 3 buttons
button_width = 250
button_height = 100
button_y = constants.SCREEN_HEIGHT // 2  # all buttons share this y

# reordered buttons: senses = easy, planets = medium, main = hard
buttons = [
    {"label": "5 Senses\n(Easy)", "x": 100, "target": "senses"},
    {"label": "Planets\n(Medium)", "x": 375, "target": "planets"},
    {"label": "Sports\n(Hard)", "x": 650, "target": "main"}
]

# draw the main menu title at the top
def draw_title():
    title = TITLE_FONT.render("Choose a Crossword!", True, constants.TEXT_COLOR)
    rect = title.get_rect(center=(constants.SCREEN_WIDTH // 2, 100))
    screen.blit(title, rect)

# draw each button – includes labels that can be on multiple lines
def draw_buttons():
    for btn in buttons:
        rect = pygame.Rect(btn["x"], button_y, button_width, button_height)
        pygame.draw.rect(screen, constants.CARD_BACK_COLOR, rect)
        pygame.draw.rect(screen, constants.TEXT_COLOR, rect, 3)

        # allow \n in label to go on multiple lines
        lines = btn["label"].split('\n')
        for i, line in enumerate(lines):
            text = FONT.render(line, True, constants.TEXT_COLOR)
            text_rect = text.get_rect(center=(btn["x"] + button_width // 2, button_y + 30 + i * 30))
            screen.blit(text, text_rect)

# check if the user clicked on any of the 3 buttons
def get_button_clicked(pos):
    for btn in buttons:
        rect = pygame.Rect(btn["x"], button_y, button_width, button_height)
        if rect.collidepoint(pos):
            return btn["target"]
    return None

# main loop – shows menu and waits for user input
def main():
    running = True
    while running:
        screen.fill(constants.BACKGROUND_COLOR)
        draw_title()
        draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if a button was clicked, run the relevant crossword file
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = get_button_clicked(event.pos)
                if clicked == "senses":
                    subprocess.run(["python3", "senses.py"])
                elif clicked == "planets":
                    subprocess.run(["python3", "planets.py"])
                elif clicked == "main":
                    subprocess.run(["python3", "main.py"])

        pygame.display.flip()
        pygame.time.Clock().tick(constants.FPS)  # cap the framerate

    pygame.quit()
    sys.exit()

# run the menu if this file is opened directly
if __name__ == "__main__":
    main()
