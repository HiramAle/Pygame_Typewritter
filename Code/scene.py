from __future__ import annotations
import pygame
import basic_player
import basic_inventory
import constants


class Scene:
    def __init__(self, name: str, display: pygame.Surface):
        self.name = name
        self.display = display
        self.sprites = pygame.sprite.Group()

    def event_loop(self, manager: SceneManager, event: pygame.event.Event) -> None: ...

    def input(self, event: pygame.event.Event) -> None: ...

    def update(self, dt: float, manager: SceneManager) -> None: ...

    def draw(self) -> None: ...


class BasicScene(Scene):
    def __init__(self, display: pygame.Surface):
        super().__init__("basic", display)
        self.player = basic_player.Player(self.sprites)

    def draw(self) -> None:
        self.display.fill(constants.BG_COLOR1)
        self.sprites.draw(self.display)

    def update(self, dt: float, manager: SceneManager) -> None:
        self.sprites.update(dt)


class SceneManager:
    def __init__(self):
        self.sceneStack: list[Scene] = []

    def enter_scene(self, new_scene: Scene):
        self.sceneStack.append(new_scene)

    def exit_scene(self):
        self.sceneStack.pop()

    def set_scene(self, new_scene: Scene):
        self.sceneStack = [new_scene]

    def input(self):
        if self.sceneStack:
            self.sceneStack[-1].input()

    def event_loop(self, event: pygame.event.Event):
        if self.sceneStack:
            self.sceneStack[-1].event_loop(self, event)

    def update(self, dt: float):
        if self.sceneStack:
            self.sceneStack[-1].update(dt, self)

    def draw(self):
        if self.sceneStack:
            self.sceneStack[-1].draw()
