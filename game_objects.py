import pygame
from pygame import mixer
import data_master
from random import choice
import game_menu


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_data):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [pygame.image.load(plane_data[5]),
                       pygame.image.load('data/booms/boom1.png'), pygame.image.load('data/booms/boom2.png'),
                       pygame.image.load('data/booms/boom3.png'), pygame.image.load('data/booms/boom4.png'),
                       pygame.image.load('data/booms/boom5.png'), pygame.image.load('data/booms/boom6.png')]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.speed = plane_data[3]
        self.bullets = pygame.sprite.Group()
        self.bombs = int(plane_data[13])
        self.hits = int(plane_data[8])
        self.down = False
        self.rect.x = 600
        self.rect.y = 300

    def move_up(self):
        if self.rect.y <= 0:
            self.rect.y = 0
        else:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.y >= 600 - self.rect.height:
            self.rect.y = 600 - self.rect.height
        else:
            self.rect.y += self.speed

    def move_left(self):
        if self.rect.x <= 0:
            self.rect.x = 0
        else:
            self.rect.x -= self.speed

    def move_right(self):
        if self.rect.x >= 1000 - self.rect.width:
            self.rect.x = 1000 - self.rect.width
        else:
            self.rect.x += self.speed

    def update(self, group):
        if self.down and self.cur_frame < len(self.frames) - 1:
            self.cur_frame += 1
            self.image = self.frames[self.cur_frame]
        elif self.down:
            group.remove(self)

    def shoot(self):
        bullet = Bullet(pygame.image.load('data/bullet.png'), self.rect.x, self.rect.y, self.speed)
        self.bullets.add(bullet)

    def drop_bomb(self, bombs):
        if self.bombs >= 1:
            bmb = Bomb(self.rect.x, self.rect.y, self.speed)
            bombs.add(bmb)
            self.bombs -= 1

    def hit(self, plane_data, player_data, score):
        self.hits -= 1
        if self.hits <= 0:
            self.down = True
            mixer.stop()
            data_master.change_score_money(player_data, int(int(plane_data[7]) * score))
            data_master.show_info(player_data)

    def add_bombs(self):
        self.bombs += 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit = False

    def update(self):
        self.rect.y -= self.speed * 2

    def hit(self):
        pass


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [pygame.image.load('data/arms/bomb.png'),
                       pygame.image.load('data/booms/boom1.png'), pygame.image.load('data/booms/boom2.png'),
                       pygame.image.load('data/booms/boom3.png'), pygame.image.load('data/booms/boom4.png'),
                       pygame.image.load('data/booms/boom5.png'), pygame.image.load('data/booms/boom6.png')]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.speed = speed * 0.5
        self.rect = self.image.get_rect()
        self.rect.x = x + 60
        self.rect.y = y + 70
        self.size_x = 20
        self.size_y = 36
        self.hit = False
        self.sound = mixer.Sound('data/music/bomb.wav')
        self.explosion = mixer.Sound('data/music/explosion.wav')
        self.explosion.set_volume(0.5)
        self.sound.set_volume(0.5)
        self.sound.play(1)

    def update(self, group):
        if not self.hit and self.size_x >= 12:
            self.rect.y += self.speed
            self.size_x *= 0.99
            self.size_y *= 0.99
            self.image = pygame.transform.smoothscale(self.image, (self.size_x, self.size_y))
        elif not self.hit:
            self.hit = True
            self.explosion.play()
        elif self.hit and self.cur_frame < len(self.frames) - 1:
            self.cur_frame += 1
            self.image = self.frames[self.cur_frame]
        else:
            group.remove(self)


class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, speed, base_pos):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [pygame.image.load('data/hangar.png'),
                       pygame.image.load('data/booms/boom1.png'), pygame.image.load('data/booms/boom2.png'),
                       pygame.image.load('data/booms/boom3.png'), pygame.image.load('data/booms/boom4.png'),
                       pygame.image.load('data/booms/boom5.png'), pygame.image.load('data/booms/boom6.png')]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = base_pos[0]
        self.rect.y = base_pos[1]
        self.speed = int(speed * 0.5)
        self.destroyed = False
        self.sound = mixer.Sound('data/music/explosion.wav')

    def update_animation(self, group):
        if self.cur_frame < len(self.frames) - 1 and self.destroyed:
            self.cur_frame += 1
            self.image = self.frames[self.cur_frame]
        elif self.destroyed:
            group.remove(self)
            self.sound.set_volume(0.5)
            self.sound.play()

    def move(self):
        self.rect.y += self.speed

    def check_collision(self, objects):
        if not pygame.sprite.spritecollideany(self, objects):
            return True
        return False

    def bombed(self, bmbs):
        if pygame.sprite.spritecollideany(self, bmbs):
            pygame.sprite.spritecollideany(self, bmbs).sound.stop()
            bmbs.remove(pygame.sprite.spritecollideany(self, bmbs))
            self.destroyed = True
            return True
        return False


class AARocket(pygame.sprite.Sprite):
    def __init__(self, spo_sound, x, height):
        pygame.sprite.Sprite.__init__(self)
        self.spo_sound = spo_sound
        self.frames = [pygame.image.load('data/arms/aa_rocket.png'),
                       pygame.image.load('data/booms/boom1.png'), pygame.image.load('data/booms/boom2.png'),
                       pygame.image.load('data/booms/boom3.png'), pygame.image.load('data/booms/boom4.png'),
                       pygame.image.load('data/booms/boom5.png'), pygame.image.load('data/booms/boom6.png')]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = height
        self.speed = 4
        self.destroyed = False

    def chase(self):
        if not self.destroyed:
            spo = mixer.Sound(self.spo_sound)
            spo.set_volume(0.4)
            spo.play()

    def aa_move(self):
        self.rect.y -= self.speed

    def check_collision(self, player):
        if pygame.sprite.spritecollideany(self, player) and not self.destroyed:
            self.destroyed = True
            explosion = mixer.Sound('data/music/explosion.wav')
            explosion.set_volume(0.5)
            explosion.play()
            return True
        return False

    def update_animation(self, group):
        if self.destroyed and self.cur_frame < len(self.frames) - 1:
            self.cur_frame = (self.cur_frame + 1)
            self.image = self.frames[self.cur_frame]
        elif self.destroyed:
            group.remove(self)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed, enemy_pos):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [pygame.image.load('data/booms/boom1.png'), pygame.image.load('data/booms/boom2.png'),
                       pygame.image.load('data/booms/boom3.png'), pygame.image.load('data/booms/boom4.png'),
                       pygame.image.load('data/booms/boom5.png'), pygame.image.load('data/booms/boom6.png')]
        self.frames.append(pygame.image.load(choice(['data/planes/mig-23-1.png', 'data/planes/mig-23-2.png'])))
        self.cur_frame = len(self.frames) - 1
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = enemy_pos[0]
        self.rect.y = enemy_pos[1]
        self.speed = int(speed * 0.5)
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
