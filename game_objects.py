import pygame
from pygame import mixer
from images import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_data):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(plane_data[5])
        self.rect = self.image.get_rect()
        self.speed = plane_data[3]
        self.bullets = pygame.sprite.Group()
        self.hits = 0
        self.rect.topleft = [600, 300]

    def move_up(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def move_down(self):
        if self.rect.top >= 600 - self.rect.height:
            self.rect.top = 600 - self.rect.height
        else:
            self.rect.top += self.speed

    def move_left(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def move_right(self):
        if self.rect.left >= 1000 - self.rect.width:
            self.rect.left = 1000 - self.rect.width
        else:
            self.rect.left += self.speed

    def change_down_stage(self):
        pass

    def shoot(self):
        bullet = Bullet(pygame.image.load('data/bullet.png'), self.rect.left, self.rect.top)
        self.bullets.add(bullet)

    def drop_bomb(self):
        pass

    def throw_flares(self):
        pass

    def death_from_collision(self):
        pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('data/bullet.png')
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.hit = False

    def update(self):
        self.rect.y -= self.speed * 2

    def hit(self):
        pass


class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, speed, base_pos):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.frames.append(load_image('hangar.png'))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = base_pos[0]
        self.rect.y = base_pos[1]
        self.speed = speed
        self.destroyed = False

    def update(self):
        if self.destroyed:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def move(self):
        if not self.destroyed:
            self.rect.y += self.speed

    def check_collision(self, objects):
        if not pygame.sprite.spritecollideany(self, objects):
            return True
        return False


class AARocket(pygame.sprite.Sprite):
    def __init__(self, spo_sound):
        pygame.sprite.Sprite.__init__(self)
        self.spo_sound = spo_sound

    def chase(self):
        mixer.music.load(self.spo_sound)
        mixer.music.set_volume(0.2)
        mixer.music.play(4)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed, enemy_pos):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.frames.append(pygame.image.load('data/planes/mig-15.png'))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = enemy_pos[0]
        self.rect.y = enemy_pos[1]
        self.speed = speed
        self.destroyed = False

    def update(self):
        if self.destroyed:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def move(self):
        if not self.destroyed:
            self.rect.y += self.speed

    def check_collision(self, objects):
        if not pygame.sprite.spritecollideany(self, objects):
            return True
        return False

    def check_collision_with_player(self, player):
        if pygame.sprite.spritecollideany(self, player):
            return True
        return False
