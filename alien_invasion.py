import sys
import pygame
from pygame.sprite import Group

#导入设置类
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
import game_functions as gf
from button import Button

def run_game():
    #初始化游戏
    pygame.init()
    ai_settings = Settings()

    #创建一个屏幕对象
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建一艘飞船
    ship = Ship(ai_settings,screen)

    #创建一个用于存储子弹的编组
    bullets = Group()

    #创建外星人的编组
    aliens = Group()

    #创造外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #创建一个存储游戏统计信息的实例,并创立一个计分板
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    #创建一个play按钮
    play_button = Button(ai_settings,screen,"Play")

    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

        if stats.game_active: #当有飞船剩余时，运行这些部分
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,aliens,ship,bullets)

        gf.update_screen(ai_settings,screen,stats,sb,ship,bullets,aliens,play_button)
run_game()