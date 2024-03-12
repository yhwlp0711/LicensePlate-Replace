import cv2
import numpy as np
from detect import detect
from basecode import replaceImgRegionBySpecImg, constructRectFrom4Points, translation
from style.styleTrans import styleTran


def getRect4Point(rect):
    """
    根据矩形的左上角坐标及长和高返回矩形的左上、右上、左下、右下四个点的坐标
    :param rect:为代表矩形的列表，三个元素，分别为左上角坐标、宽和高
    :return:返回矩形的四个顶点，分别是左上、右上、左下、右下四个点的坐标
    """
    luPoint, w, h = rect
    x0, y0 = luPoint
    return (luPoint, (x0 + w, y0), (x0, y0 + h), (x0 + w, y0 + h))


def tranPoint(currentPoint, w, h):
    left = False
    right = False
    up = False
    down = False
    if currentPoint[0][0] < 0:  # 左上横坐标
        left = True
        tempList = list(currentPoint)
        tempList[0] = (0, tempList[0][1])
        currentPoint = tuple(tempList)

    elif currentPoint[1][0] < 0:  # 右上横坐标
        right = True
        tempList = list(currentPoint)
        tempList[1] = (w, tempList[1][1])
        currentPoint = tuple(tempList)

    if currentPoint[2][0] < 0:  # 左下横坐标
        left = True
        tempList = list(currentPoint)
        tempList[2] = (0, tempList[2][1])
        currentPoint = tuple(tempList)

    elif currentPoint[3][0] < 0:  # 右下横坐标
        right = True
        tempList = list(currentPoint)
        tempList[3] = (w, tempList[3][1])
        currentPoint = tuple(tempList)

    if currentPoint[0][1] < 0:  # 左上纵坐标
        up = True
        tempList = list(currentPoint)
        tempList[0] = (tempList[0][0], 0)
        currentPoint = tuple(tempList)

    elif currentPoint[2][1] < 0:  # 左下纵坐标
        down = True
        tempList = list(currentPoint)
        tempList[2] = (tempList[2][0], h)
        currentPoint = tuple(tempList)

    if currentPoint[1][1] < 0:  # 右上纵坐标
        up = True
        tempList = list(currentPoint)
        tempList[1] = (tempList[1][0], 0)
        currentPoint = tuple(tempList)

    elif currentPoint[3][1] < 0:  # 右下纵坐标
        down = True
        tempList = list(currentPoint)
        tempList[3] = (tempList[3][0], h)
        currentPoint = tuple(tempList)

    index = (currentPoint[3][0] - currentPoint[0][0]) / (currentPoint[3][1] - currentPoint[0][1])

    return currentPoint, index, (left, right, up, down)


def chanePlate(srcImgList, destImgList, flag):
    resultList = list()
    # 获取两车的车牌四角点（左上角、右上角、左下角、右下角）
    srcPointsSelected = detect(srcImgList)

    if flag:
        destPointsSelected = detect(destImgList)[0][0][0]
    else:
        destPointsSelected = [(0, 0), (440, 0), (0, 140), (440, 140)]

    if destPointsSelected is None:
        print("目标图片中未检测到车牌")
        return
    for Itemindex in range(len(srcImgList)):
        currentItemRes = list()
        currentItemRes.append(srcImgList[Itemindex][0])
        srcImgList[Itemindex] = srcImgList[Itemindex][1:]
        for Imgindex in range(len(srcImgList[Itemindex])):
            if len(srcPointsSelected[Itemindex][Imgindex]) == 0:
                print("源图片中未检测到车牌")
                currentItemRes.append(srcImgList[Itemindex][Imgindex])
                continue
            else:
                destImg = destImgList[0][1]
                currentImg = srcImgList[Itemindex][Imgindex]
                w, h, _ = currentImg.shape
                currentPoints = srcPointsSelected[Itemindex][Imgindex]
                for currentPoint in currentPoints:

                    currentPoint, index, isScale = tranPoint(currentPoint, w, h)
                    destPointsSelected1 = destPointsSelected
                    destRect = constructRectFrom4Points(destPointsSelected)  # 根据目标车牌的左上角、右上角、左下角、右下角4四角顶点以左上角构建矩形
                    if isScale[0]:
                        newW = int(destRect[2] * index)
                        newPoint = (destRect[0][0] + (destRect[1] - newW), destRect[0][1])
                        destRect = (newPoint, newW, destRect[2])
                        destPointsSelected1 = (newPoint, destPointsSelected[1], (newPoint[0], newPoint[1] + destRect[2]),
                                              destPointsSelected[3])
                    elif isScale[1]:
                        newW = int(destRect[2] * index)
                        destRect = (destRect[0], newW, destRect[2])
                        destPointsSelected1 = (destPointsSelected[0][0], (destPointsSelected[1][0] - destRect[1], destPointsSelected[1][1]),
                                              destPointsSelected[2],(destPointsSelected[1][0] - destRect[1], destPointsSelected[3][1]))
                    if isScale[2]:
                        newH = int(destRect[1] / index)
                        newPoint = (destRect[0][0], destRect[0][1] + (destRect[1] - newH))
                        destRect = (newPoint, destRect[1], newH)
                        destPointsSelected1 = (newPoint, (newPoint[0] + destRect[1], destPointsSelected[1][1]),
                                              destPointsSelected[2], destPointsSelected[3])
                    elif isScale[3]:
                        newH = int(destRect[1] / index)
                        destRect = (destRect[0], destRect[1], newH)
                        destPointsSelected1 = (destPointsSelected[0], destPointsSelected[1],
                                              (destPointsSelected[2][0], destPointsSelected[2][1] - newH),
                                              (destPointsSelected[3][0], destPointsSelected[3][1] - newH))

                    srcRect = (currentPoint[0], destRect[1], destRect[2])  # 根据目标车牌的矩形大小以源图像车牌左上角构建一个相同大小的矩形

                    # 根据车牌的四顶点将车牌区域映射到对应矩形进行透视变换得到统一车牌大小的中间图像，确保两车车牌大小和形状相同
                    destRectPoints = np.float32(getRect4Point(destRect))
                    srcRectPoints = np.float32(getRect4Point(srcRect))
                    srcPoints = np.float32(currentPoint)
                    destPoints = np.float32(destPointsSelected1)
                    srcM = cv2.getPerspectiveTransform(srcPoints, srcRectPoints)
                    destM = cv2.getPerspectiveTransform(destPoints, destRectPoints)
                    dstSrc = cv2.warpPerspective(currentImg, srcM, (currentImg.shape[1]*2, currentImg.shape[0]*2))
                    dstDst = cv2.warpPerspective(destImg, destM, (destImg.shape[1]*2, destImg.shape[0]*2))

                    destX0, destY0 = constructRectFrom4Points(destPointsSelected1)[0]
                    w = destRect[1]
                    h = destRect[2]
                    resRect = constructRectFrom4Points(currentPoint)
                    srcX0, srcY0 = resRect[0]

                    destPlate = np.array(dstDst[destY0:destY0 + h, destX0:destX0 + w])  # 取目标车牌对应的图像
                    srcPlate = np.array(dstSrc[srcY0:srcY0 + h, srcX0:srcX0 + w])
                    destPlate = styleTran(destPlate, srcPlate)
                    destPlate = cv2.resize(destPlate, (w, h))

                    replaceImgRegionBySpecImg(dstSrc, currentPoint[0], destPlate)  # 将源车牌的图像换成目标车牌图像
                    resultImgSrc = cv2.warpPerspective(dstSrc, srcM, (currentImg.shape[1], currentImg.shape[0]),
                                                       flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)
                    tempplate = np.array(resultImgSrc[srcY0:srcY0 + resRect[2], srcX0:srcX0 + resRect[1]])
                    replaceImgRegionBySpecImg(currentImg, resRect[0], tempplate)

                currentItemRes.append(currentImg)
        resultList.append(currentItemRes)
    return resultList
