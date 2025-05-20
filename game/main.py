import os

import pygame
from end_game import end_screen
from start_level import start_level
from start_window import start_window
from states import States


def main() -> None:
    """
    Главная функция отвечает за запуск уровнений и доп экранов
    """
    map_level_1 = [
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "b                r                  r          b",
        "b    !    !  3   rbbbbbbbbbbbbbbbbbbr       3  b",
        "b                                              b",
        "b                @    2   @#        #          b",
        "b    ! 2  !                            $       b",
        "b                rbbbbbbbbbbbbbbbbbbr       2  b",
        "b    wwwwww      r                  r          b",
        "b 3  wwwwww      r                  r          b",
        "b    wwwwww      r                  r          b",
        "b  rrrrrrrr      r                  r          b",
        "b  r             r                  r          b",
        "b  r             r                  r  $       b",
        "b  r             r                  rrrr   rrrrb",
        "b  r             rp                    r       b",
        "b  r       h     rp                    r       b",
        "b  r             rp                    r       b",
        "brrr   rrrrrrrrrrrpiiiiiiiiiiiiiiiiiiiirrrrr v b",
        "b             ppppp                            b",
        "b                                              b",
        "b                        u                     b",
        "b               a                ppppppppppppppb",
        "bpppppppppp           sssssss    pwwwwwwwwwwwwwb",
        "bwwwwwwwwwp           s     s    pwwwwwwwwwwwwwb",
        "bwwwwwwwwwp           s  d  s    pwwwwwwwwwwwwwb",
        "bwwwwwwwwwp           s     s    pwwwwwwwwwwwwwb",
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ]
    map_level_2 = [
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "b                                              b",
        "b   2  @              3                  @  2  b",
        "b                                              b",
        "b         h                                    b",
        "b     !                                  $     b",
        "b           ppppppppp    pppppppppp            b",
        "b           pwwwwwwww    wwwwwwwwwp            b",
        "b           pww                 wwp      v     b",
        "b           pww                 wwp            b",
        "b           pww     sssssss     wwp            b",
        "b                   s     s                    b",
        "b      3            s  d  s                 3  b",
        "b                   s     s                    b",
        "b                   sssssss                    b",
        "b           pww                 wwp            b",
        "b           pww        u        wwp            b",
        "b           pww                 wwp            b",
        "b           pwwwwwwww     wwwwwwwwp            b",
        "b           ppppppppppppppppppppppp            b",
        "b     !                                        b",
        "b                        3                     b",
        "b           a                             $    b",
        "b                      2                       b",
        "b    #                                   #     b",
        "b                                              b",
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ]

    map_level_3 = [
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "b                               b    iiiwiiiiiib",
        "b     @        3             @  b    iiiiiiwiiib",
        "b                               b    iiiiwiiiiib",
        "b      2       b                b           wwwb",
        "b              b        b               !   wwwb",
        "bbbbbbbbbbbbbbbb   2    b                   wwwb",
        "b              b        b               h   wwwb",
        "b              bbpppppppppppppppppp            b",
        "b                pwwwwwwwwwwwwwwwwp            b",
        "bssss            pwwwwwwwwwwwwwwwwp            b",
        "b   s            pwwwwwwwwwwwwwwwwp      3     b",
        "b d s   u        pwwwwwwwwwwwwwwwwp            b",
        "b   s            pwwwwwwwwwwwwwwwwp            b",
        "bssss            pwwwwwwwwwwwwwwwwp            b",
        "b                pwwwwwwwwwwwwwwwwp            b",
        "b                pppppppppppppppppppppp        b",
        "b                                              b",
        "b     $                  $                     b",
        "b                        v                     b",
        "b     $                  $       pppp   !      b",
        "b                                rwwp          b",
        "brrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrwwp   a      b",
        "b                                rppp          b",
        "b     #      2             3              #    b",
        "b                                              b",
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ]

    map_level_4 = [
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "biiwwiw          ppppppppppppp           wiwiiwb",
        "bwiwiwi  #        ppwwwwwwwwwpp       $  wiwiwib",
        "bwiwiwi      2    ppwwwwwwwpp     2      wiwiwib",
        "b                  ppwwwwwpp                   b",
        "b       3     pppp  ppwwwpp  pppp         3    b",
        "b               ppppppppppppppp                b",
        "b             pppp  ppwwwpp  pppp              b",
        "b                  ppwwwwwpp                   b",
        "b                 ppwwwwwwwpp                  b",
        "b                ppwwwwwwwwwpp                 b",
        "b                ppppppppppppp                 b",
        "b                                     $        b",
        "b        #      h              v               b",
        "b                                              b",
        "bbbbbbbbbbbbbbbbbb     a    bbbbbbbbbbbbbbbbbbbb",
        "bwwwwwwwwwwwwwwwwb          bwwwwwwwwwwwwwwwwwwb",
        "bwwwwwwwwwwwwwwwwb          bwwwwwwwwwwwwwwwwwwb",
        "bbbbbbbbbbbbbbbbbb          bbbbbbbbbbbbbbbbbbbb",
        "bwi                                         wiwb",
        "bwi                    u                    iwib",
        "b   !          !                 @         @   b",
        "b     ppprrppp      sssssss        pprrpp      b",
        "b   ppppprrppppp    s     s      pppprrpppp    b",
        "b   rrrrrrrrrrrr    s  d  s      rrrrrrrrrr    b",
        "b   rrrrrrrrrrrr    s     s   3  rrrrrrrrrr  2 b",
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ]

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    background_music_path = os.path.join(base_dir, "sounds", "background_music.mp3")
    pygame.mixer.music.load(background_music_path)
    pygame.mixer.music.set_volume(0.25)

    pygame.mixer.music.play(-1)
    status = start_window()
    while True:
        if status == States.SAVE:
            status = start_level(None, None)
        if "play" in status.value:
            if status == States.PLAY_1:
                status = start_level(map_level_1, "1")
            if status == States.PLAY_2:
                status = start_level(map_level_2, "2")
            if status == States.PLAY_3:
                status = start_level(map_level_3, "3")
            if status == States.PLAY_4:
                status = start_level(map_level_4, "4")
        if status == States.MENU:
            status = start_window()
        if status == States.NEXT_1:
            status = States.PLAY_2
        if status == States.NEXT_2:
            status = States.PLAY_3
        if status == States.NEXT_3:
            status = States.PLAY_4
        if status == States.NEXT_4:
            status = end_screen()


main()
