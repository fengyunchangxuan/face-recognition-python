import cv2
import os
import random
from user import User
from settings import Settings


class Pick:
    """获取人脸样本"""

    # 初始化
    def __init__(self) -> None:
        # 样本数目
        self.count = 0
        self.user_id = random.randint(10000, 99999)
        self.user_name = input('输入名字:')
        self.settings = Settings()
        # 调用人脸分类器，要根据实际路径调整
        self.face_detector = cv2.CascadeClassifier(self.settings.h_f_alt)

    def add_record(self):
        """添加一条记录"""

        self.user = User(self.settings.db_path)
        self.user.insert(self.user_id, self.user_name)
        self.user.close()

    def create_dir(self):
        """创建目录"""
        if not os.path.exists('data/%s' % self.user_id):
            os.mkdir('data/%s' % self.user_id)
        else:
            print('exists')

    def save(self, img, gray, faces):
        # 框选人脸，for循环保证一个能检测的实时动态视频流
        for (x, y, w, h) in faces:
            # xy为左上角的坐标,w为宽，h为高，用rectangle为人脸标记画框
            cv2.rectangle(img, (x, y), (x + w, y + w), (255, 0, 0))
            # 成功框选则样本数增加
            self.count += 1
            # 保存图像，把灰度图片看成二维数组来检测人脸区域
            # (这里是建立了data的文件夹，当然也可以设置为其他路径或者调用数据库)

            img_path = "data/%s/%s.jpg" % (self.user_id, str(self.count))
            cv2.imencode(
                '.jpg', gray[y:y + h, x:x + w])[1].tofile(img_path)

            # 显示图片
            cv2.imshow('image', img)

    def get(self):
        """打开摄像头获取样本"""

        # 调用笔记本内置摄像头，参数为0，如果有其他的摄像头可以调整参数为1,2
        cap = cv2.VideoCapture(cv2.CAP_DSHOW+0)
        while True:
            # 从摄像头读取图片
            success, img = cap.read()

            # 转为灰度图片，减少程序符合，提高识别度
            if success is True:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                break
            # 检测人脸，将每一帧摄像头记录的数据带入OpenCv中，让Classifier判断人脸
            # 其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为minNeighbors
            faces = self.face_detector.detectMultiScale(gray, 1.3, 5)
            self.save(img, gray, faces)

            # 保持画面的连续。waitkey方法可以绑定按键保证画面的收放，通过q键退出摄像
            k = cv2.waitKey(1)
            if k == '27':
                break
                # 或者得到20个样本后退出摄像，这里可以根据实际情况修改数据量，实际测试后800张的效果是比较理想的
            elif self.count >= 20:
                break

        # 关闭摄像头，释放资源
        cap.release()
        cv2.destroyAllWindows()


pick = Pick()
pick.add_record()
pick.create_dir()
pick.get()
