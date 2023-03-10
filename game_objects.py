import pygame
from pygame import mixer
import data_master
from random import choice
import threading


class BasicSprite(pygame.sprite.Sprite):   # базовый спрайт с базовым функционалом
    def __init__(self, frames, speed):
        pygame.sprite.Sprite.__init__(self)
        self.frames = frames
        self.cur_frame = 0
        self.image = frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.speed = speed
        self.destroyed = False

    def update_animation(self, group):
        if self.cur_frame < len(self.frames) - 1 and self.destroyed:
            self.cur_frame += 1
            self.image = self.frames[self.cur_frame]
        elif self.destroyed:
            group.remove(self)
            self.sound.set_volume(0.5)
            self.sound.play()

    def move(self, vector=1):
        self.rect.y += self.speed * vector

    def check_collision(self, objects):
        if not pygame.sprite.spritecollideany(self, objects):
            return True
        return False


class Player(BasicSprite):   # спрайт игрока: большинство названий говорящие, как и во всех других српайтах
    def __init__(self, plane_data):
        BasicSprite.__init__(self, [pygame.image.load(plane_data[5]),
                                    pygame.image.load('data/booms/boom1.png'),
                                    pygame.image.load('data/booms/boom2.png'),
                                    pygame.image.load('data/booms/boom3.png'),
                                    pygame.image.load('data/booms/boom4.png'),
                                    pygame.image.load('data/booms/boom5.png'),
                                    pygame.image.load('data/booms/boom6.png')],
                             plane_data[3])
        self.bullets = plane_data[14]
        self.bombs = int(plane_data[13])
        self.hits = int(plane_data[8])
        self.explosion = mixer.Sound('data/music/explosion.wav')
        self.explosion.set_volume(0.5)
        self.down = False
        self.exploding = False
        self.rect.x = 600
        self.rect.y = 300

    def move_up(self):
        if self.rect.y <= 0:
            self.rect.y = 0
        else:
            self.rect.y -= self.speed

    def move_down(self, height):
        if self.rect.y >= height - self.rect.height:
            self.rect.y = height - self.rect.height
        else:
            self.rect.y += self.speed

    def move_left(self):
        if self.rect.x <= 0:
            self.rect.x = 0
        else:
            self.rect.x -= self.speed

    def move_right(self, width):
        if self.rect.x >= width - self.rect.width:
            self.rect.x = width - self.rect.width
        else:
            self.rect.x += self.speed

    def update(self, group, player_data, plane_data, score):
        if self.down and self.cur_frame < len(self.frames) - 1 and self.exploding:
            self.cur_frame += 1
            self.image = self.frames[self.cur_frame]
        elif self.down:
            self.exploding = False
            group.remove(self)
        if self.down and not self.exploding:
            group.remove(self)
            mixer.stop()
            add_points = threading.Thread(target=data_master.change_score_money(player_data, int(int(plane_data[7])
                                                                                                 * score)))
            add_points.start()
            data_master.show_info(data_master.check_player(player_data[0], player_data[1]))

    def shoot(self, group):
        if self.bullets > 0:
            bullet = Bullet(pygame.image.load('data/arms/bullet.png'), self.speed, self.rect.midtop)
            group.add(bullet)
            self.bullets -= 1

    def drop_bomb(self, bombs):
        if self.bombs >= 1:
            bmb = Bomb(self.rect.midbottom, self.speed)
            bombs.add(bmb)
            self.bombs -= 1

    def hit(self):
        self.hits -= 1
        if self.hits <= 0:
            self.hits = 0
            self.down = True
            self.exploding = True
            self.explosion.play()
            mixer.stop()

    def add_bombs(self):
        self.bombs += 1

    def check_collision(self, objects):
        colided = pygame.sprite.spritecollideany(self, objects)
        if colided and not colided.destroyed:
            colided.kill()
            self.hit()

    def shot(self, bullets):
        colided = pygame.sprite.spritecollideany(self, bullets)
        if colided:
            bullets.remove(colided)
            self.hit()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, speed, px):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = int(px[0]) - 10
        self.rect.y = int(px[1])
        self.hit = False
        self.sound = mixer.Sound('data/music/bullet.wav')
        self.sound.set_volume(0.3)
        self.sound.play()

    def update(self, vector=1):
        self.rect.y -= self.speed * 2 * vector


class Bomb(BasicSprite):
    def __init__(self, mid_bottom, speed):
        BasicSprite.__init__(self, [pygame.image.load('data/arms/bomb.png'),
                                    pygame.image.load('data/booms/boom1.png'),
                                    pygame.image.load('data/booms/boom2.png'),
                                    pygame.image.load('data/booms/boom3.png'),
                                    pygame.image.load('data/booms/boom4.png'),
                                    pygame.image.load('data/booms/boom5.png'),
                                    pygame.image.load('data/booms/boom6.png')],
                             speed * 0.5)
        self.rect.x = mid_bottom[0] - 10
        self.rect.y = mid_bottom[1] - 60
        self.size_x = 20
        self.size_y = 36
        self.hit = False
        self.sound = mixer.Sound('data/music/bomb.wav')
        self.explosion = mixer.Sound('data/music/explosion.wav')
        self.explosion.set_volume(0.5)
        self.sound.set_volume(0.5)
        self.sound.play(1)

    def update(self, group):
        if not self.hit and self.size_x >= 10:
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


class EnemyBase(BasicSprite):
    def __init__(self, speed, base_pos):
        BasicSprite.__init__(self, [pygame.image.load('data/backgrounds/hangar_dec.png'),
                                    pygame.image.load('data/booms/boom1.png'),
                                    pygame.image.load('data/booms/boom2.png'),
                                    pygame.image.load('data/booms/boom3.png'),
                                    pygame.image.load('data/booms/boom4.png'),
                                    pygame.image.load('data/booms/boom5.png'),
                                    pygame.image.load('data/booms/boom6.png')],
                             speed * 0.5)
        self.rect.x = base_pos[0]
        self.rect.y = base_pos[1]
        self.sound = mixer.Sound('data/music/explosion.wav')

    def bombed(self, bmbs):
        colided = pygame.sprite.spritecollideany(self, bmbs)
        if colided:
            if colided.size_x <= 10:
                colided.sound.stop()
                bmbs.remove(colided)
                self.destroyed = True
                return True
        return False


class AARocket(BasicSprite):
    def __init__(self, spo_sound, x, height):
        BasicSprite.__init__(self, [pygame.image.load('data/arms/aa_rocket.png'),
                                    pygame.image.load('data/booms/boom1.png'),
                                    pygame.image.load('data/booms/boom2.png'),
                                    pygame.image.load('data/booms/boom3.png'),
                                    pygame.image.load('data/booms/boom4.png'),
                                    pygame.image.load('data/booms/boom5.png'),
                                    pygame.image.load('data/booms/boom6.png')], 10)
        self.spo_sound = spo_sound
        self.rect.x = x
        self.rect.y = height
        self.sound = mixer.Sound('data/music/explosion.wav')
        self.sound.set_volume(0.5)

    def chase(self):
        if not self.destroyed:
            spo = mixer.Sound(self.spo_sound)
            spo.set_volume(0.4)
            spo.play()
            start = mixer.Sound('data/music/missile.wav')
            start.set_volume(0.4)
            start.play()

    def exploded(self):
        self.destroyed = True


class Enemy(BasicSprite):
    def __init__(self, enemy_pos):
        BasicSprite.__init__(self, [pygame.image.load('data/planes/mig-23-1.png'),
                                    pygame.image.load('data/booms/boom1.png'),
                                    pygame.image.load('data/booms/boom2.png'),
                                    pygame.image.load('data/booms/boom3.png'),
                                    pygame.image.load('data/booms/boom4.png'),
                                    pygame.image.load('data/booms/boom5.png'),
                                    pygame.image.load('data/booms/boom6.png')], 2)
        self.rect.x = enemy_pos[0]
        self.rect.y = enemy_pos[1]
        self.sound = mixer.Sound('data/music/explosion.wav')

    def shot(self, bullets):
        colided = pygame.sprite.spritecollideany(self, bullets)
        if colided:
            bullets.remove(colided)
            self.destroyed = True
            return True
        return False

    def shoot(self, group):
        bullet = Bullet(pygame.image.load('data/arms/bullet.png'), self.speed, self.rect.midbottom)
        group.add(bullet)

    def kill(self):
        self.destroyed = True


class Decorations(BasicSprite):
    def __init__(self, speed, x, y):
        building = choice(['building1', 'building2', 'building3', 'building4', 'building5', 'building6',
                           'building7'])
        BasicSprite.__init__(self, [pygame.image.load(f'data/backgrounds/{building}/image1.png'),
                                    pygame.image.load(f'data/backgrounds/{building}/image4.png')], speed * 0.5)
        self.rect.x = x
        self.rect.y = y

    def update(self, bmbs):
        colided = pygame.sprite.spritecollideany(self, bmbs)
        if colided:
            if colided.size_x <= 10:
                colided.sound.stop()
                if self.cur_frame < len(self.frames) - 1:
                    self.cur_frame += 1
                return True
            return False
        self.image = self.frames[self.cur_frame]
