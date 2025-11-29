class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)
        self.fps = 60
        
        # Player settings
        self.player_speed = 5
        self.player_width = 40
        self.player_height = 40
        self.player_color = (0, 255, 0)
        self.player_max_hp = 100
                
        # Bullet settings
        self.bullet_speed = 7
        self.bullet_width = 4
        self.bullet_height = 10
        self.bullet_color = (255, 255, 0)
        self.bullets_allowed = 5
        
        # Enemy settings
        self.enemy_speed = 2
        self.enemy_width = 30
        self.enemy_height = 30
        self.enemy_color = (255, 0, 0)
        self.fleet_drop_speed = 10
