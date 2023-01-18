from images import load_image
import pygame
from pygame import mixer
import random


pygame.init()
size = width, height = 1400, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
background = pygame.image.load('data/backgrounds/game_background.png').convert()


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_data):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(plane_data[5])
        self.rect = self.image.get_rect()
        self.speed = plane_data[3]
        self.bullets = pygame.sprite.Group()
        self.hits = 0
        self.rect.topleft = [600, 300]

    def Up(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def Down(self):
        if self.rect.top >= 600 - self.rect.height:
            self.rect.top = 600 - self.rect.height
        else:
            self.rect.top += self.speed

    def Left(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def Right(self):
        if self.rect.left >= 1200 - self.rect.width:
            self.rect.left = 1200 - self.rect.width
        else:
            self.rect.left += self.speed


class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__(all_sprites)
        self.default_pic = load_image('data/hangar.png')
        self.frames = []
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.fall_speed = speed
        self.destroyed = False

    def update(self):
        if self.destroyed:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


def play(plane_data, player_data):
    print(plane_data)
    print(player_data)
    player = Player(plane_data)
    running = True
    screen.fill('white')
    fps = 60
    '''
    e_base = EnemyBase(player.speed)
    '''
    clock = pygame.time.Clock()
    while running:
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            player.Up()
        if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            player.Down()
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            player.Left()
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            player.Right()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(background, (0, 0))
        '''
        screen.blit(boom.image, (200, 300))
        boom.update()
        '''
        screen.blit(player.image, player.rect)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()