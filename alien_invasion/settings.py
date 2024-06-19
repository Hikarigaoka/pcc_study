class Settings:
    """외계인 침공 게임의 세팅을 모두 저장하는 클래스"""

    def __init__(self):
        """게임 세팅을 초기화합니다"""
        
        # 화면 세팅
        self.screen_width  = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 우주선 세팅
        self.ship_speed = 8

        # 외계인 세팅
        self.alien_speed = 5.0
        self.fleet_drop_speed = 30
        # fleet_direction이 1이면 오른쪽 -1이면 왼쪽입니다
        self.fleet_direction = 1

        # 탄환 세팅
        self.bullet_speed = 80.0
        self.bullet_width = 10
        self.bullet_height = 120
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 100