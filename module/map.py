import pygame, pytmx, pyscroll, os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Map:
    name: str
    walls: list
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    gravity: int


class MapManager:
    def __init__(self, screen, player, map):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.gravity = 4
        self.current_map = map  # endroit ou la carte a ete choisie

        self.path = Path('assets/map')
        for map in os.listdir(self.path):
            map_path = self.path / map
            if os.path.isdir(map_path):
                map_path / map
                self.register_map(map_path, Path(map).stem)

        self.teleport_player("spawn")

    def check_collision(self):
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position = [point.x, point.y]
        self.player.save_location()

    def register_map(self, path, name):
        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(path / f'{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # definir les collissions
        walls = [pygame.Rect(obj.x, obj.y, obj.width, obj.height) for obj in tmx_data.objects if
                 obj.type == "collision"]

        # dessiner le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        group.add(self.player)

        # creer un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, self.gravity)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.check_collision()
        self.get_group().update()

    def physics(self):
        self.player.gravity(self.get_map().gravity)
        self.check_collision()

    def add_player(self, *players):
        self.get_group().remove_sprites_of_layer(self.get_group().layers()[0])
        for player in players:
            self.get_group().add(player)
