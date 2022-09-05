from typing import TYPE_CHECKING

from pygame.sprite import Group, collide_circle
from pygame.time import Clock
from pygame import init, mixer, display, draw, event, QUIT, KEYDOWN, K_SPACE, quit

if TYPE_CHECKING:
    from app.base import GameApp
    from base.schemas import GameConfig


class GameAccessor:

    def __init__(self, app: "GameApp"):
        self.app = app
        self.sprites = None
        self.created_mobs = None
        self.player = None
        self.mice = None
        self.dogs = None
        self.trees = None

    def run(self):
        self.app.base.init_window()
        self.app.base.loop()

    def create_game(self):
        self.sprites = Group()
        self.created_mobs = Group()
        self.mice = Group()
        self.dogs = Group()
        self.trees = Group()

    def create_bar(self):
        pass

    def create_player(self):
        pass

    def create_trees(self):
        pass

    def create_mice(self):
        pass

    def create_dogs(self):
        pass

    def set_pause(self):
        pass


class BaseAccessor:

    def __init__(self, app: "GameApp"):
        self.app = app
        self.screen = None
        self.clock = None
        self.is_running = False
        self.is_pause = False

    def create_screen(self):
        self.screen = display.set_mode(
            (
                self.app.config.base.width,
                self.app.config.base.height,
            )
        )

    def create_clock(self):
        self.clock = Clock()

    def render_screen(self):
        self.screen.fill((0, 0, 0))

    def handle_events(self):
        for ev in event.get():
            if ev.type == QUIT:
                self.is_running = False

    def init_window(self):
        init()
        mixer.init()
        self.create_screen()
        self.create_clock()

    def renew_states(self):
        pass

    def loop(self):
        self.is_running = True

        while self.is_running:
            self.clock.tick(self.app.config.base.fps)
            self.handle_events()
            self.renew_states()
            self.render_screen()
            display.flip()

        quit()
