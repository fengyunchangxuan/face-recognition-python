class Settings:
    """人脸识别设置"""

    # 初始化
    def __init__(self) -> None:
        self.h_f_alt = r'C:/Program Files/opencv/sources/data/haarcascades/haarcascade_frontalface_alt.xml'
        self.db_path = 'db/test'
        self.trainner_path = "trainner/trainner.yml"
