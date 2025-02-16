import pygame
import random
import math  # Import math for sinusoidal calculations
from settings import *
from sprites import *
from game_logic import *

# Initialize pygame
pygame.init()

# Initialize font and sounds
initialize_font()
initialize_sounds()

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Adventure Game")

# Load background image
try:
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()  # Load the image
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale to fit the screen
except pygame.error as e:
    print(f"Error loading background image: {e}")
    background_image = None  # Fallback if the image fails to load

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game variables
score = 0
teacher_hp = 100
difficulty = 1
current_question = ""
correct_answer = None
input_box = ""
answered = False
projectile_active = False
projectile_pos = [player_pos[0], player_pos[1]]
damage_text = ""
damage_timer = 0 
feedback_text = ""
feedback_timer = 0 
waiting_for_feedback = False 
active_operation = "+"  # Default operation

# Bounce animation variables for player
bounce_timer = 0  # Timer for the player's bounce animation
is_bouncing = False  # Flag to indicate if the player is bouncing

# Bounce animation variables for teacher
teacher_bounce_timer = 0  # Timer for the teacher's bounce animation
is_teacher_bouncing = False  # Flag to indicate if the teacher is bouncing

# Create buttons
buttons = [
    Button(WIDTH - BUTTON_WIDTH - BUTTON_PADDING, BUTTON_PADDING, BUTTON_WIDTH, BUTTON_HEIGHT, "+", "+"),
    Button(WIDTH - BUTTON_WIDTH - BUTTON_PADDING, BUTTON_PADDING + BUTTON_HEIGHT + BUTTON_PADDING, BUTTON_WIDTH, BUTTON_HEIGHT, "-", "-"),
    Button(WIDTH - BUTTON_WIDTH - BUTTON_PADDING, BUTTON_PADDING + 2 * (BUTTON_HEIGHT + BUTTON_PADDING), BUTTON_WIDTH, BUTTON_HEIGHT, "*", "*"),
    Button(WIDTH - BUTTON_WIDTH - BUTTON_PADDING, BUTTON_PADDING + 3 * (BUTTON_HEIGHT + BUTTON_PADDING), BUTTON_WIDTH, BUTTON_HEIGHT, "/", "/")
]

# Highlight the "+" button by default
for button in buttons:
    if button.operation == "+":
        button.is_highlighted = True
    else:
        button.is_highlighted = False

# Set the active operation to match the highlighted button
active_operation = "+"

# Generate the first question
current_question, correct_answer = get_problem(difficulty, active_operation)

# Play background music
play_background_music()

# Main game loop
def play_game():
    global score, teacher_hp, difficulty, current_question, correct_answer, input_box, answered
    global projectile_active, projectile_pos, damage_text, damage_timer, feedback_text, feedback_timer, waiting_for_feedback, active_operation
    global bounce_timer, is_bouncing, teacher_bounce_timer, is_teacher_bouncing

    running = True

    while running:
        # Render background image
        if background_image:
            screen.blit(background_image, (0, 0))  # Draw the background image
        else:
            screen.fill(WHITE)  # Fallback to white background if no image is loaded

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle button clicks
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.check_click(pos):
                        active_operation = button.operation
                        # Unhighlight all buttons
                        for b in buttons:
                            b.is_highlighted = False
                        # Highlight the clicked button
                        button.is_highlighted = True
                        # Generate a new question with the selected operation
                        current_question, correct_answer = get_problem(difficulty, active_operation)
            elif event.type == pygame.KEYDOWN and not waiting_for_feedback:
                if event.key == pygame.K_RETURN:  # Submit answer
                    try:
                        user_answer = float(input_box)
                        if round(user_answer, 2) == correct_answer:
                            score += 10
                            teacher_hp -= 20
                            feedback_text = "Right! Good job!"
                            feedback_timer = FEEDBACK_DURATION
                            projectile_active = True  # Activate the projectile
                            projectile_pos = [player_pos[0], player_pos[1]]  # Reset projectile position
                            waiting_for_feedback = True  # Pause the game for feedback

                            # Start the player's bounce animation
                            bounce_timer = BOUNCE_DURATION
                            is_bouncing = True
                        else:
                            feedback_text = f"Wrong! The answer\nwas {correct_answer}."
                            feedback_timer = FEEDBACK_DURATION
                            teacher_hp += 10
                            waiting_for_feedback = True  # Pause the game for feedback
                        input_box = ""  # Clear input box
                    except ValueError:
                        feedback_text = "Invalid input. Try again."
                        feedback_timer = FEEDBACK_DURATION
                        waiting_for_feedback = True  # Pause the game for feedback
                elif event.key == pygame.K_BACKSPACE:  # Delete last character
                    input_box = input_box[:-1]
                else:  # Add character to input box
                    input_box += event.unicode

        # Update projectile movement
        if projectile_active:
            projectile_pos[0] += 10  # Move projectile to the right
            if projectile_pos[0] > teacher_pos[0]:  # Check if projectile hits the teacher
                projectile_active = False
                damage_timer = DAMAGE_TEXT_DURATION  # Show damage text for a short duration
                play_damage_sound()  # Play damage sound effect

                # Start the teacher's bounce animation
                teacher_bounce_timer = TEACHER_BOUNCE_DURATION
                is_teacher_bouncing = True

        # Update damage timer
        if damage_timer > 0:
            damage_timer -= 1

        # Update feedback timer
        if feedback_timer > 0:
            feedback_timer -= 1

        # Update player bounce animation
        if is_bouncing:
            if bounce_timer > 0:
                bounce_timer -= 1
                # Calculate sinusoidal offsets for bouncing
                bounce_offset_x = int(BOUNCE_AMPLITUDE_X * math.sin(2 * math.pi * (BOUNCE_DURATION - bounce_timer) / BOUNCE_DURATION))
                bounce_offset_y = -int(BOUNCE_AMPLITUDE_Y * abs(math.sin(2 * math.pi * (BOUNCE_DURATION - bounce_timer) / BOUNCE_DURATION)))
            else:
                # Stop bouncing when the timer reaches 0
                is_bouncing = False
                bounce_offset_x = 0
                bounce_offset_y = 0
        else:
            bounce_offset_x = 0
            bounce_offset_y = 0

        # Update teacher bounce animation
        if is_teacher_bouncing:
            if teacher_bounce_timer > 0:
                teacher_bounce_timer -= 1
                # Calculate sinusoidal offsets for bouncing
                teacher_bounce_offset_x = int(TEACHER_BOUNCE_AMPLITUDE_X * math.sin(2 * math.pi * (TEACHER_BOUNCE_DURATION - teacher_bounce_timer) / TEACHER_BOUNCE_DURATION))
                teacher_bounce_offset_y = -int(TEACHER_BOUNCE_AMPLITUDE_Y * abs(math.sin(2 * math.pi * (TEACHER_BOUNCE_DURATION - teacher_bounce_timer) / TEACHER_BOUNCE_DURATION)))
            else:
                # Stop bouncing when the timer reaches 0
                is_teacher_bouncing = False
                teacher_bounce_offset_x = 0
                teacher_bounce_offset_y = 0
        else:
            teacher_bounce_offset_x = 0
            teacher_bounce_offset_y = 0

        # If feedback is over, generate a new question
        if waiting_for_feedback and feedback_timer <= 0:
            if teacher_hp <= 0:
                feedback_text = "You defeated the teacher!"
                pygame.display.flip()
                pygame.time.wait(2000)
                stop_background_music()  # Stop background music
                running = False
            else:
                current_question, correct_answer = get_problem(difficulty, active_operation)
                waiting_for_feedback = False  # Resume the game

        # Display sprites
        screen.blit(player_image, (player_pos[0] + bounce_offset_x, player_pos[1] + bounce_offset_y))  # Apply player bounce offsets
        screen.blit(teacher_image, (teacher_pos[0] + teacher_bounce_offset_x, teacher_pos[1] + teacher_bounce_offset_y))  # Apply teacher bounce offsets

        # Display speech bubble
        screen.blit(speech_bubble_image, speech_bubble_pos)

        # Display either the current question or feedback text
        if waiting_for_feedback:
            draw_text(screen, feedback_text, BLACK, speech_bubble_pos[0] + 30, speech_bubble_pos[1] + 50, FEEDBACK_FONT_SIZE)
        else:
            draw_text(screen, current_question, BLACK, speech_bubble_pos[0] + 30, speech_bubble_pos[1] + 50, FONT_SIZE)

        # Display HP and score
        draw_text(screen, f"Score: {score}", BLACK, 10, 10, FONT_SIZE)
        draw_text(screen, f"Teacher HP: {teacher_hp}", RED, 10, 50, FONT_SIZE)

        # Display input box
        draw_text(screen, f"Your answer: {input_box}", BLACK, 10, 150, FONT_SIZE)

        # Display projectile
        if projectile_active:
            screen.blit(projectile_image, projectile_pos)

        # Display damage text
        if damage_timer > 0:
            draw_text(screen, damage_text, RED, teacher_pos[0], teacher_pos[1] - 50, FONT_SIZE)

        # Draw buttons
        for button in buttons:
            button.draw(screen)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    play_game()