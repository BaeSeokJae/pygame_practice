from pygame.color import Color
from animation import Animation

class Explosion(Animation):
    def __init__(self):
        self.sprite_image = 'explosionsprite.png'
        self.sprite_width = 100
        self.sprite_height = 100 
        self.sprite_columns = 25
        self.fps = 16
        self.init_animation()
       
    def update(self): 
        self.calc_next_frame()
        if self.current_frame == self.sprite_columns:
            self.current_frame = 0
            self.kill()
        
        rect = (self.sprite_width*self.current_frame, 0, 
                self.sprite_width, self.sprite_height)
        self.image.blit( self.sprite_sheet, (0, 0), rect)
        self.image.set_colorkey(Color(255, 0, 255))