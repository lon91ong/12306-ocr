# coding: utf-8
import base64
from os import path

import cv2, os
from tensorflow.compat.v1 import logging as tf_log
import numpy as np
from keras import models

from config import Logger

tf_log.set_verbosity(tf_log.ERROR)


class ShareInstance():
    __session = None

    @classmethod
    def share(cls, **kwargs):
        if not cls.__session:
            cls.__session = cls(**kwargs)
        return cls.__session


class Predict(ShareInstance):
    orc_dir = ''
    model = None
    texts = []
    code_model = None

    def __init__(self):
        self.orc_dir = path.dirname(path.abspath(__file__ + '/../')) + '/ocr/'
        # 识别文字
        self.model = models.load_model('%smodel.v2.0.h5' % self.orc_dir, compile=False)

        with open('%stexts.txt' % self.orc_dir, encoding='utf-8') as f:
            self.texts = [text.rstrip('\n') for text in f]

        # 加载图片分类器
        self.code_model = models.load_model('%s12306.image.model.h5' % self.orc_dir, compile=False)

    def get_text(self, img, offset=0):
        text = img[3:22, 120 + offset:177 + offset]
        text = cv2.cvtColor(text, cv2.COLOR_BGR2GRAY)
        text = text / 255.0
        h, w = text.shape
        text.shape = (1, h, w, 1)
        return text
    
    def get_image_position_by_offset(self, offsets, floatF = False):
        # floatF 返回实数列还是整数列, 默认整数列
        from random import randint
        from math import ceil
        positions = ''
        width = 75
        height = 75
        for offset in offsets:
            random_x = randint(-5, 5)
            random_y = randint(-5, 5)
            offset = int(offset)
            x = width * ((offset - 1) % 4 + 1) - width / 2 + random_x
            y = height * ceil(offset / 4) - height / 2 + random_y
            # 联众格式: 实数 x,y|x,y ; 非联众: 整型 x,y,x,y
            positions += (str(x)+',') if floatF else (str(int(x))+',')
            positions += (str(y)+'|') if floatF else (str(int(y))+',')
        return positions[:-1]

    def get_coordinate(self, img_str, option = 'list'):
        # 储存最终坐标结果, 默认返回序号列表
        result = ''

        try:
            # 读取并预处理验证码
            img = cv2.imdecode(np.fromstring(img_str, np.uint8), cv2.IMREAD_COLOR)
            text = self.get_text(img)
            imgs = np.array(list(self._get_imgs(img)))
            imgs = self.preprocess_input(imgs)

            label = self.model.predict(text)
            label = label.argmax()
            text = self.texts[label]

            # list放文字
            titles = [text]

            position = []

            # 获取下一个词
            # 根据第一个词的长度来定位第二个词的位置
            offset = 27 if len(text) == 1 else 47 if len(text) == 2 else 60

            text2 = self.get_text(img, offset=offset)
            if text2.mean() < 0.95:
                label = self.model.predict(text2)
                label = label.argmax()
                text2 = self.texts[label]
                titles.append(text2)

            labels = self.code_model.predict(imgs)
            labels = labels.argmax(axis=1)

            for pos, label in enumerate(labels):
                if self.texts[label] in titles:
                    position.append(pos + 1)

            # 没有识别到结果
            if len(position) == 0:
                return result
            else:
                result = position if option == 'list' else \
                str(position)[1:-1] if option == 'ZhuS' else \
                self.get_image_position_by_offset(position, option == 'LianZ')
            Logger.info('识别结果: %s' % result)
        except:
            pass
        return result

    def preprocess_input(self, x):
        x = x.astype('float32')
        # 用cv2来读取的图片，其已经是BGR格式了
        mean = [103.939, 116.779, 123.68]
        x -= mean
        return x

    def _get_imgs(self, img):
        interval = 5
        length = 67
        for x in range(40, img.shape[0] - length, interval + length):
            for y in range(interval, img.shape[1] - length, interval + length):
                yield img[x:x + length, y:y + length]

if __name__ == '__main__':
    for i in range(10):
        with open('test.jpg', 'r') as f:
            print(Predict.share().get_coordinate(f.buffer.read()))
