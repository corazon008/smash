from PIL import Image as img
import time
import os
import pygame
from pathlib import Path


def load(path):
    path = Path(path)
    try:
        return Gif(path.with_name(path.stem + '.gif'))
    except FileNotFoundError:
        return Image(path.with_name(path.stem + '.png'))


class Var:
    size = [100, 100]

    def __init__(self, name):
        try:
            path = Path('assets/character')
            path = path / name
            for e in os.listdir(path):
                if os.path.isfile(path / e):
                    file = e
            self._size = [int(e) for e in file.split('x')]
        except Exception as e:
            pass

    def get_size(self):
        try:
            return self._size
        except Exception as e:
            pass
            return self.size


class Image:

    def __init__(self, path):
        self.path = path
        self.name = self.path.parts[2]
        self.var = Var(self.name)
        self.size = self.var.get_size()
        self.image = pygame.transform.scale(pygame.image.load(path), self.size)

    def get_image(self):
        return self.image

    def send(self):
        self.image = pygame.image.tostring(self.image, 'RGB')

    def receive(self):
        self.image = pygame.image.fromstring(self.image, self.size, 'RGB')


class Gif(Var):
    def __init__(self, path):
        """to flip gif : https://onlinegiftools.com/flip-gif"""
        self.path = path
        self.name = self.path.parts[2]
        self.var = Var(self.name)
        self.size = self.var.get_size()

        self.gif = img.open(path)

        self.frames = []
        self.frames_nb = self.gif.n_frames
        for frame_index in range(self.frames_nb):
            self.gif.seek(frame_index)
            frame_rgba = self.gif.convert("RGBA")
            pygame_image = pygame.image.fromstring(
                frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
            )
            self.frames.append(pygame.transform.scale(pygame_image, self.size))

        self.count = 0
        self.image = iter(self)

    def __iter__(self):
        while True:
            yield self.frames[self.count % self.frames_nb]
            self.count += 1
            time.sleep(1 / 15)

    def draw(self):
        return next(self.image)

    def get_image(self):
        return next(self.image)

    def send(self):
        del self.image
        for i, images in enumerate(self.frames):
            self.frames[i] = pygame.image.tostring(images, 'RGB')

    def receive(self):
        self.image = iter(self)
        for i, images in enumerate(self.frames):
            self.frames[i] = pygame.image.fromstring(images, self.size, 'RGB')
