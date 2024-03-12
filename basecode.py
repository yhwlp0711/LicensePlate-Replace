import traceback
from math import pi, cos, sin, tan

import cv2
import numpy as np


def  overlyImgs(bottomImg,topImg,blackMaxVal=0):
    """
    将两个图叠加，叠加时上层图非透明部分遮挡下层图对应部分，上层图透明部分则不遮挡下层图
    blackMaxVal:灰度值小于等于该值的都作为透明黑色处理，如果是彩色图像则以彩色转灰度后的值作为比较
    """
    if bottomImg.shape[:2]!=topImg.shape[:2]:
        errInf = f"bottomImg和topImg图像对应大小不同：\n" + traceback.format_exc()
        raise ValueError(errInf)
    topImgGray = cv2.cvtColor(topImg, cv2.COLOR_BGR2GRAY) #将上层剪辑帧图像转成灰度图
    retval, imgMask = cv2.threshold(topImgGray, blackMaxVal, 255, type=cv2.THRESH_BINARY) #将灰度图二值化作为掩膜


    maskInv = cv2.bitwise_not(imgMask) #上层剪辑掩膜求反，用于获取底层剪辑需要显示内容
    result = cv2.bitwise_and(topImg, topImg, mask=imgMask) + cv2.bitwise_and(bottomImg, bottomImg, mask=maskInv)

    return result

def replaceImgBySpecImgRefPoint(largeImg,largeImgRefPoint,smallImg,smallImgRefPoint,overlyBlackMaxValue=None):
    """
    - 将一个小图像的内容copy到大图像中，要求小图像的smallImgRefPoint对应点和大图像的largeImgRefPoint对应点重合。
    - largeImgRefPoint/smallImgRefPoint都是（X,Y)形式，其值都是对应点在自身图像的位置。
    - overlyBlackMaxValue：为None表示大图像对应区域用小图像简单替代，否则根据smallImg是否有对应灰度值小于overlyBlackMaxValue的像素，  如果有结果图像中这部分像素则保持大图部分的像素不变，其他部分则使用小图对应像素替代
     - 返回已经copy或融合小图像的大图像
    """
    #largeImg = np.array(largImg)
    if len(largeImg.shape)==3:
        lh,lw,lc = largeImg.shape
    else:
        lh, lw = largeImg.shape
        lc = 1
    if len(smallImg.shape)==3:
        sh,sw,sc = smallImg.shape
    else:
        sh, sw = smallImg.shape
        sc = 1
    if sc!=lc:
        raise ValueError('largeImg和smallImg通道数不同'+ traceback.format_exc())
    if lh<sh or lw<sw:
        raise ValueError( 'largeImg图像的高度和宽度都不能小于smallImg图像的高度和宽度'+ traceback.format_exc())
    lx,ly = largeImgRefPoint
    sx,sy = smallImgRefPoint
    lx -= sx
    ly -= sy
    lx2 = lx+sw
    ly2 = ly+sh
    if lx<0 or ly<0 or lx2>lw or ly2>lh:
        raise ValueError(f'largeImg图像对应参考点{largeImgRefPoint}和smallImg图像对应参考点{smallImgRefPoint}重叠时smallImg图像超出了largeImg图像范围')
    if overlyBlackMaxValue is None:
        largeImg[ly:ly2, lx:lx2] = smallImg
    else:
        largeImg[ly:ly2, lx:lx2] = overlyImgs(largeImg[ly:ly2, lx:lx2],smallImg,overlyBlackMaxValue)
    return largeImg


def replaceImgRegionBySpecImg(srcImg, regionTopLeftPos, specImg,overlyBlackMaxValue=None):
    """将srcImg的regionTopLeftPos开始位置的一个矩形图像替换为specImg
      overlyBlackMaxValue: 为None表示大图像对应区域用小图像简单替代，否则根据smallImg是否有对应灰度值小于overlyBlackMaxValue的像素，  如果有结果图像中这部分像素则保持大图部分的像素不变，其他部分则使用小图对应像素替代
     返回已经copy或融合小图像的大图像"""
    return replaceImgBySpecImgRefPoint(srcImg,regionTopLeftPos,specImg,(0,0),overlyBlackMaxValue)


def constructRectFrom4Points(pointList):
    """
    依据一个四边形构建一个和坐标轴平行的矩形，构建原则是取四边形左上角的点为矩形的左上角点，四边形上边和下边x、y坐标的最大差距作为矩形横边的边长，以及侧边的边长
    :param pointList: 四边形的四个点，分别为左上、右上、左下、右下
    :return: 构成成功则返回矩形的左上角坐标、横边和侧边的边长
    """
    if len(pointList) < 4:
        print("从四边形创建矩形需要4个点")
        return None

    lu, ru, ld, rd = pointList[:4]
    # ueX = ru[0] - lu[0]  # 上边X坐标差
    # deX = rd[0] - ld[0]  # 下边X坐标差
    # leY = ld[1] - lu[1]  # 上边X坐标差
    # reY = rd[1] - ru[1]  # 下边X坐标差

    ueX = ru[0] - lu[0]  # 上边X坐标差
    udeX = ru[0] - ld[0]
    dueX = rd[0] - lu[0]
    deX = rd[0] - ld[0]  # 下边X坐标差


    leY = ld[1] - lu[1]  # 上边Y坐标差
    lreY = ld[1] - ru[1]
    rleY = rd[1] - lu[1]
    reY = rd[1] - ru[1]  # 下边Y坐标差

    if lu[0] > ld[0]:
        lu = (ld[0], lu[1])

    if lu[1] > ru[1]:
        lu = (lu[0], ru[1])

    x = max(ueX, deX, udeX, dueX)
    y = max(leY, reY, lreY, rleY)
    return lu, x, y


# def xyxy2pxy(xyxy):
#     lu = xyxy[0], xyxy[1]
#     x = xyxy[2] - xyxy[0]
#     y = xyxy[3] -xyxy[1]
#     return lu, x, y


def constructAffineMatrix(rotationAngle=0,xShearAngle=0,yShearAngle=0,translationX=0,translationY=0,scaleX=1,scaleY=1):
    """
    :param rotationAngle: 旋转角度，图像旋转时使用，逆时钟为正、顺时针为负，如顺时针旋转30°，则值为-30
    :param xShearAngle: 水平错切角，水平错切时使用
    :param yShearAngle: 垂直错切角，垂直错切时使用
    :param translationX: x轴平移距离
    :param translationY: y轴平移距离
    :param scaleX: 水平方向缩放因子
    :param scaleY: 竖直方向缩放因子
    :param bTMT: 是否返回3*3矩阵，为False返回2*3矩阵，为True返回3*3矩阵，默认值为False
    :return: 构建的3*3矩阵
    补充说明：
    本函数只能构建旋转、错切、平移、缩放四种情况的一种矩阵，参数只取一种情况进行矩阵构造，
    取的情况按照旋转、错切、平移、缩放从高到低的优先级排列，高优先级的值非0则低优先级的值忽略。
    如果返回的矩阵为3*3矩阵，如果该矩阵立即调用warpAffine进行仿射变换，需要通过切片方式取前2行传入warpAffine，如果需要与其他仿射矩阵相乘，
    则必须保持3*3矩阵，相乘的结果再进行切片处理，因为两个2*3的矩阵之间没法相乘（矩阵乘法要求第一个矩阵的列数等于第二个矩阵的行数）
    """
    if rotationAngle:
        rotationAngle = pi*rotationAngle/180
        return np.float32([[cos(rotationAngle), -sin(rotationAngle), 0], [sin(rotationAngle), cos(rotationAngle), 0],[0,0,1]])
    elif xShearAngle:
        xShearAngle = pi*xShearAngle/180
        return np.float32([[1,tan(xShearAngle),0], [0, 1, 0],[0,0,1]])
    elif yShearAngle:
        yShearAngle = pi*yShearAngle/180
        return np.float32([[1, 0, 0], [tan(yShearAngle), 1, 0],[0,0,1]])
    elif translationX or translationY:
        return np.float32([[1, 0, translationX], [0, 1, translationY],[0,0,1]])
    else:return np.float32([[scaleX, 0, 0], [0, scaleY, 0],[0,0,1]])


def translation(img,x,y,size):
    m = constructAffineMatrix(translationX=x,translationY=y)
    w,h = size
    if w%2: w += 1
    if h % 2: h += 1

    img = cv2.warpAffine(img, m[0:2], (w,h))
    return img