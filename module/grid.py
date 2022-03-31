import os
import pygame
from module.infinity_for import For


class Grid:
    def __init__(self, win_size, size=200):
        self.win_size = win_size
        self.size = size

    def create_grid(self, number_element, rows):
        self.square = []
        size = self.size
        for i in range(number_element // rows):
            for j in range(rows):
                self.square.append(pygame.Rect((100 + size * j, 100 + self.size * i), (size, size)))

        if number_element % rows != 0:
            i = number_element // rows
            for j in range(number_element % rows):
                self.square.append(pygame.Rect((100 + size * j, 100 + size * i), (size, size)))
