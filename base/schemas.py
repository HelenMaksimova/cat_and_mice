from typing import ClassVar, Type

from marshmallow import Schema
from marshmallow_dataclass import dataclass


@dataclass
class BaseSettings:
    width: int
    height: int
    bar_height: int
    an_time: int
    fps: int

    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class GameSettings:
    trees: int
    dogs: int
    mice: int

    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class PlayerSettings:
    step: int
    tries: int
    stars: int

    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class MobsSettings:
    step: int
    size: int
    destination: int

    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class GameConfig:
    base: BaseSettings
    game: GameSettings
    player: PlayerSettings
    mobs: MobsSettings

    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class GameImages:
    pass
