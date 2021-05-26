import pygame
import math
import sys
from pygame import draw
from pygame.locals import QUIT, K_SPACE
from pygame.sprite import Sprite
from pygame.color import Color

from catapult import Catapult
from alien import Alien
from pingpong import Pingpong
from explosion import Explosion

FPS = 60
pingpong_count = 3
g = 0.7
BASE_Y = 250

CATAPULT_READY = 0
CATAPULT_FIRE = 1

pingpong_READY = 0
pingpong_FLY = 1

MIN_POWER = 1
MAX_POWER = 20

MIN_DIRECTION = 20
MAX_DIRECTION = 85

GAME_INIT = 0
GAME_PLAY = 1
GAME_CLEAR = 2
GAME_OVER = 3

def decrement_pingpongs():
    global pingpong_count
    pingpong_count -= 1

class Background(Sprite):

    def __init__(self):        
        self.sprite_image = 'table.jpeg'
        self.image = pygame.image.load(
                self.sprite_image).convert()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.dx = 1

        Sprite.__init__(self)
        
    # def update(self):
        # self.rect.x -= self.dx
        # if self.rect.x == -800:
        #     self.rect.x = 0

if __name__ == '__main__':
    pygame.init()

    size = (680, 1000)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Beer Pong")

    run = True
    clock = pygame.time.Clock()
    t = 0

    power = 15
    direction = 45

    game_state = GAME_INIT
    background = Background()
    background_group = pygame.sprite.Group()
    background_group.add(background)

    pingpong = Pingpong() 
    pingpong.rect.y = -100   # 위치 변경
    pingpong_group = pygame.sprite.Group()
    pingpong_group.add(pingpong)

    catapult = Catapult(pingpong)    
    catapult.rect.x = 50 # 위치 변경                       
    catapult.rect.y = BASE_Y
    catapult_group = pygame.sprite.Group()
    catapult_group.add(catapult)

    alien = Alien()
    alien.rect.x = 350
    alien.rect.y = BASE_Y
    alien_group = pygame.sprite.Group()
    alien_group.add(alien) 

    explosion = Explosion()
    explosion_group = pygame.sprite.Group()
    explosion_group.add(explosion)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # 초기화면에서 스페이스를 입력하면 시작
                    if game_state == GAME_INIT: 
                        game_state = GAME_PLAY
                    elif game_state == GAME_PLAY: 
                        # GAME_PLAY 상태일 때 스페이스를 입력하면 발사
                        if pingpong.state == pingpong_READY:
                            t = 0
                            catapult.fire(power, direction)

        if game_state == GAME_PLAY:
            # 누르고 있는 키 확인하기.
            keys = pygame.key.get_pressed()  
            if keys[pygame.K_LEFT]:
                catapult.backward()
            elif keys[pygame.K_RIGHT]:
                catapult.forward()
            elif keys[pygame.K_UP]:
                if direction < MAX_DIRECTION:
                    direction += 1
            elif keys[pygame.K_DOWN]:
                if direction > MIN_DIRECTION:
                    direction -= 1    
            elif keys[pygame.K_SPACE]:
                if power > MAX_POWER:
                    power = MIN_POWER
                else:
                    power += 0.2

        if pingpong.state == pingpong_FLY:
            t += 0.5
            pingpong.move(t, 
                       (screen.get_width(), screen.get_height()), 
                       decrement_pingpongs)

        if alien.alive():
            collided = pygame.sprite.groupcollide(
                        pingpong_group, alien_group, False, True)
            if collided:
                explosion.rect.x = \
                    (alien.rect.x + alien.rect.width/2) - \
                     explosion.rect.width/2
                explosion.rect.y = \
                    (alien.rect.y + alien.rect.height/2) - \
                    explosion.rect.height/2

        elif not explosion.alive(): 
            # 외계인도 죽고 폭발 애니메이션도 끝났을 때.
            game_state = GAME_CLEAR
       
        # 외계인이 살아 있는데 돌멩이 수가 0이면 게임 오버.
        if alien.alive() and pingpong_count == 0:
            game_state = GAME_OVER

        if game_state == GAME_PLAY: # 게임 객체 업데이트
            catapult_group.update()
            pingpong_group.update()
            alien_group.update()
        
        # 3) 게임 상태 그리기
        background_group.update()
        background_group.draw(screen)
                
        if game_state == GAME_INIT: 
            # 초기화면
            sf = pygame.font.SysFont("Arial", 20, bold=True)
            title_str = "Beer Pong"
            title = sf.render(title_str, True, (255,0,0))
            title_size = sf.size(title_str)
            title_pos = (screen.get_width()/2 - title_size[0]/2, 100)
            
            sub_title_str = "Press [Space] Key To Start"
            sub_title = sf.render(sub_title_str, True, (255,0,0))
            sub_title_size = sf.size(sub_title_str)
            sub_title_pos = (screen.get_width()/2 - sub_title_size[0]/2, 200)

            screen.blit(title, title_pos)
            screen.blit(sub_title, sub_title_pos)

        elif game_state == GAME_PLAY: 
            # 플레이 화면
            catapult_group.draw(screen)
            pingpong_group.draw(screen)
            alien_group.draw(screen)

            # 파워와 각도를 선으로 표현.
            line_len = power*5 
            r = math.radians(direction)        
            pos1 = (catapult.rect.x+32, catapult.rect.y)
            pos2 = (pos1[0] + math.cos(r)*line_len, 
                    pos1[1] - math.sin(r)*line_len)
            draw.line(screen,Color(255, 0, 0), pos1, pos2)                 

            # 파워와 각도를 텍스트로 표현.
            sf = pygame.font.SysFont("Arial", 15)
            text = sf.render("{0} °, {1} m/s".
                             format(direction, int(power)), True, (0,0,0))
            screen.blit(text, pos2)

            # 돌의 개수를 표시
            sf = pygame.font.SysFont("Monospace", 20)
            text = sf.render("pingpongs : {0}".
                             format(pingpong_count), True, (0,0,255))
            screen.blit(text, (10, 10))

            if not alien.alive():
                explosion_group.update()
                explosion_group.draw(screen)

        elif game_state == GAME_CLEAR: 
            # 게임 클리어
            sf = pygame.font.SysFont("Arial", 20, bold=True)
            title_str = "Congratulations! Mission Complete"
            title = sf.render(title_str, True, (0,0,255))
            title_size = sf.size(title_str)
            title_pos = (screen.get_width()/2 - title_size[0]/2, 100)
            screen.blit(title, title_pos)

        elif game_state == GAME_OVER: 
            # 게임 오버
            sf = pygame.font.SysFont("Arial", 20, bold=True)
            title_str = "Game Over"
            title = sf.render(title_str, True, (255,0,0))
            title_size = sf.size(title_str)
            title_pos = (screen.get_width()/2 - title_size[0]/2, 100)
            screen.blit(title, title_pos)

        pygame.display.flip() 
        clock.tick(FPS)
 
    pygame.quit()
# def main():
#     image = pygame.image.load("circle.png")
#     background = pygame.image.load("table.jpeg")
#     pingpong = pygame.image.load("pingpong.png")
#     pingpong = pygame.transform.scale(pingpong, (50,50))
#     image = pygame.transform.scale(image, (100, 100))
#     while True:
#         Surface.fill((0,0,0))
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == K_SPACE:
#                 pingpong

#         # 배경
#         Surface.blit(background,(0,0))
#         # 첫번째 줄
#         Surface.blit(image,(170,50))
#         Surface.blit(image,(250,50))
#         Surface.blit(image,(330,50))
#         Surface.blit(image,(410,50))
#         # 두번째 줄
#         Surface.blit(image,(210,120))
#         Surface.blit(image,(290,120))
#         Surface.blit(image,(370,120))
#         # 세번재 줄
#         Surface.blit(image,(250,190))
#         Surface.blit(image,(330,190))
#         # 마지막
#         Surface.blit(image,(290,260))

#         # 첫번째 줄
#         Surface.blit(image,(290,620))
#         # 두번째 줄
#         Surface.blit(image,(250,690))
#         Surface.blit(image,(330,690))
#         # 세번째 줄
#         Surface.blit(image,(210,760))
#         Surface.blit(image,(290,760))
#         Surface.blit(image,(370,760))
#         # 네번째 줄
#         Surface.blit(image,(170,830))
#         Surface.blit(image,(250,830))
#         Surface.blit(image,(330,830))
#         Surface.blit(image,(410,830))


#         # 노란색 원그리기 반경 10 , 반경 20
#         pygame.display.update()
#         FPSCLOCK.tick(30)
# if __name__ == '__main__':
#     main()