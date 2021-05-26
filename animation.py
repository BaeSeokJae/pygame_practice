import pygame
from pygame import Surface
from pygame.color import Color
from pygame.sprite import Sprite

class Animation(Sprite):
    def init_animation(self):
        Sprite.__init__(self)

        self.sprite_sheet = pygame.image.load(self.sprite_image).convert()
        self.current_frame = 0
        self.image = Surface((self.sprite_width, self.sprite_height))

        rect = (self.sprite_width*self.current_frame, 0, 
                self.sprite_width, self.sprite_height)
        self.image.blit( self.sprite_sheet, (0, 0), rect)
        self.image.set_colorkey(Color(255, 0, 255))
        self.rect = self.image.get_rect()        
        self.elapsed = pygame.time.get_ticks()
        self.threshold =  1000/self.fps
 
    def calc_next_frame(self):
       tick = pygame.time.get_ticks()
       if tick - self.elapsed > self.threshold:
           self.elapsed = tick
           if self.current_frame == self.sprite_columns:
               self.current_frame = 0
           else:
               self.current_frame += 1