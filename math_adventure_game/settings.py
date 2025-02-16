# settings.py

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font settings
FONT_NAME = "Comic Sans MS"
FONT_SIZE = 36  # Default font size for questions
FEEDBACK_FONT_SIZE = 24  # Smaller font size for feedback messages
FONT_BOLD = True

# Initial positions
PLAYER_POS = [100, 450]  # Player starts lower on the screen
TEACHER_POS = [600, 400]  # Teacher starts lower on the screen

# Speech bubble position (relative to teacher)
SPEECH_BUBBLE_OFFSET = [-250, -105]

# Damage text display duration (in frames)
DAMAGE_TEXT_DURATION = 60  # 60 frames at 30 FPS = 2 seconds

# Feedback display duration (in frames)
FEEDBACK_DURATION = 60  # 60 frames at 30 FPS = 2 seconds

# Frame rate
FPS = 30

# Button settings
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_PADDING = 10
BUTTON_COLOR = (200, 200, 200)  # Default button color
BUTTON_HIGHLIGHT_COLOR = (100, 200, 100)  # Highlighted button color
BUTTON_TEXT_COLOR = BLACK

# Bounce animation settings
BOUNCE_DURATION = 60  # Duration of the bounce animation in frames (2 seconds at 30 FPS)
BOUNCE_AMPLITUDE_X = 10  # Horizontal bounce amplitude (pixels)
BOUNCE_AMPLITUDE_Y = 20  # Vertical bounce amplitude (pixels)

# Teacher bounce animation settings
TEACHER_BOUNCE_DURATION = 30  # Duration of the teacher's bounce animation in frames (1 second at 30 FPS)
TEACHER_BOUNCE_AMPLITUDE_X = 15  # Horizontal bounce amplitude (pixels)
TEACHER_BOUNCE_AMPLITUDE_Y = 25  # Vertical bounce amplitude (pixels)

# Background image path
BACKGROUND_IMAGE_PATH = "assets/background.png"  # Replace with the actual file name/path