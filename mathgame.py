import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Define screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Math Game')


# Initialize Pygame Mixer
pygame.mixer.init()

# Load the music file
pygame.mixer.music.load("Kirby_-_Gourmet_Race_Remix_[_YTBMP3.org_].mp3")  # Replace with your file's path



# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Define font for the text
font = pygame.font.SysFont(None, 40)  # Choose the font size for displaying numbers

# Dictionary of equations and their answers
equations = {
    "(7 - 3)": 4,
    "(2 * 3)": 6,
    "9 / 3": 3,
    "(5 + 4)": 9,
    "(8 - 2)": 6,
    "3 - 5": -2,
    "(4 * 2)": 8,
    "6 / 2": 3,
    "(10 - 7)": 3,
    "(3 + 6)": 9,
    "(1 - 4)": -3,
    "(6 - 9)": -3,
    "(3 * 0)": -0,
    "(3 - 8)": -5
}


# Global variable for difficulty setting
difficulty = "Medium"  # Default difficulty

# Settings menu options
settings_options = ["Difficulty", "Audio", "Visual", "Back"]

# Difficulty options and gate speed dictionary
difficulty_options = ["Easy", "Medium", "Hard"]
gate_speeds = {"Easy": 1, "Medium": 2, "Hard": 4}
# Difficulty setting submenu
def difficulty_menu():
    global difficulty  # Declare 'difficulty' as global at the start of the function
    selected_difficulty = difficulty_options.index(difficulty)

    while True:
        screen.fill(BLACK if is_dark_mode else WHITE)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_difficulty = (selected_difficulty - 1) % len(difficulty_options)
                elif event.key == pygame.K_DOWN:
                    selected_difficulty = (selected_difficulty + 1) % len(difficulty_options)
                elif event.key == pygame.K_RETURN:
                    difficulty = difficulty_options[selected_difficulty]
                    return  # Go back to settings menu on selection
                elif event.key == pygame.K_ESCAPE:
                    return  # Return to settings menu

        # Display difficulty options
        for i, option in enumerate(difficulty_options):
            color = BLUE if i == selected_difficulty else BLACK
            option_text = font.render(option, True, color)
            screen.blit(option_text, (screen_width // 2 - option_text.get_width() // 2, screen_height // 2 + i * 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Track the current theme
is_dark_mode = False  # Global variable to track if Dark Mode is enabled

# Function to display individual setting options with Dark Mode toggle
def setting_submenu(option_name):
    global is_dark_mode, screen, screen_width, screen_height  # Declare globals to modify screen properties
    selected_option = 0
    options = ["Dark Mode", "Screen Size", "Back"]  # Add "Screen Size" to the options

    while True:
        # Set background and text colors based on Dark Mode
        background_color = BLACK if is_dark_mode else WHITE
        text_color = WHITE if is_dark_mode else BLACK

        screen.fill(background_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Toggle Dark Mode
                        is_dark_mode = not is_dark_mode
                    elif selected_option == 1:  # Adjust Screen Size
                        # Increase screen size
                        screen_width += 200
                        screen_height += 150
                        screen = pygame.display.set_mode((screen_width, screen_height))
                    elif selected_option == 2:  # Back
                        return  # Exit to the settings menu

        # Display options
        for i, option in enumerate(options):
            color = BLUE if i == selected_option else text_color
            option_text = font.render(option, True, color)
            screen.blit(option_text, (screen_width // 2 - option_text.get_width() // 2, screen_height // 2 + i * 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)



# Preset high scores (3-letter initials and a score)
high_scores_list = [
    ("LBJ", 23),
    ("SGA", 22),
    ("MLK", 20),
    ("JFK", 16),
    ("PJD", 12)
]
def high_scores():
    selected_option = 0  # Only one option: "Back"
    while True:
        screen.fill(BLACK if is_dark_mode else WHITE)


        # Display high scores
        title_text = font.render("High Scores", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))

        # Display each high score
        for i, (initials, score) in enumerate(high_scores_list):
            score_text = font.render(f"{initials}: {score}", True, BLACK)
            screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 100 + i * 40))

        # Display "Back" option
        color = BLUE if selected_option == 0 else BLACK
        back_text = font.render("Back", True, color)
        screen.blit(back_text, (screen_width // 2 - back_text.get_width() // 2, screen_height - 100))

        pygame.display.flip()

        # Event handling for back option
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to select "Back"
                    menu_loop()
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 1  # Toggle back option (single option)

        pygame.time.Clock().tick(60)


# Function to prompt for initials and insert into high scores
def enter_initials_and_save_score(new_score):
    initials = ""
    while True:
        screen.fill(BLACK if is_dark_mode else WHITE)


        # Display prompt for entering initials
        prompt_text = font.render("Enter Your Initials:", True, BLACK)
        screen.blit(prompt_text, (screen_width // 2 - prompt_text.get_width() // 2, screen_height // 3))

        # Display the current initials entered
        initials_text = font.render(initials, True, BLACK)
        screen.blit(initials_text, (screen_width // 2 - initials_text.get_width() // 2, screen_height // 2))

        pygame.display.flip()

        # Handle events for entering initials
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(initials) == 3:
                    # Insert the new high score in the sorted list
                    high_scores_list.append((initials, new_score))
                    high_scores_list.sort(key=lambda x: x[1], reverse=True)
                    del high_scores_list[5:]  # Keep only top 5 scores
                    return
                elif event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]  # Remove the last character
                elif len(initials) < 3 and event.unicode.isalpha():
                    initials += event.unicode.upper()  # Add new letter and convert to uppercase

# End game screen and check if score qualifies for high scores



# Settings menu function
def settings_menu():
    selected_setting = 0  # Track selected setting
    while True:
        screen.fill(BLACK if is_dark_mode else WHITE)


        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_setting = (selected_setting - 1) % len(settings_options)
                elif event.key == pygame.K_DOWN:
                    selected_setting = (selected_setting + 1) % len(settings_options)
                elif event.key == pygame.K_RETURN:
                    if selected_setting == 0:  # Difficulty
                        difficulty_menu()
                    elif selected_setting == 1:  # Audio
                        setting_submenu("Audio")
                    elif selected_setting == 2:  # Visual
                        setting_submenu("Visual")
                    elif selected_setting == 3:  # Back
                        return  # Return to main menu

        # Display settings options
        for i, option in enumerate(settings_options):
            color = BLUE if i == selected_setting else BLACK
            option_text = font.render(option, True, color)
            screen.blit(option_text, (screen_width // 2 - option_text.get_width() // 2, screen_height // 2 + i * 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)


# Start Menu function
def menu_loop():
    clock = pygame.time.Clock()
    selected_option = 0  # Track the selected option
    options = ["Start Game", "High Scores", "Settings"]

    while True:
        screen.fill(BLACK if is_dark_mode else WHITE)

        keys = pygame.key.get_pressed()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)  # Move selection up
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)  # Move selection down
                elif event.key == pygame.K_RETURN:  # Enter key selects an option
                    if selected_option == 0:
                        game_loop()  # Start the game
                    elif selected_option == 1:
                        high_scores()  # Display high scores and return to this menu after "Back" is selected
                    elif selected_option == 2:
                        settings_menu()  # Go to settings

        # Display menu options
        for i, option in enumerate(options):
            color = BLUE if i == selected_option else BLACK
            option_text = font.render(option, True, color)
            screen.blit(option_text, (screen_width // 2 - option_text.get_width() // 2, screen_height // 2 + i * 50))

        pygame.display.flip()
        clock.tick(60)
# Define Cube class
class Cube:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.value = 1  # Initial value on the cube

        # Load the image for the cube and scale it to the size of the cube
        self.image = pygame.image.load('Character.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def draw(self, screen):
        # Draw the image in place of the cube
        screen.blit(self.image, (self.x, self.y))

        # Render the value of the cube in the center (you can adjust positioning to fit your image)
        number_text = font.render(str(self.value), True, WHITE)
        text_rect = number_text.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
        screen.blit(number_text, text_rect)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Prevent the cube from moving off screen
        if self.x < 0:
            self.x = 0
        if self.x + self.size > screen_width:
            self.x = screen_width - self.size

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


# Define Gate class for both gates
class Gate:
    def __init__(self, x, width, height, speed, color):
        self.x = x
        self.width = width
        self.height = height
        self.y = 0
        self.speed = speed
        self.color = color
        self.reset_equation()

    def reset_equation(self):
        self.equation, self.answer = random.choice(list(equations.items()))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        equation_text = font.render(self.equation, True, WHITE)
        text_rect = equation_text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(equation_text, text_rect)

    def fall(self):
        self.y += self.speed
        if self.y > screen_height:
            self.y = 0
            self.reset_equation()  # Reset equation when the gate falls off screen

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# End game screen to show the final score

def end_game_screen(score):
    # Check if score qualifies for high scores only once
    new_high_score = False
    if score > min(high_scores_list, key=lambda x: x[1])[1]:  # Score qualifies if higher than the lowest high score
        enter_initials_and_save_score(score)
        new_high_score = True  # Mark that a new high score was entered

    # Display "Game Over" and final score
    screen.fill(BLACK if is_dark_mode else WHITE)
    end_text = font.render("Game Over", True, WHITE if is_dark_mode else BLACK)
    score_text = font.render(f"Final Score: {score}", True, WHITE if is_dark_mode else BLACK)

    # Center the text on the screen
    end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    score_text_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))

    # Draw text to the screen
    screen.blit(end_text, end_text_rect)
    screen.blit(score_text, score_text_rect)

    pygame.display.flip()
    pygame.time.delay(3000)  # Display "Game Over" message for 3 seconds

    # Automatically show the high scores list after "Game Over" message
    high_scores()



# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    cube = Cube(100, screen_height - 100, 100, 5)

    red_gate = Gate(screen_width - screen_width // 2, screen_width // 2, 40, gate_speeds[difficulty], RED)
    green_gate = Gate(0, screen_width // 2, 40, gate_speeds[difficulty], GREEN)

    # Set the starting time and countdown duration
    countdown = 15  # Start at 15 seconds
    start_ticks = pygame.time.get_ticks()  # Get initial time

    # Play background music
    pygame.mixer.music.play(-1)  # Loop music indefinitely

    while True:
        screen.fill(BLACK if is_dark_mode else WHITE)
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop music on quit
                pygame.quit()
                sys.exit()

        # Calculate time remaining
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = countdown - seconds_passed

        # Display the countdown timer at the top center of the screen
        timer_text = font.render(f"Time: {time_left}", True, BLACK if not is_dark_mode else WHITE)
        timer_text_rect = timer_text.get_rect(center=(screen_width // 2, 20))
        screen.blit(timer_text, timer_text_rect)

        # Check if time has run out
        if time_left <= 0:
            pygame.mixer.music.stop()  # Stop music when the game ends
            end_game_screen(cube.value)  # Display end game screen with final score

        # Move and draw the cube
        cube.move(keys)
        cube.draw(screen)

        # Make the gates fall and draw them
        red_gate.fall()
        red_gate.draw(screen)
        green_gate.fall()
        green_gate.draw(screen)

        # Check for collisions and update cube value
        if cube.get_rect().colliderect(red_gate.get_rect()):
            cube.value += red_gate.answer
            red_gate.y = 0
            red_gate.reset_equation()

        if cube.get_rect().colliderect(green_gate.get_rect()):
            cube.value += green_gate.answer
            green_gate.y = 0
            green_gate.reset_equation()

        pygame.display.flip()
        clock.tick(60)


# Run the game
if __name__ == "__main__":
    menu_loop()
