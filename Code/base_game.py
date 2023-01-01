import pygame
import constants
import basic_player
import inventory


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.caption = ""
        self.gameCanvas = pygame.Surface((constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.sprites = pygame.sprite.Group()
        self.player = basic_player.Player(self.sprites)
        self.inventory = inventory.Inventory(self, self.sprites)

    def draw(self):
        self.gameCanvas.fill(constants.BG_COLOR1)

        self.sprites.draw(self.gameCanvas)
        self.sprites.update(self.clock.tick() / 1000)
        self.render()

    def render(self):
        # Blit the game canvas on display
        self.display.blit(pygame.transform.scale(self.gameCanvas, (constants.WIDTH, constants.HEIGHT)), (0, 0))

    def update(self):
        self.update_caption()

    def update_caption(self):
        self.caption = f"Game_test      FPS: {int(self.clock.get_fps())}"
        pygame.display.set_caption(self.caption)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                event: pygame.event.Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.update()
            self.draw()
            pygame.display.update()


if __name__ == '__main__':
    Game().run()
