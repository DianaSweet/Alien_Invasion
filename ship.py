import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self,ai_settings,screen):
        #初始化飞船并设置其初始位置
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx #屏幕的中心即为飞船的中心
        self.rect.bottom = self.screen_rect.bottom #屏幕的底部即为飞船的底部

        #在飞船的属性中存放小数值（便于移动）
        self.center = float(self.rect.centerx)

        #飞船的移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #调整飞机位置 and 飞机未超边界 (用两个if块，保证同时按下左右键的时候飞船静止不动）
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        #rect.centerx不能存储整数值，这里更新rect对象,让他控制飞船的位置，虽然只能保留整数部分，但影响不大
        self.rect.centerx = self.center

    def blitme(self):
        #在指定位置绘制飞船:
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        #将新的飞船移至屏幕中央
        self.center = self.screen_rect.centerx #通过update()方法将self.center赋给self.rect.centerx，调整飞船位置使其居中