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
    "(3 + 6)": 9
}


# Define Cube and Gate classes (omitted here for brevity - same as your original code)

# Placeholder functions for high scores and settings
def high_scores():
    # Display high scores here, can be implemented further
    pass


def settings():
    # Display settings menu here, can be implemented further
    pass


# Start Menu function
def menu_loop():
    clock = pygame.time.Clock()
    selected_option = 0  # Track the selected option
    options = ["Start Game", "High Scores", "Settings"]

    while True:
        screen.fill(WHITE)
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
                        high_scores()  # Display high scores
                    elif selected_option == 2:
                        settings()  # Go to settings

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
    screen.fill(WHITE)
    end_text = font.render("Game Over", True, BLACK)
    score_text = font.render(f"Final Score: {score}", True, BLACK)

    # Center the text on the screen
    end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    score_text_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))

    # Draw text to the screen
    screen.blit(end_text, end_text_rect)
    screen.blit(score_text, score_text_rect)

    pygame.display.flip()
    pygame.time.delay(3000)  # Display for 3 seconds before exiting
    pygame.quit()
    sys.exit()

# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    cube = Cube(100, screen_height - 100, 100, 5)
    red_gate = Gate(screen_width - screen_width // 2, screen_width // 2, 40, 2, RED)
    green_gate = Gate(0, screen_width // 2, 40, 2, GREEN)

    # Set the starting time and countdown duration
    countdown = 15  # Start at 15 seconds
    start_ticks = pygame.time.get_ticks()  # Get initial time

    while True:
        screen.fill(WHITE)
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calculate time remaining
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = countdown - seconds_passed

        # Display the countdown timer at the top center of the screen
        timer_text = font.render(f"Time: {time_left}", True, BLACK)
        timer_text_rect = timer_text.get_rect(center=(screen_width // 2, 20))
        screen.blit(timer_text, timer_text_rect)

        # Check if time has run out
        if time_left <= 0:
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
