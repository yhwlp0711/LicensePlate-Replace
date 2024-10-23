# import os
#
# import cv2
# import numpy as np
# from PIL import Image
# from PyQt5.QtGui import QImage
#
# imgtypes = ['.jpg', '.png', '.bmp', '.jpeg', '.tif']
# videotypes = ['.mp4', '.avi']
# FPScount = list()
#
# srcImgs = list()
# srcPaths = list()
# dstPath = ""
# dstImg = list()
#
# def init():
#     srcImgs.clear()
#     srcPaths.clear()
#     dstImg.clear()
#     FPScount.clear()
#
# def readVideo(videopath):
#     videoImgs = list()
#     videoImgs.append(-1)
#     currentVideo = cv2.VideoCapture(videopath)
#     # count = 0
#     FPS = currentVideo.get(cv2.CAP_PROP_FPS)
#     while currentVideo.isOpened():
#         ret, frame = currentVideo.read()
#         if ret:
#             videoImgs.append(frame)
#         else:
#             break
#
#     currentVideo.release()
#     return videoImgs, FPS
#
#
# def saveVideo(savapth, imgList, FPS):
#     frameW = imgList[0].shape[1]
#     frameH = imgList[0].shape[0]
#
#     out = cv2.VideoWriter(savapth, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (frameW, frameH))
#     for i in imgList:
#         out.write(i)
#
#     out.release()
#
#
# def readImg(filepath):
#     # init()
#     imgPaths = list()
#     imgList = list()
#     if not os.path.isdir(filepath):
#         _, filename = os.path.split(filepath)
#         _, filetype = os.path.splitext(filename)
#         if filetype in imgtypes:
#             imgList.append([0, cv2.imread(filepath)])
#         elif filetype in videotypes:
#             videoImgs, currentFPS = readVideo(filepath)
#             FPScount.append(currentFPS)
#             imgList.append(videoImgs)
#     else:
#         files = os.listdir(filepath)
#         imgsList = list()
#         for file in files:
#             if not os.path.isdir(file):
#                 _, filename = os.path.split(filepath + '/' + file)
#                 imgPaths.append(filename)
#                 _, filetype = os.path.splitext(filename)
#                 if filetype in imgtypes:
#                     imgsList.append(cv2.imread(filepath + '/' + file))
#                 elif filetype in videotypes:
#                     videoImgs, currentFPS = readVideo(filepath + '/' + file)
#                     FPScount.append(currentFPS)
#                     imgList.append(videoImgs)
#         if not len(imgsList) == 0:
#             imgsList.insert(0, 0)
#             imgList.append(imgsList)
#     return imgList, imgPaths
#
#
# def cv2qt(cvimg):
#     height, width, depth = cvimg.shape
#     temp = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
#     qtimg = QImage(temp.data, width, height, width * depth, QImage.Format_RGB888)
#     return qtimg
#
import os

import cv2
from PyQt5.QtGui import QImage

# 定义支持的图片和视频文件类型
imgtypes = ['.jpg', '.png', '.bmp', '.jpeg', '.tif']
videotypes = ['.mp4', '.avi']
FPScount = list()  # 存储视频的帧率

srcImgs = list()  # 源图片列表
srcPaths = list()  # 源图片路径列表
dstPath = ""  # 目标路径
dstImg = list()  # 目标图片列表


# 初始化全局变量
def init():
    srcImgs.clear()
    srcPaths.clear()
    dstImg.clear()
    FPScount.clear()


# 读取视频文件并返回视频帧列表和帧率
def readVideo(videopath):
    videoImgs = list()
    videoImgs.append(-1)  # 用于标识视频
    currentVideo = cv2.VideoCapture(videopath)
    FPS = currentVideo.get(cv2.CAP_PROP_FPS)  # 获取视频帧率
    while currentVideo.isOpened():
        ret, frame = currentVideo.read()
        if ret:
            videoImgs.append(frame)
        else:
            break

    currentVideo.release()
    return videoImgs, FPS


# 保存视频文件
def saveVideo(savapth, imgList, FPS):
    frameW = imgList[0].shape[1]
    frameH = imgList[0].shape[0]

    # 已废弃
    # out = cv2.VideoWriter(savapth, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (frameW, frameH))
    out = cv2.VideoWriter(savapth, cv2.VideoWriter.fourcc('m', 'p', '4', 'v'), FPS, (frameW, frameH))
    for i in imgList:
        out.write(i)

    out.release()


# 读取图片或视频文件
def readImg(filepath):
    imgPaths = list()
    imgList = list()
    if not os.path.isdir(filepath):  # 如果是文件
        _, filename = os.path.split(filepath)
        _, filetype = os.path.splitext(filename)
        if filetype in imgtypes:  # 如果是图片文件
            imgList.append([0, cv2.imread(filepath)])
        elif filetype in videotypes:  # 如果是视频文件
            videoImgs, currentFPS = readVideo(filepath)
            FPScount.append(currentFPS)
            imgList.append(videoImgs)
    else:  # 如果是目录
        files = os.listdir(filepath)
        imgsList = list()
        for file in files:
            if not os.path.isdir(file):
                _, filename = os.path.split(filepath + '/' + file)
                imgPaths.append(filename)
                _, filetype = os.path.splitext(filename)
                if filetype in imgtypes:  # 如果是图片文件
                    imgsList.append(cv2.imread(filepath + '/' + file))
                elif filetype in videotypes:  # 如果是视频文件
                    videoImgs, currentFPS = readVideo(filepath + '/' + file)
                    FPScount.append(currentFPS)
                    imgList.append(videoImgs)
        if not len(imgsList) == 0:
            imgsList.insert(0, 0)
            imgList.append(imgsList)
    return imgList, imgPaths


# 将OpenCV图片转换为QImage
def cv2qt(cvimg):
    height, width, depth = cvimg.shape
    temp = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
    qtimg = QImage(temp.data, width, height, width * depth, QImage.Format_RGB888)
    return qtimg
