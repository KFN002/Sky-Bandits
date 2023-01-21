from game_objects import Player, Enemy
from images import load_image
import pygame
from pygame import mixer
import random

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
background = random.choice(['data/backgrounds/jungles.png',
                            'data/backgrounds/forest.png',
                            'data/backgrounds/mountains.png'])
background = pygame.image.load(background).convert()
enemies = pygame.sprite.Group()
enemies_killed = pygame.sprite.Group()


def play(plane_data, player_data):
    print(plane_data)
    print(player_data)
    player = Player(plane_data)
    running = True
    screen.fill('white')
    fps = 60
    clock = pygame.time.Clock()
    while running:
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            player.move_up()
        if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            player.move_down()
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            player.move_left()
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            player.move_right()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        enemy_pos = [random.randint(0, width - 150), 0]
        enemy_base = Enemy(plane_data[3], enemy_pos)
        if enemy_base.check_collision(enemies):
            enemies.add(enemy_base)
        for enemy in enemies:
            enemy.move()
            if enemy.check_collision_with_player(player):
                player.death_from_collision()
                exit()
        screen.blit(background, (0, 0))
        enemies.draw(screen)
        screen.blit(player.image, player.rect)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
