import pygame
from pygame import *
import random

pygame.mixer.pre_init(44100, -16, 1, 512)

pygame.init()

clock = pygame.time.Clock()

PARTICLE_EVENT = pygame.USEREVENT
pygame.time.set_timer(PARTICLE_EVENT,30)

is_walk = False
state_m = 'off'
state = 'game'

pygame.mixer.music.load("b489b1be02fc97a.mp3")
pygame.mixer.music.play(-1)

m1 = pygame.mixer.Sound('arkadnaya-igra-power-power-sound-41566.ogg')
m2 = pygame.mixer.Sound('zvuk-najatiya-klavishi.ogg')

W_WIDTH = 820
W_HEIGHT = 690
DISPLAY = (W_WIDTH, W_HEIGHT)
BACKGROUND = (0,0,255)

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = (255,255,255)

MOVE_SPEED = 7
JUMP_SPEED = 10
GRAVITY = 0.5

screen = pygame.display.set_mode(DISPLAY)

font = pygame.font.Font(None, 32)
font1 = pygame.font.Font(None,102)

enemy_i = pygame.image.load('box.png')
new_img_e = pygame.transform.scale(enemy_i,(42,42))

gold_i = pygame.image.load('light.png')
gold_count = 10

heals = 3
new_gold_i = pygame.transform.scale(gold_i,(30,30))
class ParticleStyle:
    def __init__(self):
        self.particles = []
    def process(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][0]+=particle[2][0]
                particle[0][1]+=particle[2][1]
                particle[1]-=0.2
                pygame.draw.circle(screen,pygame.Color('Yellow'),particle[0],int(particle[1]))

    def add_particles(self):
        global x2,y2
        for m in range(10):
            pos_x = x2
            pos_y = y2
            radius = 5
            direction_x = random.randint(-3,3)
            direction_y = random.randint(-3,3)
            particle_element = [[pos_x,pos_y],radius,[direction_x,direction_y]]
            self.particles.append(particle_element)
    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1]>0]
        self.particles = particle_copy

particle_style = ParticleStyle()

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callback_=[]
        self._current_option_index = 0
    def append_options(self,option,callback):
        self._option_surfaces.append(font1.render(option,True,(255,255,255)))
        self._callback_.append(callback)
    def switch(self, direction):
        self._current_option_index = max(0,min(self._current_option_index+direction,len(self._option_surfaces)-1))
    def select(self):
        self._callback_[self._current_option_index]()
    def draw(self,surf,x,y,option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x,y+i*option_y_padding)
            if i == self._current_option_index:
                draw.rect(surf,(0,100,0),option_rect)
            surf.blit(option,option_rect)
class Game_Over:
    def __init__(self):
        screen.fill((0,0,0))
        text1 = font1.render('GameOver', True, (255, 0, 0))
        screen.blit(text1,(100,100))
class Game_WIN:
    def __init__(self):
        screen.fill((0,0,0))
        text1 = font1.render('YOU WIN', True, (0, 255, 0))
        screen.blit(text1,(100,100))
class Start:
    def __init__(self):
        global  state
        state = 'game'
class Off:
    def __init__(self):
        pygame.mixer.music.pause()
class On:
    def __init__(self):
        pygame.mixer.music.unpause()
class Sett:
    def __init__(self):
        global state
        state = 'settings'
menu = Menu()
menu.append_options('start', Start)
menu.append_options('setting', Sett)
menu.append_options('quit',quit)
setting = Menu()
setting.append_options('Music On', On)
setting.append_options('Music Off', Off)

class Player(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load('walk1.png'), (50, 60)))
        self.images.append(pygame.transform.scale(pygame.image.load('walk2.png'), (50, 60)))
        self.images.append(pygame.transform.scale(pygame.image.load('walk3.png'), (50, 60)))
        self.images.append(pygame.transform.scale(pygame.image.load('walk4.png'), (50, 60)))
        self.images.append(pygame.transform.scale(pygame.image.load('walk5.png'), (50, 60)))
        self.images.append(pygame.transform.scale(pygame.image.load('walk6.png'), (50, 60)))
        self.images.append(pygame.transform.scale(pygame.image.load('walk7.png'), (50, 60)))
        self.images.append(pygame.transform.scale(pygame.image.load('walk8.png'), (50, 60)))
        self.images.append(pygame.transform.scale(pygame.image.load('walk9.png'), (50, 60)))
        self.images.append(pygame.transform.scale(pygame.image.load('walk10.png'), (50, 60)))
        self.index = 0
        self.image = self.images[self.index]
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.startX = x
        self.startY = y

        self.rect = Rect(x, y, 50, 60)

    def update(self, left, right, up, platform):
        global x2,y2
        if is_walk:
            self.rect.x += self.xvel
            self.collide(self.xvel, 0, platform)
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]
        if up:
            if self.onGround:
                self.yvel = -JUMP_SPEED
        if left:
            self.xvel = -MOVE_SPEED
            self.image = pygame.transform.flip(self.image, True, False)
        if right:
            self.xvel = MOVE_SPEED
        if not (left or right):
            self.xvel = 0
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platform)
        x2 = self.rect.x
        y2 = self.rect.y

    def collide(self, xvel, yvel, platform):
        for p in platform:
            if sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = new_img_e
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Gold(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = new_gold_i
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(120, W_WIDTH - 120)
        self.rect.y = random.randint(120, W_HEIGHT - 120)
    def collide(self, platform):
        for p in platform:
            if sprite.collide_rect(self, p):
                self.rect.x = random.randint(120, W_WIDTH - 120)
                self.rect.y = random.randint(120, W_HEIGHT - 120)
        for j in enemy:
            if sprite.collide_rect(self,j):
                self.rect.x = random.randint(120, W_WIDTH - 120)
                self.rect.y = random.randint(120, W_HEIGHT - 120)

enemy = pygame.sprite.Group()
gold1 = pygame.sprite.Group()
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x,y,PLATFORM_WIDTH,PLATFORM_HEIGHT)
def draw_timer(screen, time_left):
    text = font.render("Time left: " + str(time_left), True, (255, 255, 255))
    screen.blit(text, (250, 250))
def main():
    global  gold_count, is_walk
    hero = Player(55,55)
    left = right = False
    up = False
    entities = pygame.sprite.Group()
    platform = []
    entities.add(hero)
    level = [
        '---------------------------'
        '-                        -',
        '-                        -',
        '-                        -',
        '-                        -',
        '-      ----              -',
        '-                  ----  -',
        '-                 -      -',
        '-   --------             -',
        '-                        -',
        '-                        -',
        '-                ---     -',
        '-                        -',
        '-           --           -',
        '-   -----     -          -',
        '-                        -',
        '-                        -',
        '-  --         --         -',
        '-    -                   -',
        '-         -              -',
        '-                        -',
        '--------------------------']
    timer = pygame.time.Clock()
    x=y=0
    for row in level:
        for col in row:
            if col == '-':
                pf = Platform(x,y)
                entities.add(pf)
                platform.append(pf)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    enemy1 = Enemy(100,600)
    enemy.add(enemy1)
    entities.add(enemy1)

    enemy2 = Enemy(600, 600)
    enemy.add(enemy2)
    entities.add(enemy2)

    enemy3 = Enemy(700,122)
    enemy.add(enemy3)
    entities.add(enemy3)

    enemy4 = Enemy(600, 278)
    enemy.add(enemy4)
    entities.add(enemy4)

    for i in range(15):
        gold = Gold()
        entities.add(gold)
        gold1.add(gold)

    pygame.display.set_caption('ya hochu cushat')
    bg = Surface((W_WIDTH,W_HEIGHT))
    bg.fill(Color(BACKGROUND))
    time1 = 40
    pygame.time.set_timer(USEREVENT + 1, 1000)

    while 1:

        global state, heals,x2,y2
        timer.tick(60)
        screen.blit(bg, (0, 0))
        hero.update(left,right,up,platform)
        entities.draw(screen)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            collected_gold = pygame.sprite.spritecollide(hero, gold1,True)
            if len(collected_gold)>0:
                gold_count -= len(collected_gold)
                if e.type == PARTICLE_EVENT:
                    particle_style.add_particles()
                m1.play()
                if gold_count == 0:
                    state = 'win'
            collected_enemy = pygame.sprite.spritecollide(hero,enemy,True)
            if len(collected_enemy)>0:
                heals -= 1
                gold_count+=5
                m2.play()
                for i in range(5):
                    gold = Gold()
                    entities.add(gold)
                    gold1.add(gold)
                if heals == 0:
                    state = 'lose'
            if e.type==KEYDOWN:
                if e.key == K_ESCAPE:
                    state = 'menu'
            if state == 'menu':
                if e.type == KEYDOWN:
                    if e.key == K_UP:
                        menu.switch(-1)
                    elif e.key == K_DOWN:
                        menu.switch(1)
                    elif e.key == K_RETURN:
                        menu.select()
            if state == 'settings':
                if e.type == KEYDOWN:
                    if e.key == K_UP:
                        setting.switch(-1)
                    elif e.key == K_DOWN:
                        setting.switch(1)
                    elif e.key == K_RETURN:
                        setting.select()
            if state == 'game':
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                    is_walk = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                    is_walk = True
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True

                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                    is_walk = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                    is_walk = False
                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == USEREVENT + 1:
                    time1 -= 1

        if state =='menu':
            screen.fill((0,0,0))
            menu.draw(screen,100,100,100)
        if state =='settings':
            screen.fill((0,0,0))
            setting.draw(screen,100,100,100)
            text = font.render(f"press 'ESCAPE' to return", True, (255, 255, 255))
            screen.blit(text, (500, 310))
        if state == 'lose':
            Game_Over()
        if state == 'win':
            Game_WIN()

        if time1 == 0 and state!='win':
            state = 'lose'
        text = font.render(f"Time:{time1}", True, (0, 0, 0))
        screen.blit(text, (700, 10))
        text = font.render(f"(press 'ESCAPE' for menu)  Gold left: {gold_count}   Lives: {heals}  ", True, (0,0,0))
        screen.blit(text, (10, 10))
        particle_style.process()
        pygame.display.update()

if __name__ == '__main__':
    main()