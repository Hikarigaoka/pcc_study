class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 400
        self.bg_color = (135, 206, 235) # Sky blue
        self.ground_color = (34, 139, 34) # Forest green
        self.fps = 60
        
        # Player settings
        self.player_width = 40
        self.player_height = 40
        self.player_color = (0, 0, 255) # Sonic Blue
        self.gravity = 0.8
        self.jump_strength = -16
        self.player_speed = 5
        self.player_hp = 100
        self.player_hp_recovery_rate = 0.02 # Very slow passive regen
        self.weapon_upgrade_duration = 600 # 10 seconds
        
        self.shield_max_hp = 50
        self.shield_recovery_rate = 0.2
        self.shield_break_cooldown = 180 # 3 seconds at 60 FPS
        
        self.attack_duration = 10 # frames (visual recoil)
        self.attack_cooldown = 20 # frames (fire rate)
        
        # Bullet settings
        self.bullet_speed = 10
        self.bullet_width = 10
        self.bullet_height = 5
        self.player_bullet_color = (255, 255, 0) # Yellow
        self.enemy_bullet_color = (128, 0, 128) # Purple
        
        self.weapon_plasma_damage = 30 # High damage
        self.weapon_plasma_speed = 8
        self.weapon_plasma_color = (0, 255, 255) # Cyan
        
        # Enemy settings
        self.enemy_speed = 3
        self.enemy_width = 40
        self.enemy_height = 40
        self.enemy_color = (255, 0, 0) # Red
        self.enemy_hp = 30 # Nerfed from 50
        self.enemy_attack_range = 400 # Shooting range
        self.enemy_attack_cooldown = 60 # Slower fire rate
        
        # Rolling Obstacle settings
        self.rolling_obstacle_speed = 5
        self.rolling_obstacle_radius = 15
        self.rolling_obstacle_color = (139, 69, 19) # Saddle Brown (Mine-like)
        
        # Supply Drop settings
        self.helicopter_speed = 3
        self.supply_drop_speed = 2 # Slow fall
        self.heal_amount = 30
