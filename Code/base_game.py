import pygame
import constants
import basic_player
import basic_inventory
import scene
import inventory


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.caption = ""
        self.gameCanvas = pygame.Surface((constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.sceneManager = scene.SceneManager()
        # self.sceneManager.set_scene(scene.BasicScene(self.gameCanvas))
        self.sceneManager.set_scene(inventory.SceneInventory(self.gameCanvas, 1))

    def draw(self):
        self.sceneManager.draw()
        self.scale_canvas()

    def scale_canvas(self):
        # Blit the game canvas on display and scale it up
        self.display.blit(pygame.transform.scale(self.gameCanvas, (constants.WIDTH, constants.HEIGHT)), (0, 0))

    def update(self):
        self.sceneManager.update(self.clock.tick() / 1000)
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
                self.sceneManager.event_loop(event)

            self.update()
            self.draw()
            pygame.display.update()


if __name__ == '__main__':
    Game().run()
