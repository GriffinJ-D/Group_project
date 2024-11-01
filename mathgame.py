import pygame
import sys

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

# Define font for the text
font = pygame.font.SysFont(None, 40)  # Choose the font size for displaying numbers

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
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size))

        # Render the value of the cube in the center
        number_text = font.render(str(self.value), True, WHITE)
        # Calculate the position to center the text on the cube
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
    def __init__(self, x, width, height, speed, value, color):
        self.x = x  # Position horizontally (either left or right)
        self.width = width
        self.height = height
        self.y = 0  # Start at the top
        self.speed = speed
        self.value = value  # Value displayed and used for calculation (+ or -)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Render the value (+5 or -3) in the center of the gate
        number_text = font.render(f'{self.value:+}', True, WHITE)  # + sign included for positive numbers
        text_rect = number_text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(number_text, text_rect)

    def fall(self):
        self.y += self.speed  # Move down the screen
        if self.y > screen_height:
            self.y = 0  # Reset to the top if it goes off the screen

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    cube = Cube(100, screen_height - 60, 50, 5)  # Create a cube at (100, 540) with size 50x50 and speed 5

    # Create two gates: one on the right and one on the left
    red_gate = Gate(screen_width - screen_width // 2, screen_width // 2, 40, 2, 5, RED)  # Red gate with +5
    green_gate = Gate(0, screen_width // 2, 40, 2, -3, GREEN)  # Green gate with -3

    while True:
        screen.fill(WHITE)  # Clear the screen
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move and draw the cube
        cube.move(keys)
        cube.draw(screen)

        # Make the gates fall and draw them
        red_gate.fall()
        red_gate.draw(screen)
        green_gate.fall()
        green_gate.draw(screen)

        # Check for collision with the red gate
        if cube.get_rect().colliderect(red_gate.get_rect()):
            cube.value += red_gate.value  # Add the value of the red gate (+5)
            red_gate.y = 0  # Reset the red gate's position

        # Check for collision with the green gate
        if cube.get_rect().colliderect(green_gate.get_rect()):
            cube.value += green_gate.value  # Subtract the value of the green gate (-3)
            green_gate.y = 0  # Reset the green gate's position

        # Update the display
        pygame.display.flip()

        # Cap the frame rate at 60 FPS
        clock.tick(60)

# Run the game
if __name__ == "__main__":
    game_loop()
