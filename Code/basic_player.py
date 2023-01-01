import pygame
import constants


class Player(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group | list[pygame.sprite.Group], position: tuple[int, int] = (0, 0)):
        super().__init__(groups)
        self.pixelPosition = pygame.math.Vector2(position)
        self.direction = pygame.math.Vector2(0, 0)
        self.tilePosition = pygame.math.Vector2(self.pixelPosition.x / constants.TILE_SIZE,
                                                self.pixelPosition.y / constants.TILE_SIZE)
        self.image = pygame.Surface((constants.TILE_SIZE, constants.TILE_SIZE))
        self.rect = self.image.get_rect(center=self.pixelPosition)
        self.speed = 300

    def input(self):
        keys = pygame.key.get_pressed()
        # Input for vertical movement
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # Input for horizontal movement
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, dt: float):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        self.pixelPosition += self.direction * self.speed * dt
        self.rect.center = self.pixelPosition

    def update(self, dt: float):
        self.input()
        self.move(dt)
