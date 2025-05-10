import ctypes
import os
import time

import pygame.transform
from behavior_strategy import AttackerStrategy, ChaserStrategy, PatrolStrategy
from bullets import (ConcretePunchingBullet, DefaultBullet, IncendiaryBullet,
                     PlayerBullet)
from cyclicIterator import CyclicIterator
from let import Brick, Ice, Plant, Rock, Water
from loading_screen import transition_screen
from pause import pause
from states import States
from tank import ArmorTank, FastTank, PlayerTank, RapidFireTank, WeakTank

from game.load_data import load_data
from game.save import save


def start_level(map: list, level_num: str) -> States:
    """
    Запускает уровень
    :param map: карта уровня
    :param level_num: номер уровня
    :return: статус игры
    """
    SPAWN_X = None
    SPAWN_Y = None
    let_size = 40
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    pygame.init()
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    pygame.display.set_caption("Battle City")
    running = True
    transition_screen(screen)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shoot_music_path = os.path.join(base_dir, "sounds", "shoot.mp3")
    shoot_sound = pygame.mixer.Sound(shoot_music_path)
    armor_music_path = os.path.join(base_dir, "sounds", "armor.wav")
    armor_sound = pygame.mixer.Sound(armor_music_path)
    health_music_path = os.path.join(base_dir, "sounds", "health.wav")
    health_sound = pygame.mixer.Sound(health_music_path)
    speed_music_path = os.path.join(base_dir, "sounds", "speed.wav")
    speed_sound = pygame.mixer.Sound(speed_music_path)
    win_music_path = os.path.join(base_dir, "sounds", "win.wav")
    win_sound = pygame.mixer.Sound(win_music_path)
    lost_music_path = os.path.join(base_dir, "sounds", "lost.wav")
    lost_sound = pygame.mixer.Sound(lost_music_path)
    play_sound = False

    load_armor_image = pygame.image.load("../game_images/armor.png")
    armor_image = pygame.transform.scale(load_armor_image, (50, 50))
    armor_rect = None

    load_game_over = pygame.image.load("../game_images/game_over.jpg")
    game_over = pygame.transform.scale(load_game_over, (1920, 1080))
    game_rect = game_over.get_rect(topleft=(0, 0))

    load_replay_button = pygame.image.load("../game_images/replay_button.png")
    replay_button = pygame.transform.scale(load_replay_button, (280, 70))
    replay_button_rect = replay_button.get_rect(center=(width // 2, (height * 3.5) // 5))

    load_winner = pygame.image.load("../game_images/winner.jpg")
    winner = pygame.transform.scale(load_winner, (1920, 1080))
    winner_rect = winner.get_rect(topleft=(0, 0))

    load_health_image = pygame.image.load("../game_images/health.png")
    health_image = pygame.transform.scale(load_health_image, (50, 50))
    health_rect = None

    load_speed_image = pygame.image.load("../game_images/speed.png")
    speed_image = pygame.transform.scale(load_speed_image, (60, 40))
    speed_rect = None

    load_flame_image = pygame.image.load("../game_images/flame.png")
    flame_image = pygame.transform.scale(load_flame_image, (100, 100))

    load_base_image = pygame.image.load("../game_images/base.jfif")
    base_image = pygame.transform.scale(load_base_image, (100, 100))
    base_pos = None

    load_player_tank_image = pygame.image.load("../game_images/player_tank.png")
    player_tank_image = pygame.transform.scale(load_player_tank_image, (75, 75))

    load_back_image = pygame.image.load("../game_images/back.png")
    back_image_in_game = pygame.transform.scale(load_back_image, (100, 100))
    back_pos = back_image_in_game.get_rect(topleft=(0, -25))

    back_image_lost = pygame.transform.scale(load_back_image, (250, 250))
    back_image_lost_rect = back_image_lost.get_rect(center=(width // 2, (height * 4) // 5))

    load_pause_image = pygame.image.load("../game_images/pause.png")
    pause_image = pygame.transform.scale(load_pause_image, (50, 50))
    pause_rect = pause_image.get_rect(topleft=(100, 0))

    load_next_image = pygame.image.load("../game_images/next_button.png")
    next_image = pygame.transform.scale(load_next_image, (250, 125))
    next_rect = next_image.get_rect(center=(width // 2, (height * 3) // 5))

    player_tank = PlayerTank(
        width // 2,
        height // 2,
        PlayerBullet(width // 2, height // 2, 0),
        0,
        None,
    )

    base_health = 8

    lets = []
    patrol1 = []
    patrol2 = []
    patrol3 = []
    patrol4 = []
    tuple_base_pos = None
    attackers_pos = []
    chaser_pos = []
    bullets = []
    start_time = 0
    update_chaser = False
    flames = []
    speed_pos = None
    health_pos = None
    armor_pos = None
    bonus_pos = None

    if map is not None:
        map = [row[:] for row in map]
        for y in range(height // let_size):
            for x in range(width // let_size):
                if map[y][x] == "b" and (x == 0 or y == 0 or x == width // let_size - 1 or y == height // let_size - 1):
                    lets.append(Brick(999, x * let_size, y * let_size))
                elif map[y][x] == "b" or map[y][x] == "s":
                    lets.append(Brick(3, x * let_size, y * let_size))
                elif map[y][x] == "i":
                    lets.append(Ice(2, x * let_size, y * let_size))
                elif map[y][x] == "r":
                    lets.append(Rock(5, x * let_size, y * let_size))
                elif map[y][x] == "p":
                    lets.append(Plant(1, x * let_size, y * let_size))
                elif map[y][x] == "w":
                    lets.append(Water(999, x * let_size, y * let_size))
                elif map[y][x] == "d":
                    tuple_base_pos = (x, y)
                    base_pos = base_image.get_rect(
                        center=(
                            x * let_size + let_size // 2,
                            y * let_size + let_size // 2,
                        )
                    )
                elif map[y][x] == "u":
                    SPAWN_X = x * let_size + let_size // 2
                    SPAWN_Y = y * let_size + let_size // 2
                    player_tank.set_x(x * let_size + let_size // 2)
                    player_tank.set_y(y * let_size + let_size // 2)
                elif map[y][x] == "!":
                    patrol1.append((x * let_size, y * let_size))
                elif map[y][x] == "@":
                    patrol2.append((x * let_size, y * let_size))
                elif map[y][x] == "#":
                    patrol3.append((x * let_size, y * let_size))
                elif map[y][x] == "$":
                    patrol4.append((x * let_size, y * let_size))
                elif map[y][x] == "2":
                    attackers_pos.append((x * let_size, y * let_size))
                elif map[y][x] == "3":
                    chaser_pos.append((x * let_size, y * let_size))
                elif map[y][x] == "v":
                    speed_pos = (x * let_size, y * let_size)
                    speed_rect = speed_image.get_rect(center=(x * let_size, y * let_size))
                elif map[y][x] == "a":
                    armor_pos = (x * let_size, y * let_size)
                    armor_rect = armor_image.get_rect(center=(x * let_size, y * let_size))
                elif map[y][x] == "h":
                    health_pos = (x * let_size, y * let_size)
                    health_rect = health_image.get_rect(center=(x * let_size, y * let_size))

        bonus_pos = {"speed": speed_pos, "armor": armor_pos, "health": health_pos}

        bonus = [
            (speed_image, speed_rect, "speed"),
            (armor_image, armor_rect, "armor"),
            (health_image, health_rect, "health"),
        ]

        patrol_tanks = []

        patrol_tank1 = FastTank(
            patrol1[0][0],
            patrol1[0][1],
            DefaultBullet(patrol1[0][0], patrol1[0][1], 0),
            0,
            PatrolStrategy(patrol1[0][0], patrol1[0][1], patrol1[1][0], patrol1[1][1]),
        )
        iterator1 = CyclicIterator(patrol1)
        patrol_tanks.append((patrol_tank1, iterator1))

        patrol_tank2 = ArmorTank(
            patrol2[0][0],
            patrol2[0][1],
            DefaultBullet(patrol2[0][0], patrol2[0][1], 0),
            0,
            PatrolStrategy(patrol2[0][0], patrol2[0][1], patrol2[1][0], patrol2[1][1]),
        )
        iterator2 = CyclicIterator(patrol2)
        patrol_tanks.append((patrol_tank2, iterator2))

        patrol_tank3 = WeakTank(
            patrol3[0][0],
            patrol3[0][1],
            DefaultBullet(patrol3[0][0], patrol3[0][1], 0),
            0,
            PatrolStrategy(patrol3[0][0], patrol3[0][1], patrol3[1][0], patrol3[1][1]),
        )
        iterator3 = CyclicIterator(patrol3)
        patrol_tanks.append((patrol_tank3, iterator3))

        patrol_tank4 = RapidFireTank(
            patrol4[0][0],
            patrol4[0][1],
            DefaultBullet(patrol4[0][0], patrol4[0][1], 0),
            0,
            PatrolStrategy(patrol4[0][0], patrol4[0][1], patrol4[1][0], patrol4[1][1]),
        )
        iterator4 = CyclicIterator(patrol4)
        patrol_tanks.append((patrol_tank4, iterator4))

        attackers = []
        for pos in attackers_pos:
            tank = ArmorTank(
                pos[0],
                pos[1],
                ConcretePunchingBullet(pos[0], pos[1], 0),
                0,
                AttackerStrategy(pos[0], pos[1], base_pos.x, base_pos.y),
            )
            attackers.append(tank)
            tank.get_strategy().find_path(map, (pos[0] // 40, pos[1] // 40), tuple_base_pos)

        chasers = []

        for pos in chaser_pos:
            tank = WeakTank(
                pos[0],
                pos[1],
                IncendiaryBullet(pos[0], pos[1], 0),
                0,
                ChaserStrategy(pos[0], pos[1], map),
            )
            chasers.append(tank)
    else:
        data = load_data()
        lets = data["lets"]
        for let in lets:
            let.__post_init__()
        player_tank = data["player_tank"]
        patrol_tanks = data["patrol_tanks"]
        attackers = data["attackers"]
        chasers = data["chasers"]
        for tank in attackers + chasers:
            tank.get_strategy().load_image()
        for tank in patrol_tanks:
            tank[0].get_strategy().load_image()
        bonus_pos = data["bonus"]
        bonus = []
        if "speed" in bonus_pos:
            speed_rect = speed_image.get_rect(center=(bonus_pos["speed"][0], bonus_pos["speed"][1]))
            bonus.append((speed_image, speed_rect, "speed"))
        if "armor" in bonus_pos:
            armor_rect = armor_image.get_rect(center=(bonus_pos["armor"][0], bonus_pos["armor"][1]))
            bonus.append((armor_image, armor_rect, "armor"))
        if "health" in bonus_pos:
            health_rect = health_image.get_rect(center=(bonus_pos["health"][0], bonus_pos["health"][1]))
            bonus.append((health_image, health_rect, "health"))
        level_num = data["level_num"]
        base_tuple_pos = data["base_pos"]
        base_pos = base_image.get_rect(
            center=(
                base_tuple_pos[0] * let_size + let_size // 2,
                base_tuple_pos[1] * let_size + let_size // 2,
            )
        )
        base_health = data["base_health"]
        map = data["map"]
        SPAWN_X = data["SPAWN_X"]
        SPAWN_Y = data["SPAWN_Y"]

    while running:
        screen.fill("black")
        cooldown = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()

        if len(attackers + chasers + patrol_tanks) == 0:
            if not play_sound:
                win_sound.play()
                play_sound = True
            screen.blit(winner, winner_rect)
            screen.blit(replay_button, replay_button_rect)
            screen.blit(back_image_lost, back_image_lost_rect)
            screen.blit(next_image, next_rect)
            if replay_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return States("play" + level_num)
            if back_image_lost_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return States.MENU
            if next_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return States("next" + level_num)
            pygame.display.flip()
            continue

        if base_health <= 0:
            if not play_sound:
                lost_sound.play()
                play_sound = True
            screen.blit(game_over, game_rect)
            screen.blit(replay_button, replay_button_rect)
            screen.blit(back_image_lost, back_image_lost_rect)
            if replay_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return States("play" + level_num)
            if back_image_lost_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return States.MENU
            pygame.display.flip()
            continue
        else:
            screen.blit(base_image, base_pos)

        if back_pos.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return States.MENU
        keys = pygame.key.get_pressed()

        original_player_tank_pos = (player_tank.get_x(), player_tank.get_y())
        if keys[pygame.K_w]:
            player_tank.set_y(player_tank.get_y() - player_tank.get_speed())
            player_tank.set_direction(0)
        elif keys[pygame.K_s]:
            player_tank.set_y(player_tank.get_y() + player_tank.get_speed())
            player_tank.set_direction(180)
        elif keys[pygame.K_a]:
            player_tank.set_x(player_tank.get_x() - player_tank.get_speed())
            player_tank.set_direction(90)
        elif keys[pygame.K_d]:
            player_tank.set_x(player_tank.get_x() + player_tank.get_speed())
            player_tank.set_direction(-90)
        if keys[pygame.K_SPACE] and cooldown - player_tank.get_attack_speed() >= 0:
            start_time = time.time()
            bullet = player_tank.get_bullet()
            bullet.__init__(
                original_player_tank_pos[0],
                original_player_tank_pos[1],
                player_tank.get_direction(),
            )
            bullets.append((bullet, 1))
            shoot_sound.play()

        rotated_tank = pygame.transform.rotate(player_tank_image, player_tank.get_direction())
        new_rect = rotated_tank.get_rect(center=(int(player_tank.get_x()), int(player_tank.get_y())))

        for tank in attackers:
            for let in lets:
                let_rect = let.get_transform_image().get_rect(topleft=(let.get_x(), let.get_y()))
                if let.get_strength() <= 0:
                    lets.remove(let)
                    update_chaser = True
                    map[let.get_y() // 40] = (
                        map[let.get_y() // 40][: (let.get_x() // 40)]
                        + " "
                        + map[let.get_y() // 40][((let.get_x() // 40) + 1):]
                    )
                    continue
                screen.blit(let.get_transform_image(), let_rect)
                if new_rect.colliderect(let_rect):
                    player_tank.set_x(original_player_tank_pos[0])
                    player_tank.set_y(original_player_tank_pos[1])
                if (
                    tank.get_strategy()
                    .get_transform_image()
                    .get_rect(center=(int(tank.get_strategy().get_x()), int(tank.get_strategy().get_y())))
                    .colliderect(let_rect)
                ):
                    tank.get_strategy().set_x(tank.get_strategy().get_old_x())
                    tank.get_strategy().set_y(tank.get_strategy().get_old_y())
                if (
                    tank.get_strategy()
                    .get_transform_image()
                    .get_rect(center=(int(tank.get_strategy().get_x()), int(tank.get_strategy().get_y())))
                    .colliderect(base_pos)
                ):
                    tank.get_strategy().set_x(tank.get_strategy().get_old_x())
                    tank.get_strategy().set_y(tank.get_strategy().get_old_y())

        if len(attackers) == 0:
            for let in lets:
                let_rect = let.get_transform_image().get_rect(topleft=(let.get_x(), let.get_y()))
                if let.get_strength() <= 0:
                    lets.remove(let)
                    update_chaser = True
                    map[let.get_y() // 40] = (
                        map[let.get_y() // 40][: (let.get_x() // 40)]
                        + " "
                        + map[let.get_y() // 40][((let.get_x() // 40) + 1):]
                    )
                    continue
                screen.blit(let.get_transform_image(), let_rect)
                if new_rect.colliderect(let_rect):
                    player_tank.set_x(original_player_tank_pos[0])
                    player_tank.set_y(original_player_tank_pos[1])

        for tank in patrol_tanks:
            res = (
                tank[0]
                .get_strategy()
                .update(screen, tank[0].get_speed(), tank[0].get_health_point(), tank[0].get_armor())
            )
            if time.time() - tank[0].get_last_shot() >= tank[0].get_attack_speed():
                bullets.append(
                    (
                        DefaultBullet(
                            tank[0].get_strategy().get_x(),
                            tank[0].get_strategy().get_y(),
                            tank[0].get_strategy().get_angle(),
                        ),
                        2,
                    )
                )
                tank[0].update_last_shot(time.time())

            if res == -1:
                new_pos = next(tank[1])
                tank[0].get_strategy().set_new_point(new_pos[0], new_pos[1])

        for tank in attackers:
            tank.get_strategy().update(screen, tank.get_speed(), tank.get_health_point(), tank.get_armor())
            if time.time() - tank.get_last_shot() >= tank.get_attack_speed():
                bullets.append(
                    (
                        ConcretePunchingBullet(
                            tank.get_strategy().get_x(),
                            tank.get_strategy().get_y(),
                            tank.get_strategy().get_angle(),
                        ),
                        2,
                    )
                )
                tank.update_last_shot(time.time())

        for tank in chasers:
            if update_chaser:
                tank.get_strategy().create_grid(map)
                tank.get_strategy().set_updatable(True)
            tank.get_strategy().update(
                screen,
                tank.get_speed(),
                tank.get_health_point(),
                tank.get_armor(),
                player_tank.get_x(),
                player_tank.get_y(),
            )
            if time.time() - tank.get_last_shot() >= tank.get_attack_speed():
                bullets.append(
                    (
                        IncendiaryBullet(
                            tank.get_strategy().get_x(),
                            tank.get_strategy().get_y(),
                            tank.get_strategy().get_angle(),
                        ),
                        2,
                    )
                )
                tank.update_last_shot(time.time())
        update_chaser = False

        new_rect = rotated_tank.get_rect(center=(int(player_tank.get_x()), int(player_tank.get_y())))
        screen.blit(rotated_tank, new_rect)
        pygame.draw.rect(
            screen,
            "red",
            (
                player_tank.get_x() - 35,
                player_tank.get_y() - 55,
                player_tank.get_health_point(),
                10,
            ),
        )
        pygame.draw.rect(
            screen,
            "white",
            (player_tank.get_x() - 35, player_tank.get_y() - 70, player_tank.get_armor(), 10),
        )

        if (armor_image, armor_rect, "armor") in bonus:
            if new_rect.colliderect(armor_rect):
                player_tank.set_armor(80)
                armor_sound.play()
                bonus.remove((armor_image, armor_rect, "armor"))

        if (speed_image, speed_rect, "speed") in bonus:
            if new_rect.colliderect(speed_rect):
                player_tank.set_speed(3)
                speed_sound.play()
                bonus.remove((speed_image, speed_rect, "speed"))

        if (health_image, health_rect, "health") in bonus:
            if new_rect.colliderect(health_rect):
                player_tank.set_health_point(100)
                health_sound.play()
                bonus.remove((health_image, health_rect, "health"))

        for bon in bonus:
            screen.blit(bon[0], bon[1])
        for flame in flames:
            if time.time() - flame[1] <= 2:
                screen.blit(flame_image, flame[0])
                if flame[0].colliderect(new_rect):
                    if player_tank.get_armor() > 0:
                        player_tank.set_armor(player_tank.get_armor() - 0.3)
                    else:
                        player_tank.set_health_point(player_tank.get_health_point() - 0.3)
                    if player_tank.get_health_point() <= 0:
                        player_tank.set_health_point(80)
                        player_tank.set_x(SPAWN_X)
                        player_tank.set_y(SPAWN_Y)

            else:
                flames.remove(flame)

        for bullet in bullets:
            bullet_rect = bullet[0].update(screen)
            if bullet[1] == 2:
                if bullet_rect.colliderect(base_pos):
                    base_health -= 1
                    bullets.remove(bullet)
                    continue
                if bullet_rect.colliderect(new_rect):
                    if bullet[0].get_fire():
                        flame_x = bullet_rect.x
                        flame_y = bullet_rect.y
                        flames.append(
                            (
                                flame_image.get_rect(center=(flame_x, flame_y)),
                                time.time(),
                            )
                        )
                    if player_tank.get_armor() > 0:
                        player_tank.set_armor(player_tank.get_armor() - bullet[0].get_damage())
                    else:
                        player_tank.set_health_point(player_tank.get_health_point() - bullet[0].get_damage())
                    bullets.remove(bullet)
                    if player_tank.get_health_point() <= 0:
                        player_tank.set_health_point(80)
                        player_tank.set_x(SPAWN_X)
                        player_tank.set_y(SPAWN_Y)

            if bullet[1] == 1:
                for tank in patrol_tanks:
                    if bullet_rect.colliderect(
                        tank[0]
                        .get_strategy()
                        .get_transform_image()
                        .get_rect(center=(tank[0].get_strategy().get_x(), tank[0].get_strategy().get_y()))
                    ):
                        if tank[0].get_armor() > 0:
                            tank[0].set_armor(tank[0].get_armor() - bullet[0].get_damage())
                            bullets.remove(bullet)
                        else:
                            tank[0].set_health_point(tank[0].get_health_point() - bullet[0].get_damage())
                            bullets.remove(bullet)
                        if tank[0].get_armor() <= 0 and tank[0].get_health_point() <= 0:
                            patrol_tanks.remove(tank)

                for tank in chasers:
                    if bullet in bullets:
                        if bullet_rect.colliderect(
                            tank.get_strategy()
                            .get_transform_image()
                            .get_rect(center=(tank.get_strategy().get_x(), tank.get_strategy().get_y()))
                        ):
                            if tank.get_armor() > 0:
                                tank.set_armor(tank.get_armor() - bullet[0].get_damage())
                                bullets.remove(bullet)
                            else:
                                tank.set_health_point(tank.get_health_point() - bullet[0].get_damage())
                                bullets.remove(bullet)
                            if tank.get_armor() <= 0 and tank.get_health_point() <= 0:
                                chasers.remove(tank)

                for tank in attackers:
                    if bullet in bullets:
                        if bullet_rect.colliderect(
                            tank.get_strategy()
                            .get_transform_image()
                            .get_rect(center=(tank.get_strategy().get_x(), tank.get_strategy().get_y()))
                        ):
                            if tank.get_armor() > 0:
                                tank.set_armor(tank.get_armor() - bullet[0].get_damage())
                                bullets.remove(bullet)
                            else:
                                tank.set_health_point(tank.get_health_point() - bullet[0].get_damage())
                                bullets.remove(bullet)
                            if tank.get_armor() <= 0 and tank.get_health_point() <= 0:
                                attackers.remove(tank)
            for let in lets:
                let_rect = let.get_transform_image().get_rect(topleft=(let.get_x(), let.get_y()))
                if bullet_rect.colliderect(let_rect):
                    if bullet[0].get_fire():
                        flame_x = bullet_rect.x
                        flame_y = bullet_rect.y
                        flames.append(
                            (
                                flame_image.get_rect(center=(flame_x, flame_y)),
                                time.time(),
                            )
                        )
                    if bullet[0].get_can_break_wall() and let.get_strength() != 999:
                        let.set_strength(let.get_strength() - 1)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    break
        if pause_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                flag = pause(screen)
                if flag:
                    new_bonus_pos = {}
                    for b in bonus:
                        if b[2] in bonus_pos:
                            new_bonus_pos[b[2]] = bonus_pos[b[2]]
                    save(
                        lets,
                        player_tank,
                        patrol_tanks,
                        attackers,
                        chasers,
                        new_bonus_pos,
                        level_num,
                        tuple_base_pos,
                        base_health,
                        map,
                        SPAWN_X,
                        SPAWN_Y,
                    )
        screen.blit(pause_image, pause_rect)
        screen.blit(back_image_in_game, back_pos)
        pygame.display.flip()
