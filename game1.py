from game_objects import Player, EnemyBase, AARocket, Decorations
import pygame
import random


def play(plane_data, player_data):
    pygame.init()
    k_spawn = 0
    k_spawn_aa = 0
    k_spawn_decs = 0
    score = 0
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    background = random.choice(['data/backgrounds/jungles.png',
                                'data/backgrounds/forest.png',
                                'data/backgrounds/mountains.png'])
    background = pygame.image.load(background).convert()
    font = pygame.font.Font('freesansbold.ttf', 20)
    enemies = pygame.sprite.Group()
    players = pygame.sprite.Group()
    decorations = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    player = Player(plane_data)
    players.add(player)
    running = True
    screen.fill('white')
    fps = 60
    enemy_aa = pygame.sprite.Group()
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    player.drop_bomb(bombs)
            if event.type == pygame.QUIT:
                running = False
        base_pos = [random.randint(0, width - 150), 0]
        enemy_base = EnemyBase(plane_data[3], base_pos)
        if enemy_base.check_collision(enemies) and k_spawn == 50 and enemy_base.check_collision(decorations):
            enemies.add(enemy_base)
        dec_pos = [random.randint(0, width - 150), 0]
        decor = Decorations(plane_data[3], *dec_pos)
        if decor.check_collision(decorations) and k_spawn_decs == 30 and decor.check_collision(enemies):
            decorations.add(decor)
        if k_spawn_aa == 150:
            aa = AARocket(plane_data[12], player.rect.x + 25, height)
            enemy_aa.add(aa)
            aa.chase()
        for rocket in enemy_aa:
            rocket.aa_move()
            rocket.update_animation(enemy_aa)
            if rocket.check_collision(players):
                player.hit()
        for dec in decorations:
            dec.move()
            dec.update(bombs)
        for enemy in enemies:
            enemy.move()
            if enemy.bombed(bombs):
                score += 1
                player.add_bombs()
            enemy.update_animation(enemies)
        for bmb in bombs:
            bmb.update(bombs)
        for gamer in players:
            gamer.update(players)
            gamer.check_animation_status(plane_data, player_data, score, players)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        bomb_text = font.render(f'Bombs: {player.bombs}', True, (255, 255, 255))
        health_text = font.render(f'Health: {player.hits}', True, (255, 255, 255))
        score_rect = score_text.get_rect()
        bomb_rect = bomb_text.get_rect()
        health_rect = health_text.get_rect()
        health_rect.center = (900, 110)
        bomb_rect.center = (900, 80)
        score_rect.center = (900, 50)
        screen.blit(background, (0, 0))
        decorations.draw(screen)
        enemies.draw(screen)
        enemy_aa.draw(screen)
        bombs.draw(screen)
        players.draw(screen)
        screen.blit(score_text, score_rect)
        screen.blit(bomb_text, bomb_rect)
        screen.blit(health_text, health_rect)
        clock.tick(fps)
        k_spawn_aa = (k_spawn_aa + 1) % 151
        k_spawn = (k_spawn + 1) % 51
        k_spawn_decs = (k_spawn_decs + 1) % 31
        pygame.display.flip()
    pygame.quit()
