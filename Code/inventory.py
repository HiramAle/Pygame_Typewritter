from enum import Enum
import pygame
import constants
import base_game
import json


class ItemId(Enum):
    diamond = "0"
    bottleOfEnchanting = "1"
    carrot = "2"
    enchantedBook = "3"
    bow = "4"


class Item:
    name: str
    description: str
    icon: pygame.Surface

    def __init__(self, item_id: ItemId):
        with open("../Data/items.json") as data:
            items_data = json.load(data)
        self.name = items_data[item_id.value]["name"]
        self.description = items_data[item_id.value]["description"]
        self.icon = pygame.image.load(items_data[item_id.value]["iconPath"]).convert_alpha()


class InventoryItem(pygame.sprite.Sprite):
    def __init__(self, item: Item, groups: pygame.sprite.Group | list[pygame.sprite.Group]):
        super().__init__(groups)
        self.position = pygame.math.Vector2(0, 0)
        self.item = item
        self.defaultImage = pygame.transform.smoothscale(item.icon, (constants.TILE_SIZE * 2, constants.TILE_SIZE * 2))
        self.image = self.defaultImage
        self.rect = self.image.get_rect()
        self.quantity = 0
        self.font = pygame.font.Font("../Assets/monogram.ttf", 30)
        self.name = self.font.render(item.name, False, constants.WHITE)
        self.nameRect = self.name.get_rect()
        self.info = pygame.Surface((self.name.get_width() + 5, self.name.get_height()))
        self.info.fill(constants.BG_COLOR2)
        self.nameRect.center = (self.info.get_width() / 2, self.info.get_height() / 2)
        self.info.blit(self.name, self.nameRect)
        self.infoRect = self.info.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # self.hoverSurface = self.mask.to_surface()
        # self.hoverSurface.set_colorkey((0, 0, 0))
        # self.hoverSurface = pygame.transform.scale(self.hoverSurface,
        #                                            (constants.TILE_SIZE * 2 + 5, constants.TILE_SIZE * 2 + 5))
        # self.hoverSurfaceRect = self.hoverSurface.get_rect(center=(constants.TILE_SIZE-1, constants.TILE_SIZE-1))

        self.hoverSurface = pygame.Surface((constants.TILE_SIZE * 2, constants.TILE_SIZE * 2))
        self.hoverSurface.fill((220, 220, 220, 128))

        self.newSurface = pygame.Surface((constants.TILE_SIZE * 2, constants.TILE_SIZE * 2))
        self.newSurface.set_colorkey((0, 0, 0))
        self.newSurface.blit(self.hoverSurface, (0, 0))
        self.newSurface.blit(self.image, (0, 0))

    def hover(self, game_canvas: pygame.Surface, offset: tuple, cursor_position: tuple):
        rect = self.rect.copy()
        rect.x += offset[0]
        rect.y += offset[1]

        if rect.collidepoint(cursor_position[0] / 2, cursor_position[1] / 2):
            self.infoRect.bottomleft = (cursor_position[0] / 2, cursor_position[1] / 2)
            game_canvas.blit(self.info, self.infoRect)
            self.image = self.newSurface
        else:
            self.image = self.defaultImage

    def update(self):
        self.rect.center = self.position


class Inventory(pygame.sprite.Sprite):
    def __init__(self, game: base_game.Game, groups: pygame.sprite.Group | list[pygame.sprite.Group]):
        super().__init__(groups)
        self.position = pygame.math.Vector2(constants.CANVAS_WIDTH / 2 - 256 / 2, constants.CANVAS_HEIGHT / 2 - 128 / 2)
        self.image = pygame.Surface((256, 128))
        self.image.fill(constants.BLUE)
        self.rect = self.image.get_rect(topleft=self.position)
        self.itemsGroup = pygame.sprite.Group()
        self.items: list[InventoryItem] = [
            InventoryItem(Item(ItemId.carrot), self.itemsGroup),
            InventoryItem(Item(ItemId.enchantedBook), self.itemsGroup),
            InventoryItem(Item(ItemId.bottleOfEnchanting), self.itemsGroup),
            InventoryItem(Item(ItemId.diamond), self.itemsGroup),
            InventoryItem(Item(ItemId.bow), self.itemsGroup)]
        self.cellSize = constants.TILE_SIZE * 2
        self.rows = int(self.image.get_height() / self.cellSize)
        self.columns = int(self.image.get_width() / self.cellSize)
        self.offset = self.position.x, self.position.y
        self.game = game

    def draw_grid(self):
        for row in range(self.rows + 1):
            pygame.draw.line(self.image, constants.WHITE, (0, row * self.cellSize),
                             (self.columns * self.cellSize, row * self.cellSize))
        for column in range(self.columns + 1):
            pygame.draw.line(self.image, constants.WHITE, (column * self.cellSize, 0),
                             (column * self.cellSize, self.rows * self.cellSize))

    def place_items(self):
        x = 0
        y = 0
        for item in self.items:
            if x + self.cellSize > self.image.get_width():
                x = 0
                y += self.cellSize

            item.position.x = x + self.cellSize / 2
            item.position.y = y + self.cellSize / 2

            x += self.cellSize

    def check_hover(self):
        cursor_position = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        for item in self.items:
            item.hover(self.game.gameCanvas, self.offset, cursor_position)

    def update(self, dt: float):
        self.image.fill(constants.BLUE)
        self.check_hover()

        self.place_items()
        self.itemsGroup.draw(self.image)
        self.itemsGroup.update()
        self.draw_grid()
