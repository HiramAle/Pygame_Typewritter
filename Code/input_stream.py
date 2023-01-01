import pygame
import constants


class Keyboard:
    def __init__(self):
        self.currentKeyStates = None
        self.previousKeyStates = None

    def process_input(self):
        self.previousKeyStates = self.currentKeyStates
        self.currentKeyStates = pygame.key.get_pressed()

    def is_key_down(self, key_code):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[key_code]

    def is_key_pressed(self, key_code):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[key_code] and not self.previousKeyStates[key_code]

    def is_key_released(self, key_code):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return not self.currentKeyStates[key_code] and self.previousKeyStates[key_code]


class InputStream:
    def __init__(self):
        self.keyboard = Keyboard()

    def process_input(self):
        self.keyboard.process_input()


class GameObject(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.rect.Rect

    def __init__(self, key: str, position: tuple, groups: pygame.sprite.Group | list[pygame.sprite.Group]):
        super().__init__(groups)
        self.key = key
        self.position = pygame.math.Vector2(position)

    def update(self, dt: float) -> None: ...

    def set_position(self, position: tuple):
        self.position = pygame.math.Vector2(position)


class Player(GameObject):
    def __init__(self, groups: pygame.sprite.Group | list[pygame.sprite.Group]):
        super().__init__("player", (constants.CANVAS_WIDTH / 2, constants.CANVAS_HEIGHT / 2), groups)
        self.direction = pygame.math.Vector2()
        self.movementSpeed = 300
        self.image = pygame.Surface((32, 32))
        self.image.fill(constants.BLUE)
        self.rect = self.image.get_rect(center=self.position)

    def input(self, input_stream: InputStream) -> None:
        # Vertical
        if input_stream.keyboard.is_key_pressed(pygame.K_w):
            self.direction.y = -1
        elif input_stream.keyboard.is_key_pressed(pygame.K_s):
            self.direction.y = 1
        else:
            self.direction.y = 0

        # Horizontal
        if input_stream.keyboard.is_key_pressed(pygame.K_a):
            self.direction.x = -1
        elif input_stream.keyboard.is_key_pressed(pygame.K_d):
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, dt: float) -> None:
        # Normalizing direction vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.position.x += self.direction.x * self.movementSpeed * dt
        self.rect.centerx = round(self.position.x)

        # Vertical movement
        self.position.y += self.direction.y * self.movementSpeed * dt
        self.rect.centery = round(self.position.y)

    def update(self, dt: float) -> None:
        self.move(dt)


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.gameCanvas = pygame.Surface((constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.sprites = pygame.sprite.Group()
        self.inputStream = InputStream()
        self.player = Player(self.sprites)

    def render(self):
        # Blit the game canvas on display
        self.display.blit(pygame.transform.scale(self.gameCanvas, (constants.WIDTH, constants.HEIGHT)), (0, 0))

    def draw(self):
        self.gameCanvas.fill(constants.BG_COLOR1)
        self.sprites.draw(self.gameCanvas)
        self.render()

    def update(self):
        self.sprites.update(self.clock.tick() / 1000)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                event: pygame.event.Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    self.player.input(self.inputStream)
            self.inputStream.process_input()
            self.update()
            self.draw()
            pygame.display.update()


if __name__ == '__main__':
    Game().run()
