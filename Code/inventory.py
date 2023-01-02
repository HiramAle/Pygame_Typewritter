import pygame
import scene
import constants
import json
from enum import Enum


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
        self.dragging = False
        with open("../Data/items.json") as data:
            items_data = json.load(data)
        self.name = items_data[item_id.value]["name"]
        self.description = items_data[item_id.value]["description"]
        self.icon = pygame.image.load(items_data[item_id.value]["iconPath"]).convert_alpha()


class Inventory:
    def __init__(self):
        self.items: dict[str, int] = {}

    def add_item(self, item_id: ItemId, quantity: int):
        if self.has_item(item_id):
            self.items[item_id.value] += quantity
        else:
            self.items[item_id.value] = quantity

    def remove_item(self, item_id: ItemId, quantity: int):
        if self.has_item(item_id):
            if self.items[item_id.value] - quantity < 0:
                self.items[item_id.value] = 0
            else:
                self.items[item_id.value] -= quantity

    def has_item(self, item_id: ItemId):
        return item_id.value in self.items.keys()


class InventorySlot:
    def __init__(self, position: tuple):
        self.position = pygame.math.Vector2(position)
        self.item: Item = None
        self.rect = pygame.Rect(self.position.x, self.position.y, constants.INV_TILE_SIZE, constants.INV_TILE_SIZE)

    def draw(self, display: pygame.Surface):
        pygame.draw.rect(display, constants.WHITE, self.rect)

    def draw_item(self, display: pygame.Surface):
        if self.item is not None and not self.item.dragging:
            image = pygame.transform.scale(self.item.icon, (constants.INV_TILE_SIZE, constants.INV_TILE_SIZE))
            display.blit(image, self.position)
        if self.item is not None and self.item.dragging:
            mouse_position = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) / 2
            image = pygame.transform.scale(self.item.icon, (constants.INV_TILE_SIZE, constants.INV_TILE_SIZE))
            display.blit(image, mouse_position - (self.rect.width / 2, self.rect.height / 2))


class SceneInventory(scene.Scene):
    def __init__(self, display: pygame.Surface, target):
        super().__init__("inventory", display)
        self.rows = 4
        self.columns = 9
        self.slots: list[InventorySlot] = []
        self.target = target
        self.padding = 2
        self.movingItem: Item = None
        self.movingSlot: InventorySlot = None
        self.set_slots()

    def event_loop(self, manager: scene.SceneManager, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.input(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.drag_item()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.place_item()

    def input(self, event: pygame.event.Event) -> None:
        key = pygame.key.name(event.key)
        item_ids = [item.value for item in ItemId]

        if key in item_ids:
            self.add_item(Item(ItemId(key)))

    def set_slots(self):
        for y in range(self.display.get_height() // 2 - ((constants.INV_TILE_SIZE + self.padding) * self.rows) // 2,
                       self.display.get_height() // 2 + ((constants.INV_TILE_SIZE + self.padding) * self.rows) // 2,
                       constants.INV_TILE_SIZE + self.padding):
            for x in range(
                    self.display.get_width() // 2 - ((constants.INV_TILE_SIZE + self.padding) * self.columns) // 2,
                    self.display.get_width() // 2 + ((constants.INV_TILE_SIZE + self.padding) * self.columns) // 2,
                    constants.INV_TILE_SIZE + self.padding):
                self.slots.append(InventorySlot((x, y)))

    def draw_slots(self):
        for slot in self.slots:
            slot.draw(self.display)
        for slot in self.slots:
            slot.draw_item(self.display)

    def place_item(self):
        mouse_position = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) / 2
        for slot in self.slots:
            if slot.rect.collidepoint(mouse_position):
                if slot.item is None:
                    self.remove_item(self.movingItem)
                    self.add_item(self.movingItem, slot)
                else:
                    temp = slot.item
                    self.remove_item(self.movingItem)
                    slot.item = self.movingItem
                    self.movingSlot.item = temp

        self.movingItem.dragging = False
        self.movingItem = None

    def add_item(self, item: Item, slot: InventorySlot = None):
        if slot is None:
            for slot in self.slots:
                if slot.item is None:
                    slot.item = item
                    break
        else:
            if slot.item is None:
                slot.item = self.movingItem

    def drag_item(self):
        mouse_position = pygame.math.Vector2((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])) / 2
        for slot in self.slots:
            if slot.rect.collidepoint(mouse_position) and slot.item is not None:
                slot.item.dragging = True
                self.movingItem = slot.item
                self.movingSlot = slot
                break

    def remove_item(self, item: Item):
        for slot in self.slots:
            if slot.item is item:
                slot.item = None
                break

    def draw(self) -> None:
        self.display.fill(constants.BG_COLOR1)
        self.draw_slots()


