import pygame
import ctypes
import constants
import time

# Avoid DPI virtualization
ctypes.windll.user32.SetProcessDPIAware()


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


class Text(GameObject):
    def __init__(self, text: str, position: tuple, groups: pygame.sprite.Group | list[pygame.sprite.Group]):
        super().__init__("text", position, groups)
        self.text = text
        self.font = pygame.font.Font("../Assets/monogram.ttf", 40)
        self.image = self.font.render(self.text, False, constants.WHITE)
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self, dt: float) -> None:
        self.image = self.font.render(self.text, False, constants.WHITE)


class DialogueBox(GameObject):
    def __init__(self, text: str, position: tuple, groups: pygame.sprite.Group | list[pygame.sprite.Group]):
        super().__init__("dialogue", position, groups)
        self.text = text
        self.textBox = pygame.Surface((400, 200))
        self.textBox.fill(constants.BG_COLOR2)
        self.speed = 30
        self.counter = 0
        self.done = False
        self.font = pygame.font.Font("../Assets/monogram.ttf", 40)
        self.textImage = self.font.render(self.text, False, constants.WHITE)
        self.image = pygame.Surface(self.textBox.get_size())
        self.rect = self.image.get_rect(topleft=self.position)
        # Create dictionary with lines and words per line
        self.lines = [line.split(' ') for line in self.text.splitlines()]
        self.spaceSize = self.font.size(" ")
        self.maxWidth = self.textBox.get_width()
        self.maxHeight = self.textBox.get_height()

        self.formattedText = self.formatter(self.lines)
        self.newText = self.convert_to_text(self.formatter(self.lines))
        self.x = 0
        self.y = 0
        self.pastIndex = -1
        self.linesBoxWidth = int(self.textBox.get_height() / self.spaceSize[1])
        self.activeLines = self.formattedText[:self.linesBoxWidth]
        self.remainingLines = self.formattedText[self.linesBoxWidth:]

    def next_lines(self):
        if len(self.remainingLines) > 0:
            self.textBox = pygame.Surface((400, 200))
            self.textBox.fill(constants.BG_COLOR2)

            self.counter = 0
            self.pastIndex = -1
            self.done = False

            self.x = 0
            self.y = 0

            self.activeLines = self.remainingLines[:self.linesBoxWidth]
            self.remainingLines = self.remainingLines[self.linesBoxWidth:]
            print(f"Remaining: {len(self.remainingLines)}")



    def update(self, dt: float) -> None:
        self.typewriter(self.activeLines, dt)
        self.image.blit(self.textBox, (0, 0))

    def formatter(self, lines: list):
        text = []
        text_line = []
        x, y = 0, 0
        for line in lines:
            for word in line:
                word_width, word_height = self.font.size(word)
                if x + word_width >= self.maxWidth:
                    x = 0
                    text.append(text_line)
                    text_line = []
                x += word_width + self.spaceSize[0]
                text_line.append(word)
            x = 0
            text.append(text_line)
            text_line = []
        return text

    def typewriter(self, lines: list, dt: float):
        # Control
        if not self.done:
            self.counter += self.speed * dt
            if self.counter >= len(self.convert_to_text(lines).replace("|", " ")):
                self.done = True
        # Render

        if int(self.counter) != int(self.pastIndex) and not self.done:
            char_surface = self.font.render(self.convert_to_text(lines).replace("|", " ")[int(self.counter)], False,
                                            constants.WHITE)
            print(f"Char: {self.convert_to_text(lines)[int(self.counter)]}")
            if self.convert_to_text(lines)[int(self.counter)] == "|":
                self.y += char_surface.get_height()
                self.x = 0
                # self.newText = self.newText[:int(self.counter)] + self.newText[int(self.counter):]
            else:
                self.textBox.blit(char_surface, (self.x, self.y))
                self.x += char_surface.get_width()
            self.pastIndex = self.counter

    def convert_to_text(self, lines: list):
        return "|".join([" ".join(line) for line in lines])

    def blit(self):
        x = 0
        y = 0
        for line in self.textSurfaces:
            line_surface = self.font.render(" ".join(line), False, constants.WHITE)
            self.textBox.blit(line_surface, (x, y))
            y += line_surface.get_height()

        # lines = []
        # word_width, word_height = 0, 0
        # x, y = self.position
        # for line in self.lines:
        #     words = []
        #     for word in line:
        #         word_width, word_height = self.font.size(word)
        #         if x + word_width >= self.position[0] + self.maxWidth:
        #             x = self.position[0]  # Reset the x.z
        #             y += word_height  # Start on new row.
        #
        #         x += word_width + self.spaceLength[0]
        #         line_surface.blit(word_surface, (x, 0))
        #     self.textSurfaces.append(line_surface)
        #     x = self.position[0]  # Reset the x.
        #     y += word_height  # Start on new row.
        # print(self.textSurfaces)

    def blit_lines(self):
        x, y = 0, 0
        for text in self.textSurfaces:
            text: pygame.Surface
            self.textBox.blit(text, (0, y))
            y += text.get_height()

        # self.image.blit(self.textBox, (0, 0))
        # text = self.newText[0:round(self.counter)]
        # word_height = self.font.size(text)[0]
        # if text:
        #     if text[-1] == "|":
        #         x = 0
        #         y += word_height
        # self.textImage = self.font.render(text, False, constants.WHITE)
        # self.image.blit(self.textImage, (x, y))


class Player(GameObject):
    def __init__(self, groups: pygame.sprite.Group | list[pygame.sprite.Group]):
        super().__init__("player", (constants.CANVAS_WIDTH / 2, constants.CANVAS_HEIGHT / 2), groups)
        self.direction = pygame.math.Vector2()
        self.movementSpeed = 300
        self.image = pygame.Surface((32, 32))
        self.image.fill(constants.BLUE)
        self.rect = self.image.get_rect(center=self.position)

    def input(self) -> None:
        keys = pygame.key.get_pressed()
        # Vertical
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # Horizontal
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
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
        self.input()
        self.move(dt)


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.gameCanvas = pygame.Surface((constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.sprites = pygame.sprite.Group()
        self.player = Player(self.sprites)
        self.box = DialogueBox(constants.TEXT_TEST, (100, 100), self.sprites)
        self.coords = Text("0,0", (0, 0), self.sprites)

    def render(self):
        # Blit the game canvas on display
        self.display.blit(pygame.transform.scale(self.gameCanvas, (constants.WIDTH, constants.HEIGHT)), (0, 0))

    def draw(self):
        self.gameCanvas.fill(constants.BG_COLOR1)
        self.sprites.draw(self.gameCanvas)
        self.render()

    def update(self):
        self.coords.text = str(pygame.mouse.get_pos())
        self.sprites.update(self.clock.tick() / 1000)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                event: pygame.event.Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                        if self.box.done:
                            self.box.next_lines()

            self.update()
            self.draw()
            pygame.display.update()


if __name__ == '__main__':
    Game().run()
