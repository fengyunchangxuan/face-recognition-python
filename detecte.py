import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from user import User
from settings import Settings


class Detection:
    """检测、校验并输出结果"""

    def __init__(self) -> None:
        """初始化"""
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.settings = Settings()
        self.user = User(self.settings.db_path)
        # 再次调用人脸分类器
        self.face_cascade = cv2.CascadeClassifier(self.settings.h_f_alt)
        # 加载一个字体，用于识别后，在图片上标注出对象的名字
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        rows = self.user.select()
        for row in rows:
            print(row)

    def add_text(self, image, text, position,  color, fontsize=20):
        """图片上添加中文"""

        # 图像从OpenCV格式转换成PIL格式
        img_PIL = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        font = ImageFont.truetype('simhei.ttf', fontsize, encoding="utf-8")

        draw = ImageDraw.Draw(img_PIL)
        # PIL图片上打印汉字 # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
        draw.text(position, text, font=font, fill=color)
        img = cv2.cvtColor(np.asarray(img_PIL),
                           cv2.COLOR_RGB2BGR)  # PIL图片转cv2 图片
        return img

    def get_user_name(self, user_id):
        """根据查询到的用户id返回用户名"""
        rows = self.user.select_name(user_id)
        names = [row[0] for row in rows]
        return names[0]

    def start(self):
        """识别"""

        # 调用摄像头
        capture = cv2.VideoCapture(cv2.CAP_DSHOW)
        minW = 0.1 * capture.get(3)
        minH = 0.1 * capture.get(4)
        # 使用之前训练好的模型
        self.recognizer.read(self.settings.trainner_path)

        while True:

            ret, img = capture.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 识别人脸
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH))
            )
            # 进行校验
            for(x, y, w, h) in faces:

                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                user_id, level = self.recognizer.predict(
                    gray[y:y+h, x:x+w])

                user_name = self.get_user_name(user_id)

                # 计算出一个检验结果
                if level > 100:
                    user_name = "unknown"

                level = str(round(100-level)) + '%'
                # 输出检验结果以及用户名

                img = self.add_text(img, user_name, (x+5, y-25), (0, 0, 255))
                img = self.add_text(img, level, (x+5, y+h-5), (0, 0, 0))

                # 展示结果
                cv2.imshow('camera', img)
                k = cv2.waitKey(20)
                if k == 27:
                    break

        capture.release()
        cv2.destroyAllWindows()


detection = Detection()
detection.start()
