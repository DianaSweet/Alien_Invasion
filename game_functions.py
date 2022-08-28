import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    #响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('high_score.txt','w') as f_obj:
                f_obj.write(str(stats.high_score))
            sys.exit()

        elif event.type == pygame.KEYDOWN:
           check_keydown_events(event,ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    #单击Play开始新游戏(同时重置原来的游戏)
    '''这里存在一个问题，若仅仅以鼠标点击play_button位置作为游戏开始标志时，游戏中点击play按钮仍会
    重置游戏，所以此时增添条件，仅在game_active为False时点击Play为有效'''
    if play_button.rect.collidepoint(mouse_x,mouse_y):
        start_game(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

def check_keydown_events(event,ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    #响应按键
    if event.key == pygame.K_RIGHT:
        # 右移飞船,改变飞船的移动标志moving_right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 左移飞船
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
       fire_bullet(ai_settings,screen,ship,bullets)
    #点击q退出游戏
    elif event.key == pygame.K_q:
        with open('high_score.txt', 'w') as f_obj:
            f_obj.write(str(stats.high_score))
        sys.exit()
    #点击p开始（重置）游戏
    elif event.key == pygame.K_p:
        start_game(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

def check_keyup_events(event,ship):
    #响应松开键盘
    if event.key == pygame.K_RIGHT:
        # 松开移动键,改变飞船的移动标志moving_right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # 改变moving_left
        ship.moving_left = False

def update_screen(ai_settings,screen,stats,sb,ship,bullets,aliens,play_button):
    #更新屏幕图像，切换新屏幕
    # 每次循环前都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #在游戏非活跃时刻绘制“play”按钮
    if not stats.game_active:
        play_button.draw_button()
    #显示得分
    sb.show_score()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def fire_bullet(ai_settings,screen,ship,bullets):
    #在达到限制之前发射一颗子弹
    # 创建一颗子弹，将其加入编组bullets中
    if len(bullets) < ai_settings.bullets_allowed: #此时子弹数小于bullets_allowed，为3个
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #更新子弹的位置，并删除多余的子弹
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    # 检查是否有子弹击中了外星人，击中后删除相应子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    #加分(多发子弹同时命中/一颗子弹命中多个外星人)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        #检查并更换最高得分
        check_high_score(stats, sb)
    # 检查外星人数目，清空后再建一组
    if len(aliens) == 0:
        #消灭一群外星人后等级提升
        stats.level += 1
        sb.prep_level()
        # 先删除子弹，再创建外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings,alien_width):
    #获取外星人的数
    available_space_x = ai_settings.screen_width - 2 * alien_width  # 计算一行内外星人的数量
    number_aliens_x = int(available_space_x / (2 * alien_width))  # 外星人之间的间距是外星人的宽度
    return number_aliens_x

def get_number_aliens_y(ai_settings,ship_height,alien_height):
    #计算屏幕中外星人的行数
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_aliens_y = int(available_space_y/(2 * alien_height))
    return number_aliens_y

def create_alien(ai_settings,screen,aliens,alien_width,alien_number,row_number):
    # 创建第一行外星人
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x  # 同样为了解决rect不能取小数的问题
    # 创建后续的外星人行
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
    #创建外星人群,计算数目
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width  # 避免多次访问alien.rect，我们令alien_width为宽度
    number_aliens_x = get_number_aliens_x(ai_settings,alien_width)
    number_alien_y = get_number_aliens_y(ai_settings,ship.rect.height,alien.rect.height) #这里需要访问ship和alien的属性
    #调用函数，创建第一行外星人
    for row_number in range(number_alien_y):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_width,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    #碰撞时执行操作
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings,aliens)
            break #在外星人群中若有一个发生边缘碰撞，便改变整个群体的方向，并且跳出循环


def change_fleet_direction(ai_settings,aliens):
    #每次碰撞执行下移，并改变运动方向
    for alien in aliens.sprites(): #此时改变了所有外星人的方向
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,stats,sb,aliens,ship,bullets):
    #响应被外星人撞到的飞船
    if stats.ships_left > 0:
        #减少剩余飞船数，并更新画面
        stats.ships_left -= 1
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建新的外星人群，将飞船重置到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #同时暂停游戏，给一段反应时间
        sleep(0.5)
    else: #无飞船剩余时
        stats.game_active = False
        pygame.mouse.set_visible(True) #结束后使光标重新出现

def check_aliens_bottom(ai_settings,screen,stats,sb,aliens,ship,bullets):
    #检查外星人是否到达屏幕底端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #游戏停止，像飞船被撞一样处理
            ship_hit(ai_settings,screen,stats,sb,aliens,ship,bullets)
            break #有一个外星人到达底端即可

def update_aliens(ai_settings,screen,stats,sb,aliens,ship,bullets):
    check_fleet_edges(ai_settings,aliens) #这样在每个主循环中都会遍历一遍所有的外星人，感觉会很慢
    #更新外星人的位置
    aliens.update()
    #检查外星人是否到达底端
    check_aliens_bottom(ai_settings,screen,stats,sb,aliens,ship,bullets)
    #检测飞船与外星人的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,aliens,ship,bullets)

def start_game(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    if not stats.game_active:
        #隐藏光标
        pygame.mouse.set_visible(False)
        #开始游戏，同时重置
        stats.game_active = True
        stats.reset_stats()
        #重置外星人，飞船，删除子弹
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #重置记分牌的信息
        # 最高成绩没有改变，我觉得这里不需要调用最高成绩,但重构后会自动调用
        sb.prep_images()

def check_high_score(stats,sb):
    '''检查是否出现了新的最高得分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()