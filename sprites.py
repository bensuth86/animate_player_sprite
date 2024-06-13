import pygame
from math import fabs
from math import sqrt as sqrt
from settings import *
vec = pygame.math.Vector2  # 2D vector - x = vec.x  y = vec.y


class Static_sprite(pygame.sprite.Sprite):

    def __init__(self, game, x, y, width, height, image):

        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.game = game
        self.image = image
        self.rect = image.get_rect()
        self.pos = vec(x * TILESIZE, y * TILESIZE)  # position in pixels
        self.rect.topleft = self.pos

    def draw(self):
        self.game.screen.blit(self.image, self.rect.topleft)


class Mobile_sprite(Static_sprite):

    def __init__(self, game, x, y, width, height, image):

        super().__init__(game, x, y, width, height, image)

        self.vel = vec(0, 0)  # velocity vector
        self.current_frame = 0
        self.timer = 0  # used to trigger next frame for animations
        self.direction = 'North'
        # key input or indirect occurance e.g. falling off platform, determines self.NSEW bool and subsequent direction for example
        # SouthEast points.items == False, True, True, False
        self.NSEW = {'North': True,
                    'South': False,
                    'East': False,
                    'West': False}
        self.actionvar = "idle"  # current sprite action
        self.newaction = "idle"  # new sprite action on e.g. keyboard input- jumping, walking etc

    def collide_platforms(self, platforms):

        self.rect.y += 1  # move player rect down a pixel to check for collision with platform
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 1  # move back up having check for collision
        if len(hits) > 0 and self.vel.y >= 0:  # can only fall onto platforms- able to jump through them

            if self.pos.y < hits[0].rect.bottom:  # bottom of sprite rect above bottom of platform rect
                self.pos.y = hits[0].rect.top  # set sprite y position to top of platform
                return True

    def change_action(self, newaction):
        """ change action from e.g. jumping to falling.  First check current action to see if action has actually changed then return new actionvar"""
        self.timer = 0  # set timer at start of animation.  Resets to zero when switching to other animation
        if self.actionvar != newaction:
            self.actionvar = newaction
            self.current_frame = 0

    def animate(self, time_period):

        frames = self.game.playersprites.animation_frames[self.actionvar][self.direction]
        current_frame = int((self.game.elapsed_time // time_period) % len(frames))
        self.image = frames[current_frame]


class Player(Mobile_sprite):

    def __init__(self, game, x, y, width, height, image):
        super().__init__(game, x, y, width, height, image)

        self.runspeed = 6
        self.newaction = "idle"
        self.dead = False
        self.orientation = {'North': [True, False, False, False],
                            'South': [False, True, False, False],
                            'East': [False, False, True, False],
                            'West': [False, False, False, True],
                            'NorthWest': [True, False, False, True],
                            'NorthEast': [True, False, True, False],
                            'SouthWest': [False, True, False, True],
                            'SouthEast': [False, True, True, False]}

    def equatedirection(self):

        orientated = list(self.NSEW.values())
        for key, value in self.orientation.items():
            if orientated == value:
                self.direction = key
                break
        # print(self.direction)

    def collide_enemy(self, enemies):

        # collision with enemy from all other directions (players death)
        hits = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_rect_ratio(0.7))  # check hits to the right

        if hits and self.vel.y > 0:
            hits[0].kill()

        elif hits:
            self.dead = True
            # self.newaction = "die"

    def collide_pick_up(self, pick_ups):

        hits = pygame.sprite.spritecollide(self, pick_ups, False, pygame.sprite.collide_rect_ratio(0.5))
        if hits:
            hits[0].kill()
            hits[0].apply_pickup(self)

    def update(self):

        self.vel = vec(0, 0)
        self.NSEW = dict.fromkeys(self.NSEW, False)  # reset orientation dict to reconfigure direction
        keys = pygame.key.get_pressed()

        # Check platform collision
        # if self.collide_platforms(self.game.platforms) is True:
        #     self.vel = vec(0, 0)
        #     self.newaction = "idle"
        # else:
        #     self.vel = vec(0, FALL_VELOCITY)
        #     self.newaction = "fall"
        self.newaction = "idle"
        # KEY INPUT
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.vel.x = -self.runspeed
            self.NSEW['West'] = True
            self.newaction = "swim"

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.vel.x = self.runspeed
            self.NSEW['East'] = True
            self.newaction = "swim"

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.vel.y = -self.runspeed
            self.NSEW['North'] = True
            self.newaction = "swim"

        if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.vel.y = self.runspeed
            self.NSEW['South'] = True
            self.newaction = "swim"

        # check sprite collisions
        # self.collide_enemy(self.game.enemies)
        # self.collide_pick_up(self.game.pick_ups)
        self.equatedirection()
        self.change_action(self.newaction)  # change self.actionvar to new action
        self.animate(0.2)

        # wrap around the sides of the screen
        self.pos.x = 0 if self.pos.x > WIDTH else self.pos.x
        self.pos.x = WIDTH if self.pos.x < 0 else self.pos.x
        self.pos.y = 0 if self.pos.y > HEIGHT else self.pos.y
        self.pos.y = HEIGHT if self.pos.y < 0 else self.pos.y

        self.pos += self.vel
        self.rect.midbottom = self.pos


class Platform(Static_sprite):

    def __init__(self, start_x, start_y, image):
        "Generates a single platform tile."
        super().__init__(start_x, start_y, image)


class Pick_up(Static_sprite):

    def __init__(self, start_x, start_y, image):
        "Generates a single pick_up tile."
        super().__init__(start_x, start_y, image)

    def apply_pickup(self, player):
        player.game.score += 50
