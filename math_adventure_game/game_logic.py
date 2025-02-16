import pygame
import random
from settings import FONT_NAME, FONT_SIZE, FEEDBACK_FONT_SIZE, FONT_BOLD, DAMAGE_TEXT_DURATION, FEEDBACK_DURATION
from settings import BUTTON_COLOR, BUTTON_HIGHLIGHT_COLOR, BUTTON_TEXT_COLOR

# Initialize Pygame mixer
pygame.mixer.init()

# Font object (initialized later)
font = None
feedback_font = None

# Load music and sound effects
background_music = None
damage_sound = None

def initialize_font():
    """Initialize the font objects after pygame.init() is called."""
    global font, feedback_font
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE, bold=FONT_BOLD)
    feedback_font = pygame.font.SysFont(FONT_NAME, FEEDBACK_FONT_SIZE, bold=FONT_BOLD)

def initialize_sounds():
    """Initialize the music and sound effects."""
    global background_music, damage_sound
    # Load background music
    background_music = pygame.mixer.Sound("assets/background_music.mp3")  # Replace with your music file
    background_music.set_volume(0.1)
    # Load damage sound effect
    damage_sound = pygame.mixer.Sound("assets/0215.MP3")  # Replace with your sound file
    damage_sound.set_volume(0.1)
def play_background_music():
    """Play the background music in a loop."""
    if background_music:
        background_music.play(-1)  # -1 means loop indefinitely

def stop_background_music():
    """Stop the background music."""
    if background_music:
        background_music.stop()

def play_damage_sound():
    """Play the damage sound effect."""
    if damage_sound:
        damage_sound.play()

class Button:
    def __init__(self, x, y, width, height, text, operation):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.operation = operation
        self.is_highlighted = False  # Default state is not highlighted

    def draw(self, screen):
        """Draw the button on the screen."""
        color = BUTTON_HIGHLIGHT_COLOR if self.is_highlighted else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, pos):
        """Check if the button was clicked."""
        return self.rect.collidepoint(pos)

# Generate math problem based on the selected operation
def get_problem(difficulty, operation):
    num1, num2 = 0, 0
    if difficulty == 1:  # Easy: Numbers between 1 and 10
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
    elif difficulty == 2:  # Medium: Numbers between 1 and 12
        num1 = random.randint(1, 12)
        num2 = random.randint(1, 12)
    elif difficulty == 3:  # Hard: Numbers between 1 and 50
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 10)

    if operation == '+':
        question = f"{num1} + {num2}"
        answer = num1 + num2
    elif operation == '-':
        question = f"{num1} - {num2}"
        answer = num1 - num2
    elif operation == '*':
        question = f"{num1} * {num2}"
        answer = num1 * num2
    elif operation == '/':
        question = f"{num1} / {num2}"
        answer = round(num1 / num2, 2)

    return question, answer

# Draw text on the screen
def draw_text(screen, text, color, x, y, font_size=FONT_SIZE):
    """Draw multi-line text on the screen."""
    lines = text.split("\n")  # Split text into lines
    line_height = font_size + 5  # Add some spacing between lines

    for i, line in enumerate(lines):
        if font_size == FONT_SIZE:
            text_surface = font.render(line, True, color)
        else:
            text_surface = feedback_font.render(line, True, color)
        screen.blit(text_surface, (x, y + i * line_height))