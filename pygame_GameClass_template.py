# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame
import random
from settings import *
from helpers.spritesheet_functions import *
from sprites import *


class Game:

    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.elapsed_time = 0
        self.dt = 0  # time for 1 mainloop
        self.running = True

        # load background textures
        self.background = pygame.image.load(BACKGROUND).convert()

        # get images from spritesheets- ordered by animation frames
        self.playersprites = SpriteSheet('swimmer', PLAYER_WIDTH, PLAYER_HEIGHT)  # takes file name (not inc file extension)

    # start a new game
    def new(self):
        # init sprite groups
        self.all_sprites = pygame.sprite.Group()

        # generate sprites
        self.player = Player(self, 16, 9, PLAYER_WIDTH, PLAYER_HEIGHT, self.playersprites.animation_frames['idle']['North'][0])  # xpos, ypos, width, height (in TILES i.e. 1 TILE X 2 TILES), image (first frame of North orientation by default)

        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000  # seconds
            self.elapsed_time += self.dt
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, 0))  # draw background
        self.all_sprites.draw(self.screen)

        pygame.display.flip()  # *after* drawing everything, flip the display

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pygame.quit()