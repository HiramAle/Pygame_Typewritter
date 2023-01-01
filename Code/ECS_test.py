from __future__ import annotations
import pygame
import constants

# Settings
TILE_SIZE = 64
# Colors
DEFAULT_COLOR = constants.BLUE


class Entity:
    def __init__(self, key: int = None, name: str = None):
        self.key = key
        self.name = name
        self.components: dict[str, Component] = {}

    def add_component(self, component: Component) -> None:
        if component.key is not None:
            self.components[component.key] = component

    def get_component(self, component_key: str) -> Component | None:
        if component_key not in self.components.keys():
            return None
        return self.components[component_key]

    def has_component(self, component_key: str, *other_component_keys: str) -> bool:
        for component in [component_key] + list(other_component_keys):
            if component not in self.components.keys():
                return False
        return True

    def remove_component(self, component_key: str):
        if component_key in self.components.keys():
            self.components.pop(component_key)


class Component:
    key: str = None


class System:
    key: str = None
    requiredComponents = []

    def update(self): ...


class Renderer(System):
    def __init__(self):
        self.key = "renderer"
        self.requiredComponents = ["position", "graphic"]

    def render_entity(self, entity: Entity, surface: pygame.Surface):
        component_graphic: GraphicComponent = entity.get_component("graphic")
        component_position: PositionComponent = entity.get_component("position")

        component_graphic.rect.x = component_position.x
        component_graphic.rect.y = component_position.y

        surface.blit(component_graphic.image, component_graphic.rect)


class PositionComponent(Component):
    def __init__(self):
        self.key = "position"
        self.__vector = pygame.math.Vector2((0, 0))
        self.__layer = 0

    @property
    def x(self):
        return self.__vector.x

    @property
    def y(self):
        return self.__vector.y

    @property
    def z(self):
        return self.__layer

    @x.setter
    def x(self, value: int | float):
        self.__vector.x = value

    @y.setter
    def y(self, value: int | float):
        self.__vector.y = value

    @z.setter
    def z(self, value: int):
        self.__layer = value


class GraphicComponent(Component):
    def __init__(self):
        self.key = "graphic"
        self.__image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.__rect = self.image.get_rect()

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @image.setter
    def image(self, image: pygame.Surface):
        self.__image = image
        self.__rect = self.__image.get_rect()

    @image.setter
    def image(self, path: str, convert_alpha=True):
        self.__image = pygame.image.load(path)
        if convert_alpha:
            self.__image = self.__image.convert_alpha()
        self.__rect = self.__image.get_rect()


class Scene:
    entities: list[Entity] = []


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.gameCanvas = pygame.Surface((constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.sprites = pygame.sprite.Group()
        # Setup
        self.player = Entity(0, "player")
        self.player.add_component(GraphicComponent())
        self.player.add_component(PositionComponent())
        self.renderer = Renderer()

    def render(self):
        # Blit the game canvas on display
        self.display.blit(pygame.transform.scale(self.gameCanvas, (constants.WIDTH, constants.HEIGHT)), (0, 0))

    def draw(self):
        self.gameCanvas.fill(constants.BG_COLOR1)
        self.sprites.draw(self.gameCanvas)
        self.renderer.render_entity(self.player, self.gameCanvas)
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
            self.update()
            self.draw()
            pygame.display.update()


if __name__ == '__main__':
    Game().run()

# class Player(pygame.sprite.Sprite):
#     def __init__(self, position: tuple, groups: pygame.sprite.Group | list[pygame.sprite.Group]):
#         pygame.sprite.Sprite.__init__(self, groups)
#         self.image = pygame.Surface((TILESIZE, TILESIZE))
#         self.image.fill(YELLOW)
#         self.rect = self.image.get_rect()
#         self.vx, self.vy = 0, 0
#         self.x = x * TILESIZE
#         self.y = y * TILESIZE
#
#     def get_keys(self):
#         self.vx, self.vy = 0, 0
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT] or keys[pygame.K_a]:
#             self.vx = -PLAYER_SPEED
#         if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
#             self.vx = PLAYER_SPEED
#         if keys[pygame.K_UP] or keys[pg.K_w]:
#             self.vy = -PLAYER_SPEED
#         if keys[pygame.K_DOWN] or keys[pygame.K_s]:
#             self.vy = PLAYER_SPEED
#         if self.vx != 0 and self.vy != 0:
#             self.vx *= 0.7071
#             self.vy *= 0.7071
#
#     def collide_with_walls(self, dir):
#         if dir == 'x':
#             hits = pygame.sprite.spritecollide(self, self.game.walls, False)
#             if hits:
#                 if self.vx > 0:
#                     self.x = hits[0].rect.left - self.rect.width
#                 if self.vx < 0:
#                     self.x = hits[0].rect.right
#                 self.vx = 0
#                 self.rect.x = self.x
#         if dir == 'y':
#             hits = pg.sprite.spritecollide(self, self.game.walls, False)
#             if hits:
#                 if self.vy > 0:
#                     self.y = hits[0].rect.top - self.rect.height
#                 if self.vy < 0:
#                     self.y = hits[0].rect.bottom
#                 self.vy = 0
#                 self.rect.y = self.y
#
#     def update(self):
#         self.get_keys()
#         self.x += self.vx * self.game.dt
#         self.y += self.vy * self.game.dt
#         self.rect.x = self.x
#         self.collide_with_walls('x')
#         self.rect.y = self.y
#         self.collide_with_walls('y')
