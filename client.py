import pygame
from module.network import Network
from module.player import Player, Players
from game import Game

width = 1080
height = 720
pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, players):
    win.fill('white')
    for e in players:
        e.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        players = n.send(p)

        p.move()
        for player in players:
            player.receive()

        players.append(p)
        redrawWindow(win, players)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


main()