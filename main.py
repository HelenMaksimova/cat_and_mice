from yaml import safe_load

from app.base import GameApp
from base.schemas import GameConfig


def create_app(config_path: str):
    config = parse_config(config_path)
    return GameApp(config=config)


def parse_config(config_path: str):
    with open(config_path) as file:
        document = file.read()
    config = safe_load(document)
    return GameConfig.Schema().load(config)


def run():
    app = create_app('config/config.yaml')
    app.run()


run()