class Settings:
    """외계인 침공 게임의 세팅을 모두 저장하는 클래스"""

    def __init__(self):
        """게임 세팅을 초기화합니다"""
        
        # 화면 세팅
        self.screen_width  = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 우주선 세팅
        self.ship_speed = 1.5