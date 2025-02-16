# sprites.py
import pygame
from settings import WIDTH, HEIGHT, SPEECH_BUBBLE_OFFSET  # Import SPEECH_BUBBLE_OFFSET

def load_sprite(path, size):
    """Load and scale a sprite."""
    sprite = pygame.image.load(path)
    return pygame.transform.scale(sprite, size)

# Load sprites
player_image = load_sprite("assets/player.png", (100, 100))
teacher_image = load_sprite("assets/teacher.png", (150, 150))
speech_bubble_image = load_sprite("assets/speech_bubble.png", (300, 150))
projectile_image = load_sprite("assets/projectile.png", (50, 50))

# Sprite positions
player_pos = [100, 450]
teacher_pos = [600, 400]  # Define teacher_pos here

# Calculate speech bubble position based on teacher's position and offset
speech_bubble_pos = [teacher_pos[0] + SPEECH_BUBBLE_OFFSET[0], teacher_pos[1] + SPEECH_BUBBLE_OFFSET[1]]

class SpeechBubble:
    def __init__(self, image):
        self.image = image

    def draw(self, screen, x, y):
        """Draw the speech bubble at the specified position."""
        screen.blit(self.image, (x, y))