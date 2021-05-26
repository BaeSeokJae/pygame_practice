import math
import pygame
from pygame.color import Color
from animation import Animation

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

class Pingpong(Animation):
    # STATE : STONE_READY -> pingpong_FLY
    #           ^---------------|
    # READY일 때만 이동 가능
    # FIRE일 때는 아무것도 못함.
    def __init__(self):
        self.sprite_image = 'pingpong.png'
        self.sprite_width = 8
        self.sprite_height = 8
        self.sprite_columns = 4
        self.fps = 20
        self.state = STONE_READY
        self.init_animation()
               
    def update(self): 
        # 돌은 투석기가 발사한 이후부터 목표 또는 
        # 지면에 충돌할 때까지 날기만 하므로
        # 상태에 따른 스프라이트 정지 등은 필요 없음.
        self.calc_next_frame()
                
        rect = (self.sprite_width*self.current_frame, 0, 
                self.sprite_width, self.sprite_height)
        self.image.blit( self.sprite_sheet, (0, 0), rect)
        self.image.set_colorkey(Color(255, 0, 255))

    def setup(self, initial_pos, power, direction):
        self.initial_pos = initial_pos
        self.rect.x = initial_pos[0]
        self.rect.y = initial_pos[1]
        self.power = power
        self.direction = direction
        self.state = STONE_FLY

    def move(self, time, space, decrement_stones):
        pos = self.calculate_position(time, g, self.direction)

        pos = self.map_position(
            self.initial_pos[0], self.initial_pos[1], 
            pos[0], pos[1])
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        if pos[0] > space[0] or pos[1] > space[1]:
            self.state = STONE_READY
            decrement_stones()

    # 포탄 위치 계산
    def calculate_position(self, t, g, direction):
        r = math.radians(direction)
        x = self.power*math.cos(r)*t
        y = self.power*math.sin(r)*t - 0.5*g*math.pow(t, 2)

        return (int(x), int(y))

    # 포탄의 위치를 화면 좌표에 맞게 변환
    def map_position(self, x, y, new_x, new_y):
        return (x + new_x, y + (new_y*-1))