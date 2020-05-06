from drawable_objects.player import Player


class Dungeon:
    def __init__(self, player: Player):
        self.__scene = None
        self.__player = player

    def initialize(self, biom: str):
        pass
