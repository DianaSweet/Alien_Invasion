class GameStats():
    #跟踪游戏的统计信息
    def __init__(self,ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        #任何时候都不重置最高得分
        with open('high_score.txt') as f_obj:
            self.high_score = int(f_obj.read())

        #使游戏开始时处于非活动状态
        self.game_active = False

    def reset_stats(self):
        #初始化在游戏运行中可能变化的统计信息(为了之后重置，恢复原数据)
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1