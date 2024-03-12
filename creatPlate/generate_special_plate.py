import errno

import cv2, os
import argparse

from .generate_multi_plate import MultiPlateGenerator


def parse_args(plateNum):
    parser = argparse.ArgumentParser(description='中国车牌生成器')
    parser.add_argument('--double', action='store_true', default=False, help='是否双层车牌')
    parser.add_argument('--bg-color', default='blue', help='车牌底板颜色')
    parser.add_argument('--plate-number', default=plateNum, help='车牌号码')
    args = parser.parse_args()
    return args


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def creatPlate(plateNum):
    args = parse_args(plateNum)
    print(args)

    generator = MultiPlateGenerator('plate_model', 'font_model')
    img = generator.generate_plate_special(args.plate_number, args.bg_color, args.double)
    cv2.imwrite('./plate.jpg', img)
    # cv2.imwrite('{}.jpg'.format(args.plate_number), img)
    return [[0, img]]
