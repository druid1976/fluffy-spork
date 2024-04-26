import pygame
import sys
import random

WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)  # Brown color

egg_obstacle_images = [
    "game/images/obstacles/egg/skeleton-animation_00.png",
    "game/images/obstacles/egg/skeleton-animation_01.png"
]

mob_ghost_images = [
    "game\images\obstacles\ghost\skeleton-animation_00.png",
    "game\images\obstacles\ghost\skeleton-animation_01.png"
]

class Obstacle:
    def __init__(self, x, y, image_path):
        self.original_image = pygame.image.load(image_path).convert_alpha()  # Load image
        self.original_rect = self.original_image.get_rect()
        self.original_rect.center = (x, y)
        
        # Scale down the image
        scale_factor = 0.09  # Adjust this scaling factor to make the obstacles smaller (0.5 means half size)
        self.image = pygame.transform.scale(self.original_image, (int(self.original_rect.width * scale_factor), int(self.original_rect.height * scale_factor)))
        self.rect = self.image.get_rect()
        self.rect.center = self.original_rect.center

class Player:
    def __init__(self, x, y, image_path, screen):
        self.image = pygame.image.load(image_path).convert_alpha()  # Load image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.jump_height = 120 # jump height in pixels
        self.jump_time = 40 #jump time in frames
        #gravity and jump_power are calculated based on laws of kinematics
        self.gravity = 2*self.jump_height/self.jump_time/self.jump_time  # Gravity acceleration
        self.jump_power = 2*self.jump_height/self.jump_time  # Jump power, physically speaking initial velocity of a jump
        self.velocity_y = 0
        self.is_on_ground = False  # Flag to track if the player is on the ground
        self.collision_depth = 5
        self.max_speed = self.collision_depth*2-1

    def move_left(self):
        if self.rect.left>=-self.collision_depth: #Preventing the player from getting out of the window on the left
            self.rect.x -= self.speed
            self.is_on_ground = False

    def move_right(self):
        if self.rect.right-self.collision_depth<WIDTH: #Stopping the player if he tries to leave the window on the right
            self.rect.x += self.speed
            self.is_on_ground=False

    def jump(self):
        if self.is_on_ground:  # Check if the player is on the ground
            self.velocity_y = -self.jump_power
            self.rect.y -= self.jump_power
            self.is_on_ground = False  # Update flag to indicate the player is jumping

    def apply_gravity(self):
        # Check if the player is on the ground
        if not self.is_on_ground:
            self.velocity_y += self.gravity  # Apply gravity to vertical velocity
            if self.velocity_y >= 0:
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        if self.rect.bottom-self.collision_depth*2 < platform.rect.top and self.rect.left<=platform.rect.right-self.collision_depth and self.rect.right>=platform.rect.left+self.collision_depth:
                            self.rect.bottom = platform.rect.top  # Move the player's rect to sit on top of the platform
                            self.velocity_y = 0  # Stop vertical movement
                            self.is_on_ground = True  # Update flag to indicate the player is on the ground
                            break  # Exit the loop once a platform is found
        self.velocity_y = min(self.max_speed, self.velocity_y)
        if self.rect.top<-self.collision_depth:
            self.rect.top=0
            self.velocity_y=0
        self.rect.y += self.velocity_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

# Initialize Pygame
clock = pygame.time.Clock()
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dancing mazes")

# Load background image
background_image = pygame.image.load("game\images\Old-Dungeon\OldDungeon.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Font for the "You died" message
font = pygame.font.Font(None, 36)

# Create platforms
platforms = [
    Platform(200, 500, 400, 20),
    Platform(100, 400, 200, 20),
    Platform(500, 300, 200, 20),
    # Additional platforms
    Platform(100, 200, 200, 20),
    Platform(500, 100, 300, 20),
    Platform(200, 50, 150, 20),
]

# Randomly select a platform for player spawn
selected_platform = random.choice(platforms)
player_spawn_x = random.randint(selected_platform.rect.left, selected_platform.rect.right)
player_spawn_y = selected_platform.rect.top-10

# Create player instance
player = Player(player_spawn_x, player_spawn_y, "game\images\\Individual-Sprites\\adventurer-swrd-drw-01.png", screen)  # Change to your image file

# Create obstacles
obstacles = []

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Check for space key press event
            player.jump()

    # Movement controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move_left()
    if keys[pygame.K_d]:
        player.move_right()

    # Apply gravity
    player.apply_gravity()

    # Check collision between player and obstacles
    for obstacle in obstacles:
        if player.rect.colliderect(obstacle.rect):
            # Player collided with an obstacle
            # Display "You died" message
            screen.fill(BLACK)
            text = font.render("You died", True, RED)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()

            # Wait for any key press to exit the game
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    elif event.type == pygame.KEYDOWN:
                        waiting = False
            # Exit the game loop
            running = False
            break  # Break out of the obstacle loop

    # Check if player fell out of screen
    if player.rect.top > HEIGHT:
        # Player fell out of screen
        # Display "You died" message
        screen.fill(BLACK)
        text = font.render("You died", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

        # Wait for any key press to exit the game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    waiting = False
        # Exit the game loop
        running = False

    # Drawigng part
    
    screen.blit(background_image, (0, 0))
    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform.rect)  # Draw brown platforms

    # Create obstacles on platforms max 5

    if len(obstacles) < 5:
        for platform in platforms:
            if random.randint(0, 100) < 5:  # Adjust the probability of obstacle appearance as needed
                obstacle_x = random.randint(platform.rect.left, platform.rect.right)
                obstacle_y = platform.rect.top - 30  # Adjust the vertical position of the obstacles
                obstacle_image_path = random.choice(egg_obstacle_images)
                obstacles.append(Obstacle(obstacle_x, obstacle_y, obstacle_image_path))

    # Draw obstacles
    for obstacle in obstacles:
        screen.blit(obstacle.image, obstacle.rect)

    # Draw player
    player.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
