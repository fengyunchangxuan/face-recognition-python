import os
import cv2
import numpy as np
from PIL import Image
from settings import Settings

settings = Settings()


class Trainner:
    """建立模型、创建数据集"""

    def __init__(self) -> None:
        """初始化"""
        self.path = "data"
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier(settings.h_f_alt)
        # 图片
        self.images = []
        # 标签
        self.labels = []

    def get_images(self):
        """获取目录下的图片,并将目录设定为图片的标签"""

        # 列举总目录下的文件夹，每个文件夹对应一个用户，文件夹的名称就是用户的id
        for user_id in os.listdir(self.path):

            # 列举用户文件夹下的图片
            for file_name in os.listdir(os.path.join(self.path, user_id)):

                # 将总的目录名、用户文件夹名（用户id）、图片名称拼接成完整的图片地址
                image_path = os.path.join(self.path, user_id, file_name)

                # 通过图片路径将其转换为灰度图片
                img = Image.open(image_path).convert('L')

                # 将图片转化为数组
                imgs = np.array(img, 'uint8')

                faces = self.detector.detectMultiScale(imgs)

                # 将获取的图片和id添加到list中
                for(x, y, w, h) in faces:
                    self.images.append(imgs[y:y+h, x:x+w])
                    self.labels.append(int(user_id))

    def train(self):
        """调用函数并将数据喂给识别器训练"""

        print('Training...')

        self.get_images()
        # 训练模型
        self.recognizer.train(self.images, np.array(self.labels))
        # 保存模型
        self.recognizer.save(settings.trainner_path)


trainner = Trainner()
trainner.train()
