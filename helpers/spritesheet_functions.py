# source code: https://stackoverflow.com/questions/45526988/does-anyone-have-an-example-of-using-sprite-sheets-in-tandem-with-xml-files

import xml.etree.ElementTree as ET
import pygame

from settings import *


class SpriteSheet:
    """ load an atlas image (spritesheet) pass an associated XML file to dictionary self.animation_frames"""
    def __init__(self, filename, sprite_width, sprite_height):
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        imgfile = path.join(repos, 'spritesheets', filename + ".png")
        xmlfile = path.join(repos, 'spritesheets', filename + ".xml")
        self.spritesheet = pygame.image.load(imgfile).convert_alpha()

        if xmlfile:
            tree = ET.parse(xmlfile)
            self.animation_frames = {}
            for node in tree.iter():
                if node.attrib.get('SPRITEACTION'):
                    spriteaction = node.attrib.get('SPRITEACTION')
                    if spriteaction not in self.animation_frames:
                        self.animation_frames[spriteaction] = {}
                    if node.attrib.get('DIRECTION'):
                        direction = node.attrib.get('DIRECTION')
                        if direction not in self.animation_frames[spriteaction]:
                            self.animation_frames[spriteaction][direction] = []
                        if node.attrib.get('SPRSHEETPOS'):
                            # pos = (node.attrib.get('SPRSHEETPOS'))
                            x = int(node.attrib.get('X'))
                            y = int(node.attrib.get('Y'))
                            width = int(node.attrib.get('WIDTH'))
                            height = int(node.attrib.get('HEIGHT'))
                            img = self.get_image(x, y, width, height)
                            self.animation_frames[spriteaction][direction].append(img)
                            # self.animation_frames[spriteaction][direction].append(pos)

    def get_image(self, x, y, width, height):

        image = pygame.Surface([width, height]).convert()  # Create a new blank image
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (self.sprite_width, self.sprite_height))  # resize image
        image.set_colorkey(BLACK)  # set background to be transparent

        return image
