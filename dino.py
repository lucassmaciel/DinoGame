import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

main_file = os.path.dirname(__file__)
sprites_file = os.path.join(main_file, 'sprites')
sounds_file = os.path.join(main_file, 'sounds')

width = 640
height = 480
    
white = (255,255,255)
black = (0,0,0)
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Dino Game')

sprite_sheet = pygame.image.load(os.path.join(sprites_file, 'pixel2.png')).convert_alpha()

sound_collision = pygame.mixer.Sound(os.path.join(sounds_file, 'death.wav'))
sound_collision.set_volume(1)

sound_points = pygame.mixer.Sound(os.path.join(sounds_file,'score.wav'))
sound_points.set_volume(1)

collision = False

choice_obstacle = choice([0, 1])

points = 0

vel_game = 10

def show_message(msg, font_size, color):
    font = pygame.font.SysFont('comicsans', font_size, bold = True)
    message = f'{msg}'
    formatted_text = font.render(message, True, color)
    return formatted_text

def restart_game():
    global points, vel_game, collision, choice_obstacle
    points = 0
    vel_game = 10
    collision = False
    dino.rect.y = height - 64 - 96//2
    dino.jump = False 
    flydino.rect.x = width
    cactus.rect.x = width
    choice_obstacle = choice([0, 1])
    
    
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sound_jump = pygame.mixer.Sound(os.path.join(sounds_file, 'jump.wav'))
        self.sound_jump.set_volume(1)
        self.images_dino = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.images_dino.append(img)
        
        self.index_list = 0
        self.image = self.images_dino[self.index_list]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y = height - 64 - 96//2
        self.rect.topleft = (100, self.pos_y)
        self.jump = False
        self.vel_y = 0

    def pular(self):
        self.vel_y = -14
        self.sound_jump.play()
        
    def update(self):
        self.rect.y += self.vel_y
        self.vel_y += 1
        if self.rect.y >= self.pos_y:
            self.vel_y = 0
            self.rect.y = self.pos_y
        if self.index_list > 1:
            self.index_list = 0
        self.index_list += 0.2
        self.image = self.images_dino[int(self.index_list)]

class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = width - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = width
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= vel_game

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = height - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = width
        self.rect.x -= 10
    
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.choice = choice_obstacle
        self.rect.center = (width,  height - 64)
        self.rect.x = width


    def update(self):
        if self.choice == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = width
            self.rect.x -= vel_game

class FlyDino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images_flydino = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i*32, 0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.images_flydino.append(img)

        self.index_list = 0
        self.image = self.images_flydino[self.index_list]
        self.mask = pygame.mask.from_surface(self.image)
        self.choice = choice_obstacle
        self.rect = self.image.get_rect()
        self.rect.center = (width, 320)
        self.rect.x = width
    
    def update(self):
        if self.choice == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = width
            self.rect.x -= vel_game

            if self.index_list > 1:
                self.index_list = 0
            self.index_list += 0.25
            self.image = self.images_flydino[int(self.index_list)]

every_sprite = pygame.sprite.Group()
dino = Dino()
every_sprite.add(dino)

for i in range(4):
    cloud = Clouds()
    every_sprite.add(cloud)

for i in range(width*2//64):
    floor = Floor(i)
    every_sprite.add(floor)

cactus = Cactus()
every_sprite.add(cactus)

flydino = FlyDino()
every_sprite.add(flydino)

obstacles_group = pygame.sprite.Group()
obstacles_group.add(cactus)
obstacles_group.add(flydino)

clock = pygame.time.Clock()
while True:
    clock.tick(30)
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and collision == False:
                if dino.rect.y != dino.pos_y:
                    pass
                else:
                    dino.pular()
                    
            if event.key == K_r and collision == True:
                restart_game()

    colisoes = pygame.sprite.spritecollide(dino, obstacles_group, False, pygame.sprite.collide_mask)

    every_sprite.draw(screen)

    if cactus.rect.topright[0] <= 0 or flydino.rect.topright[0] <= 0:
        choice_obstacle = choice([0, 1])
        cactus.rect.x = width
        flydino.rect.x = width
        cactus.choice = choice_obstacle
        flydino.choice = choice_obstacle


    if colisoes and collision == False:
        sound_collision.play()
        collision = True

    if collision == True:
        if points % 100 == 0:
            points += 1
        game_over = show_message('GAME OVER', 35, black)
        screen.blit(game_over, (width//2 , height//2))
        restart = show_message('Pressione R para reiniciar', 20, black)
        screen.blit(restart, (width//2 - 10, height//2 + 60))
    
    else:
        points += 0.5
        every_sprite.update()
        points_text = show_message(int(points), 30, black)

    if points % 100 == 0:
        sound_points.play()
        vel_game += 1
        
    screen.blit(points_text, (560, 20))
    
    pygame.display.flip()