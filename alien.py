import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #表示外星人的类
    def __init__(self,ai_settings,screen):
        #初始化外星人并设置其起始位置
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #每个外星人胜成语屏幕左上角附近
        self.rect.x = self.rect.width #左边距是宽度
        self.rect.y = self.rect.height #上边距是高度

        #存储外星人的精确位置
        self.x = float(self.rect.x)

    def blitme(self):
        #指定位置绘制外星人
        self.screen.blit(self.image,self.rect)

    def update(self):
        #向右移动外星人
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edge(self):
        #外星人撞到边缘时返回True
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right: #右边缘
            return True
        elif self.rect.right <= 0: #左边缘
            return True