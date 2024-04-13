import pygame

WIDTH, HEIGHT = 800, 600
class Player:
    def __init__(self, x, y, image_path, screen):
        self.image = pygame.image.load(r"images\Individual-Sprites\adventurer-swrd-drw-01.png").convert_alpha()  # Load image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0.2
        self.jump_power = 15
        self.gravity = 0
        self.velocity_y = 0
        self.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    def move_left(self):
        self.pos.x -= self.speed

    def move_right(self):
        self.pos.x += self.speed

    def jump(self):
        if self.pos.y == HEIGHT - self.pos.height:
            self.velocity_y = -self.jump_power

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)