import pygame, os
from module.image import load


class Players:
    def __init__(self):
        self.path = 'assets/character'
        #self.names = [e for e in os.listdir(self.path)]
        self.names = ['link', 'jotaro']
        self.players = dict(
            [[e, Player(e, self.path)] for e in self.names]
                            )

    def send_player(self, name):
        player = self[name]
        player.send()
        return player

    def __getitem__(self, name):
        for i, player in enumerate(self):
            if i == name or player.name == name:
                return player

    def sendable(self, name):
        players = [player.send() for player in self]
        players.remove(self[name])
        return players

    def update(self, player):
        name = player.name
        self.players[name] = player

    def __iter__(self):
        for e in self.players.values():
            yield e


class Player(pygame.sprite.Sprite):
    def __init__(self, name, path='assets/character'):
        super().__init__()

        self.name = name
        self.path = path
        self.images = {
            'still': {'right': load(f'assets/character/{name}/still/still_r'),
                      'left': load(f'assets/character/{name}/still/still_l')},
            'walk': {'right': load(f'assets/character/{name}/walk/walk_r'),
                     'left': load(f'assets/character/{name}/walk/walk_l')},
            'attack': {'right': load(f'assets/character/{name}/attack/att_r'),
                       'left': load(f'assets/character/{name}/attack/att_l')},
            # 'jump': {'right': load(f'assets/character/{name}/jump/jump_r'), 'left': load(f'assets/character/{name}/jump/jump_l')},
        }

        self.current_mvt = 'still'
        self.current_sens = 'right'
        self.change_animation()
        self.rect = self.image.get_rect()
        self.speed = 10

        self.position = [0, 0]
        self.feet = pygame.Rect(*self.position, self.rect.width * 0.5, 12)

        self.save_location()

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self):
        self.image = self.images[self.current_mvt][self.current_sens].get_image()

    def move_right(self):
        self.position[0] += self.speed
        self.current_sens = 'right'
        self.current_mvt = 'walk'
        self.change_animation()

    def move_left(self):
        self.position[0] -= self.speed
        self.current_sens = 'left'
        self.current_mvt = 'walk'
        self.change_animation()

    def attack(self):
        self.current_mvt = 'attack'
        self.change_animation()

    def move_up(self):
        self.position[1] -= self.speed
        #self.current_mvt = 'jump'
        # self.change_animation()

    def move_down(self):
        self.position[1] += self.speed

    def gravity(self, strenght):
        self.position[1] += strenght

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def draw(self, win):
        win.blit(self.image, self.position)

    def move_back(self):
        self.position = self.old_position
        self.update()

    def send(self):
        del self.image
        for states in self.images.values():
            for images in states.values():
                images.send()

    def receive(self):
        self.change_animation()
        for states in self.images.values():
            for images in states.values():
                images.receive()

# arranger le code pour code le nv self.images fonctionne
# creer une variable floor qui est un bool qui vaut True au contace du sol et qui empeche de descendre sous le sol
# d'autre idée que lub1 avaient
