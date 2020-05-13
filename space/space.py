from scenes.game.spaceship import SpaceshipScene


class Space:
    PLANETS_NUMBER = 12

    def __init__(self, game, name='world'):
        self.__game = game
        self.__name = name
        self.spaceship_scene = None
        self.spacemap_scene = None

    def initialize(self):
        self.__game.file_manager.reset()
        self.__game.file_manager.create_space_storage(self.__name)
        self.spaceship_scene = SpaceshipScene(self.__game)
        self.spaceship_scene.initialize()
        self.__game.set_scene(self.spaceship_scene, False)
