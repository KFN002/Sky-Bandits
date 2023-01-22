from game_objects import Player, Enemy
from images import load_image
import pygame
from pygame import mixer
import random


def play(plane_data, player_data):
    k_spawn = 0
    running = True
    play_death_animation = False
    score = 0
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    font = pygame.font.Font('freesansbold.ttf', 20)
    background = random.choice(['data/backgrounds/jungles.png',
                                'data/backgrounds/forest.png',
                                'data/backgrounds/mountains.png'])
    background = pygame.image.load(background).convert()
    enemies = pygame.sprite.Group()
    players = pygame.sprite.Group()
    enemies_killed = pygame.sprite.Group()
    player = Player(plane_data)
    players.add(player)
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
        if pygame.mouse.get_pressed()[0]:
            player.shoot()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        enemy_pos = [random.randint(0, width - 150), 0]
        enemy_base = Enemy(plane_data[3], enemy_pos)
        if enemy_base.check_collision(enemies) and k_spawn == 50:
            enemies.add(enemy_base)
        for enemy in enemies:
            enemy.move()
            if enemy.check_collision_with_player(players):
                player.death(player_data, score)
                play_death_animation = True
                print('collision')
        if play_death_animation:
            player.update()
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.center = (900, 50)
        screen.blit(background, (0, 0))
        enemies.draw(screen)
        players.draw(screen)
        screen.blit(score_text, score_rect)
        clock.tick(fps)
        k_spawn = (k_spawn + 1) % 51
        pygame.display.flip()
    pygame.quit()
