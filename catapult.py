import pygame
from pygame.color import Color
from animation import Animation
from pingpong import Pingpong

g = 0.7
BASE_Y = 250

CATAPULT_READY = 0
CATAPULT_FIRE = 1

STONE_READY = 0
STONE_FLY = 1

MIN_POWER = 1
MAX_POWER = 20

MIN_DIRECTION = 20
MAX_DIRECTION = 85

GAME_INIT = 0
GAME_PLAY = 1
GAME_CLEAR = 2
GAME_OVER = 3

class Catapult(Animation):
    # STATE : CATAPULT_READY -> CATAPULT_FIRE
    #           ^------|
    # READY일 때만 이동 가능
    # FIRE일 때는 아무것도 못함.
    def __init__(self, pingpong):
        self.sprite_image = 'catapult.png'
        self.sprite_width = 32
        self.sprite_height = 32
        self.sprite_columns = 5
        self.fps = 30
        self.pingpong = pingpong
        self.state = CATAPULT_READY
        self.init_animation()

    def update(self):
        if self.state == CATAPULT_FIRE:
            self.calc_next_frame()

            if self.current_frame == self.sprite_columns:
                self.current_frame = 0
                # 돌멩이 날리기 시작
                self.state = CATAPULT_READY
                self.pingpong.setup(
                    (self.rect.x, self.rect.y),
                    self.power, self.direction)
        else:
            self.current_frame = 0
                
        rect = (self.sprite_width*self.current_frame, 0, 
                self.sprite_width, self.sprite_height)
        self.image.blit( self.sprite_sheet, (0, 0), rect)
        self.image.set_colorkey(Color(255, 0, 255))

    def forward(self):
        if self.rect.x < 100:
            self.rect.x += 1

    def backward(self):
        if self.rect.x > 0:
            self.rect.x -= 1

    def fire(self, power, direction):
        self.state = CATAPULT_FIRE
        self.power = power
        self.direction = direction