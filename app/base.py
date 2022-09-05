from typing import TYPE_CHECKING

from base.accessor import GameAccessor, BaseAccessor

if TYPE_CHECKING:
    from base.schemas import GameConfig


class GameApp:

    def __init__(self, config: "GameConfig"):
        self.game = GameAccessor(self)
        self.base = BaseAccessor(self)
        self.config = config

    def run(self):
        self.game.run()
