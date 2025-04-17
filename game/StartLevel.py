import ctypes
import time

import Let
import pygame.transform
from BehaviorStrategy import AttackerStrategy, ChaserStrategy, PatrolStrategy
from Bullet import (
    ConcretePunchingBullet,
    DefaultBullet,
    IncendiaryBullet,
    PlayerBullet,
)
from CyclicIterator import CyclicIterator
from Tank import ArmorTank, FastTank, PlayerTank, RapidFireTank, WeakTank


def start_level(map, level_num):
    """
    Запускает уровень
    :param map: карта уровня
    :param level_num: номер уровня
    :return: статус игры
    """
    map = [row[:] for row in map]

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

    armor_image = pygame.image.load("../game_images/armor.png")
    armor_image = pygame.transform.scale(armor_image, (50, 50))
    armor_rect = None

    game_over = pygame.image.load("../game_images/game_over.jpg")
    game_over = pygame.transform.scale(game_over, (1920, 1080))
    game_rect = game_over.get_rect(topleft=(0, 0))

    replay_button = pygame.image.load("../game_images/replay_button.png")
    replay_button = pygame.transform.scale(replay_button, (280, 70))
    replay_button_rect = replay_button.get_rect(
        center=(width // 2, (height * 3.5) // 5)
    )

    winner = pygame.image.load("../game_images/winner.jpg")
    winner = pygame.transform.scale(winner, (1920, 1080))
    winner_rect = winner.get_rect(topleft=(0, 0))

    health_image = pygame.image.load("../game_images/health.png")
    health_image = pygame.transform.scale(health_image, (50, 50))
    health_rect = None

    speed_image = pygame.image.load("../game_images/speed.png")
    speed_image = pygame.transform.scale(speed_image, (60, 40))
    speed_rect = None

    flame_image = pygame.image.load("../game_images/flame.png")
    flame_image = pygame.transform.scale(flame_image, (100, 100))

    base_image = pygame.image.load("../game_images/base.jfif")
    base_image = pygame.transform.scale(base_image, (100, 100))
    base_pos = None

    player_tank_image = pygame.image.load("../game_images/player_tank.png")
    player_tank_image = pygame.transform.scale(player_tank_image, (75, 75))

    back_image = pygame.image.load("../game_images/back.png")
    back_image_in_game = pygame.transform.scale(back_image, (100, 100))
    back_pos = back_image_in_game.get_rect(topleft=(0, -25))

    back_image_lost = pygame.transform.scale(back_image, (250, 250))
    back_image_lost_rect = back_image_lost.get_rect(
        center=(width // 2, (height * 4) // 5)
    )

    next_image = pygame.image.load("../game_images/next_button.png")
    next_image = pygame.transform.scale(next_image, (250, 125))
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

    for y in range(height // let_size):
        for x in range(width // let_size):
            if map[y][x] == "b" and (
                    x == 0
                    or y == 0
                    or x == width // let_size - 1
                    or y == height // let_size - 1
            ):
                lets.append(Let.Brick(999, x * let_size, y * let_size))
            elif map[y][x] == "b" or map[y][x] == "s":
                lets.append(Let.Brick(3, x * let_size, y * let_size))
            elif map[y][x] == "i":
                lets.append(Let.Ice(x * let_size, y * let_size))
            elif map[y][x] == "r":
                lets.append(Let.Rock(x * let_size, y * let_size))
            elif map[y][x] == "p":
                lets.append(Let.Plant(x * let_size, y * let_size))
            elif map[y][x] == "w":
                lets.append(Let.Water(x * let_size, y * let_size))
            elif map[y][x] == "d":
                tuple_base_pos = (x, y)
                base_pos = base_image.get_rect(
                    center=(
                        x * let_size + let_size // 2,
                        y * let_size + let_size // 2,
                    )
                )
            elif map[y][x] == "u":
                player_tank.x = SPAWN_X = x * let_size + let_size // 2
                player_tank.y = SPAWN_Y = y * let_size + let_size // 2
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
                speed_rect = speed_image.get_rect(
                    center=(x * let_size, y * let_size)
                )
            elif map[y][x] == "a":
                armor_rect = armor_image.get_rect(
                    center=(x * let_size, y * let_size)
                )
            elif map[y][x] == "h":
                health_rect = health_image.get_rect(
                    center=(x * let_size, y * let_size)
                )

    bonus = [
        (speed_image, speed_rect),
        (armor_image, armor_rect),
        (health_image, health_rect),
    ]

    bullets = []
    start_time = 0

    patrol_tanks = []

    patrol_tank1 = FastTank(
        patrol1[0][0],
        patrol1[0][1],
        DefaultBullet(patrol1[0][0], patrol1[0][1], 0),
        0,
        PatrolStrategy(
            patrol1[0][0], patrol1[0][1], patrol1[1][0], patrol1[1][1]
        ),
    )
    iterator1 = CyclicIterator(patrol1)
    patrol_tanks.append((patrol_tank1, iterator1))

    patrol_tank2 = ArmorTank(
        patrol2[0][0],
        patrol2[0][1],
        DefaultBullet(patrol2[0][0], patrol2[0][1], 0),
        0,
        PatrolStrategy(
            patrol2[0][0], patrol2[0][1], patrol2[1][0], patrol2[1][1]
        ),
    )
    iterator2 = CyclicIterator(patrol2)
    patrol_tanks.append((patrol_tank2, iterator2))

    patrol_tank3 = WeakTank(
        patrol3[0][0],
        patrol3[0][1],
        DefaultBullet(patrol3[0][0], patrol3[0][1], 0),
        0,
        PatrolStrategy(
            patrol3[0][0], patrol3[0][1], patrol3[1][0], patrol3[1][1]
        ),
    )
    iterator3 = CyclicIterator(patrol3)
    patrol_tanks.append((patrol_tank3, iterator3))

    patrol_tank4 = RapidFireTank(
        patrol4[0][0],
        patrol4[0][1],
        DefaultBullet(patrol4[0][0], patrol4[0][1], 0),
        0,
        PatrolStrategy(
            patrol4[0][0], patrol4[0][1], patrol4[1][0], patrol4[1][1]
        ),
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
        tank.strategy.find_path(
            map, (pos[0] // 40, pos[1] // 40), tuple_base_pos
        )

    chasers = []
    update_chaser = False
    flames = []

    for pos in chaser_pos:
        tank = WeakTank(
            pos[0],
            pos[1],
            IncendiaryBullet(pos[0], pos[1], 0),
            0,
            ChaserStrategy(pos[0], pos[1], map),
        )
        chasers.append(tank)

    while running:
        screen.fill("black")
        cooldown = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()

        if len(attackers + chasers + patrol_tanks) == 0:
            screen.blit(winner, winner_rect)
            screen.blit(replay_button, replay_button_rect)
            screen.blit(back_image_lost, back_image_lost_rect)
            screen.blit(next_image, next_rect)
            if replay_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return "play" + level_num
            if back_image_lost_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return "menu"
            if next_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return "next" + level_num
            pygame.display.flip()
            continue

        if base_health <= 0:
            screen.blit(game_over, game_rect)
            screen.blit(replay_button, replay_button_rect)
            screen.blit(back_image_lost, back_image_lost_rect)
            if replay_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return "play" + level_num
            if back_image_lost_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return "menu"
            pygame.display.flip()
            continue
        else:
            screen.blit(base_image, base_pos)

        if back_pos.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return "menu"
        keys = pygame.key.get_pressed()

        original_player_tank_pos = (player_tank.x, player_tank.y)
        if keys[pygame.K_w]:
            player_tank.y -= player_tank.speed
            player_tank.direction = 0
        elif keys[pygame.K_s]:
            player_tank.y += player_tank.speed
            player_tank.direction = 180
        elif keys[pygame.K_a]:
            player_tank.x -= player_tank.speed
            player_tank.direction = 90
        elif keys[pygame.K_d]:
            player_tank.x += player_tank.speed
            player_tank.direction = -90
        if keys[pygame.K_SPACE] and cooldown - player_tank.attack_speed >= 0:
            start_time = time.time()
            bullet = player_tank.bullet
            bullet.__init__(
                original_player_tank_pos[0],
                original_player_tank_pos[1],
                player_tank.direction,
            )
            bullets.append((bullet, 1))

        rotated_tank = pygame.transform.rotate(
            player_tank_image, player_tank.direction
        )
        new_rect = rotated_tank.get_rect(
            center=(int(player_tank.x), int(player_tank.y))
        )

        for tank in attackers:
            for let in lets:
                let_rect = let.image.get_rect(topleft=(let.x, let.y))
                if let.strength <= 0:
                    lets.remove(let)
                    update_chaser = True
                    map[let.y // 40] = (
                        map[let.y // 40][: (let.x // 40)]
                        + " "
                        + map[let.y // 40][((let.x // 40) + 1):]
                    )
                    continue
                screen.blit(let.image, let_rect)
                if new_rect.colliderect(let_rect):
                    player_tank.x = original_player_tank_pos[0]
                    player_tank.y = original_player_tank_pos[1]
                if tank.strategy.image.get_rect(
                        center=(int(tank.strategy.x), int(tank.strategy.y))
                ).colliderect(let_rect):
                    tank.strategy.x = tank.strategy.old_x
                    tank.strategy.y = tank.strategy.old_y
                if tank.strategy.image.get_rect(
                        center=(int(tank.strategy.x), int(tank.strategy.y))
                ).colliderect(base_pos):
                    tank.strategy.x = tank.strategy.old_x
                    tank.strategy.y = tank.strategy.old_y

        if len(attackers) == 0:
            for let in lets:
                let_rect = let.image.get_rect(topleft=(let.x, let.y))
                if let.strength <= 0:
                    lets.remove(let)
                    update_chaser = True
                    map[let.y // 40] = (
                        map[let.y // 40][: (let.x // 40)]
                        + " "
                        + map[let.y // 40][((let.x // 40) + 1):]
                    )
                    continue
                screen.blit(let.image, let_rect)
                if new_rect.colliderect(let_rect):
                    player_tank.x = original_player_tank_pos[0]
                    player_tank.y = original_player_tank_pos[1]

        for tank in patrol_tanks:
            res = tank[0].strategy.update(
                screen, tank[0].speed, tank[0].health_point, tank[0].armor
            )
            if time.time() - tank[0].last_shot >= tank[0].attack_speed:
                bullets.append(
                    (
                        DefaultBullet(
                            tank[0].strategy.x,
                            tank[0].strategy.y,
                            tank[0].strategy.angle,
                        ),
                        2,
                    )
                )
                tank[0].update_last_shot(time.time())

            if res == -1:
                new_pos = next(tank[1])
                tank[0].strategy.set_new_point(new_pos[0], new_pos[1])

        for tank in attackers:
            tank.strategy.update(
                screen, tank.speed, tank.health_point, tank.armor
            )
            if time.time() - tank.last_shot >= tank.attack_speed:
                bullets.append(
                    (
                        ConcretePunchingBullet(
                            tank.strategy.x,
                            tank.strategy.y,
                            tank.strategy.angle,
                        ),
                        2,
                    )
                )
                tank.update_last_shot(time.time())

        for tank in chasers:
            if update_chaser:
                tank.strategy.create_grid(map)
                tank.strategy.updatable = True
            tank.strategy.update(
                screen,
                tank.speed,
                tank.health_point,
                tank.armor,
                player_tank.x,
                player_tank.y,
            )
            if time.time() - tank.last_shot >= tank.attack_speed:
                bullets.append(
                    (
                        IncendiaryBullet(
                            tank.strategy.x,
                            tank.strategy.y,
                            tank.strategy.angle,
                        ),
                        2,
                    )
                )
                tank.update_last_shot(time.time())
        update_chaser = False

        new_rect = rotated_tank.get_rect(
            center=(int(player_tank.x), int(player_tank.y))
        )
        screen.blit(rotated_tank, new_rect)
        pygame.draw.rect(
            screen,
            "red",
            (
                player_tank.x - 35,
                player_tank.y - 55,
                player_tank.health_point,
                10,
            ),
        )
        pygame.draw.rect(
            screen,
            "white",
            (player_tank.x - 35, player_tank.y - 70, player_tank.armor, 10),
        )

        if (
                new_rect.colliderect(armor_rect)
                and (armor_image, armor_rect) in bonus
        ):
            player_tank.armor = 80
            bonus.remove((armor_image, armor_rect))

        if (
                new_rect.colliderect(speed_rect)
                and (speed_image, speed_rect) in bonus
        ):
            player_tank.speed = 3
            bonus.remove((speed_image, speed_rect))

        if (
                new_rect.colliderect(health_rect)
                and (health_image, health_rect) in bonus
        ):
            player_tank.health_point = 100
            bonus.remove((health_image, health_rect))

        for bon in bonus:
            screen.blit(bon[0], bon[1])
        for flame in flames:
            if time.time() - flame[1] <= 2:
                screen.blit(flame_image, flame[0])
                if flame[0].colliderect(new_rect):
                    if player_tank.armor > 0:
                        player_tank.armor -= 0.3
                    else:
                        player_tank.health_point -= 0.3
                    if player_tank.health_point <= 0:
                        player_tank.health_point = 80
                        player_tank.x = SPAWN_X
                        player_tank.y = SPAWN_Y

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
                    if bullet[0].fire:
                        flame_x = bullet_rect.x
                        flame_y = bullet_rect.y
                        flames.append(
                            (
                                flame_image.get_rect(
                                    center=(flame_x, flame_y)
                                ),
                                time.time(),
                            )
                        )
                    if player_tank.armor > 0:
                        player_tank.armor -= bullet[0].damage
                    else:
                        player_tank.health_point -= bullet[0].damage
                    bullets.remove(bullet)
                    if player_tank.health_point <= 0:
                        player_tank.health_point = 80
                        player_tank.x = SPAWN_X
                        player_tank.y = SPAWN_Y

            if bullet[1] == 1:
                for tank in patrol_tanks:
                    if bullet_rect.colliderect(
                            tank[0].strategy.image.get_rect(
                                center=(tank[0].strategy.x, tank[0].strategy.y)
                            )
                    ):
                        if tank[0].armor > 0:
                            tank[0].armor -= bullet[0].damage
                            bullets.remove(bullet)
                        else:
                            tank[0].health_point -= bullet[0].damage
                            bullets.remove(bullet)
                        if tank[0].armor <= 0 and tank[0].health_point <= 0:
                            patrol_tanks.remove(tank)

                for tank in chasers:
                    if bullet in bullets:
                        if bullet_rect.colliderect(
                                tank.strategy.image.get_rect(
                                    center=(tank.strategy.x, tank.strategy.y)
                                )
                        ):
                            if tank.armor > 0:
                                tank.armor -= bullet[0].damage
                                bullets.remove(bullet)
                            else:
                                tank.health_point -= bullet[0].damage
                                bullets.remove(bullet)
                            if tank.armor <= 0 and tank.health_point <= 0:
                                chasers.remove(tank)

                for tank in attackers:
                    if bullet in bullets:
                        if bullet_rect.colliderect(
                                tank.strategy.image.get_rect(
                                    center=(tank.strategy.x, tank.strategy.y)
                                )
                        ):
                            if tank.armor > 0:
                                tank.armor -= bullet[0].damage
                                bullets.remove(bullet)
                            else:
                                tank.health_point -= bullet[0].damage
                                bullets.remove(bullet)
                            if tank.armor <= 0 and tank.health_point <= 0:
                                attackers.remove(tank)
            for let in lets:
                let_rect = let.image.get_rect(topleft=(let.x, let.y))
                if bullet_rect.colliderect(let_rect):
                    if bullet[0].fire:
                        flame_x = bullet_rect.x
                        flame_y = bullet_rect.y
                        flames.append(
                            (
                                flame_image.get_rect(
                                    center=(flame_x, flame_y)
                                ),
                                time.time(),
                            )
                        )
                    if bullet[0].can_break_wall and let.strength != 999:
                        let.strength -= 1
                    if bullet in bullets:
                        bullets.remove(bullet)
                    break
        screen.blit(back_image_in_game, back_pos)
        pygame.display.flip()
