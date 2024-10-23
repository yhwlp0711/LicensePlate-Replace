# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainMenu.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!
import os

import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QListWidgetItem, QListView

import gb
from creatPlate.generate_special_plate import creatPlate
from replace import changePlate


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1059, 771)
        Form.setMinimumSize(QtCore.QSize(755, 555))
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 1031, 730))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.line_6 = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_4.addWidget(self.line_6)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.line_5 = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.line_5)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEditSrcPath = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEditSrcPath.setObjectName("lineEditSrcPath")
        self.horizontalLayout.addWidget(self.lineEditSrcPath)
        self.pushButtonSrcOk = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonSrcOk.setObjectName("pushButtonSrcOk")
        self.horizontalLayout.addWidget(self.pushButtonSrcOk)
        self.pushButtonSrcChooseDir = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonSrcChooseDir.setObjectName("pushButtonSrcChooseDir")
        self.horizontalLayout.addWidget(self.pushButtonSrcChooseDir)
        self.pushButtonSrcChooseFile = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonSrcChooseFile.setObjectName("pushButtonSrcChooseFile")
        self.horizontalLayout.addWidget(self.pushButtonSrcChooseFile)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidgetSrcImgs = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        self.listWidgetSrcImgs.setMinimumSize(QtCore.QSize(488, 315))
        self.listWidgetSrcImgs.setMaximumSize(QtCore.QSize(488, 315))
        self.listWidgetSrcImgs.setViewMode(QListView.IconMode)
        self.listWidgetSrcImgs.setResizeMode(QListView.Adjust)
        self.listWidgetSrcImgs.setIconSize(QSize(100, 100))
        self.listWidgetSrcImgs.setMovement(QListView.Static)

        self.listWidgetSrcImgs.setObjectName("listWidgetSrcImgs")
        self.verticalLayout.addWidget(self.listWidgetSrcImgs)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.verticalLayout)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEditDstPath = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEditDstPath.setObjectName("lineEditDstPath")
        self.horizontalLayout_2.addWidget(self.lineEditDstPath)
        self.pushButtonDstOk = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonDstOk.setObjectName("pushButtonDstOk")
        self.horizontalLayout_2.addWidget(self.pushButtonDstOk)
        self.pushButtonDstChoose = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonDstChoose.setObjectName("pushButtonDstChoose")
        self.horizontalLayout_2.addWidget(self.pushButtonDstChoose)
        self.pushButtonDstCreat = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonDstCreat.setObjectName("pushButtonDstCreat")
        self.horizontalLayout_2.addWidget(self.pushButtonDstCreat)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.labelDstImg = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.labelDstImg.setEnabled(True)
        self.labelDstImg.setMinimumSize(QtCore.QSize(488, 315))
        self.labelDstImg.setMaximumSize(QtCore.QSize(488, 315))
        self.labelDstImg.setText("")
        self.labelDstImg.setObjectName("labelDstImg")
        self.verticalLayout_7.addWidget(self.labelDstImg)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.verticalLayout_7)
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.line)
        self.horizontalLayout_4.addLayout(self.formLayout)
        self.line_3 = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_4.addWidget(self.line_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.line_8 = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_4.addWidget(self.line_8)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEditResPath = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEditResPath.setObjectName("lineEditResPath")
        self.horizontalLayout_3.addWidget(self.lineEditResPath)
        self.pushButtonStartReplace = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonStartReplace.setObjectName("pushButtonStartReplace")
        self.horizontalLayout_3.addWidget(self.pushButtonStartReplace)
        self.pushButtonResChoose = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonResChoose.setObjectName("pushButtonResChoose")
        self.horizontalLayout_3.addWidget(self.pushButtonResChoose)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.listWidgetResImgs = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        self.listWidgetResImgs.setObjectName("listWidgetResImgs")
        self.listWidgetResImgs.setViewMode(QListView.IconMode)
        self.listWidgetResImgs.setResizeMode(QListView.Adjust)
        self.listWidgetResImgs.setIconSize(QSize(100, 100))
        self.listWidgetResImgs.setMovement(QListView.Static)

        self.verticalLayout_4.addWidget(self.listWidgetResImgs)
        self.line_9 = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.verticalLayout_4.addWidget(self.line_9)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.line_7 = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout_4.addWidget(self.line_7)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButtonSrcOk.setText(_translate("Form", "确认"))
        self.pushButtonSrcChooseDir.setText(_translate("Form", "选择目录"))
        self.pushButtonSrcChooseFile.setText(_translate("Form", "选择文件"))
        self.pushButtonDstOk.setText(_translate("Form", "确认"))
        self.pushButtonDstChoose.setText(_translate("Form", "选择路径"))
        self.pushButtonDstCreat.setText(_translate("Form", "创建车牌"))
        self.pushButtonStartReplace.setText(_translate("Form", "开始替换"))
        self.pushButtonResChoose.setText(_translate("Form", "选择路径"))



class MainWidget(QtWidgets.QWidget):

    flag = 1

    def __init__(self):
        super(MainWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButtonSrcOk.clicked.connect(self.srcImgsPath)
        self.ui.pushButtonSrcChooseDir.clicked.connect(self.srcChooseDir)
        self.ui.pushButtonSrcChooseFile.clicked.connect(self.srcChooseFile)
        self.ui.pushButtonDstOk.clicked.connect(self.dstImgPath)
        self.ui.pushButtonDstChoose.clicked.connect(self.dstChooseFile)
        self.ui.pushButtonDstCreat.clicked.connect(self.creatNewPlate)
        self.ui.pushButtonResChoose.clicked.connect(self.resChooseDir)
        self.ui.pushButtonStartReplace.clicked.connect(self.startReplace)



    def srcImgsPath(self):
        imgPath = self.ui.lineEditSrcPath.text()
        self.ui.listWidgetSrcImgs.clear()
        if len(imgPath) == 0:
            QMessageBox.information(self, "通知", "请输入路径!", QMessageBox.Yes)
        else:
            gb.srcImgs.clear()
            gb.srcPaths.clear()
            gb.srcImgs, gb.srcPaths = gb.readImg(imgPath)
            if gb.srcImgs is None:
                QMessageBox.information(self, "通知", "选择的路径中没有图片或视频!", QMessageBox.Yes)
            else:
                if len(gb.srcPaths) == 0:
                    pItem = QListWidgetItem()
                    pItem.setIcon(QIcon(imgPath))
                    pItem.setText(imgPath)
                    pItem.setSizeHint(QSize(100, 100))
                    self.ui.listWidgetSrcImgs.addItem(pItem)
                else:
                    for path in gb.srcPaths:
                        pItem = QListWidgetItem()
                        pItem.setIcon(QIcon(imgPath + '/' + path))
                        pItem.setText(path)
                        pItem.setSizeHint(QSize(100, 100))
                        self.ui.listWidgetSrcImgs.addItem(pItem)

    def srcChooseDir(self):
        self.ui.listWidgetSrcImgs.clear()
        imgPath = QFileDialog.getExistingDirectory(self, "选择目录", "./", QFileDialog.ShowDirsOnly)
        if len(imgPath) != 0:
            self.ui.lineEditSrcPath.setText(imgPath)
            gb.srcImgs.clear()
            gb.srcPaths.clear()
            gb.srcImgs, gb.srcPaths = gb.readImg(imgPath)
            if gb.srcImgs is None:
                QMessageBox.information(self, "通知", "选择的路径中没有图片或视频!", QMessageBox.Yes)
            else:
                if len(gb.srcPaths) == 0:
                    pItem = QListWidgetItem()
                    pItem.setIcon(QIcon(imgPath))
                    pItem.setText(imgPath)
                    pItem.setSizeHint(QSize(100, 100))
                    self.ui.listWidgetSrcImgs.addItem(pItem)
                else:
                    for path in gb.srcPaths:
                        pItem = QListWidgetItem()
                        pItem.setIcon(QIcon(imgPath + '/' + path))
                        pItem.setText(path)
                        pItem.setSizeHint(QSize(100, 100))
                        self.ui.listWidgetSrcImgs.addItem(pItem)

    def srcChooseFile(self):
        self.ui.listWidgetSrcImgs.clear()
        imgPath = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                                   "(*.jpg *.png *.bmp *.tif *.jepg *.mp4 *.avi)")[0]
        if len(imgPath) != 0:
            self.ui.lineEditSrcPath.setText(imgPath)
            gb.srcImgs.clear()
            gb.srcPaths.clear()
            gb.srcImgs, gb.srcPaths = gb.readImg(imgPath)
            if gb.srcImgs is None:
                QMessageBox.information(self, "通知", "选择的路径中没有图片或视频!", QMessageBox.Yes)
            else:
                if len(gb.srcPaths) == 0:
                    pItem = QListWidgetItem()
                    pItem.setIcon(QIcon(imgPath))
                    _, filename = os.path.split(imgPath)
                    pItem.setText(filename)
                    pItem.setSizeHint(QSize(100, 100))
                    self.ui.listWidgetSrcImgs.addItem(pItem)
                else:
                    for path in gb.srcPaths:
                        pItem = QListWidgetItem()
                        pItem.setIcon(QIcon(imgPath + '/' + path))
                        pItem.setText(path)
                        pItem.setSizeHint(QSize(100, 100))
                        self.ui.listWidgetSrcImgs.addItem(pItem)

    def dstImgPath(self):
        imgPath = self.ui.lineEditDstPath.text()
        if len(imgPath) == 0:
            QMessageBox.information(self, "通知", "请输入路径!", QMessageBox.Yes)
        else:
            gb.dstImg.clear()
            gb.dstPath = ""
            gb.dstImg, gb.dstPath = gb.readImg(imgPath)
            if gb.dstImg is None:
                QMessageBox.information(self, "通知", "选择的路径中没有图片或视频!", QMessageBox.Yes)
            else:
                pixmap = QPixmap()
                pixmap.load(imgPath)
                pixmap = pixmap.scaled(self.ui.labelDstImg.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.ui.labelDstImg.setPixmap(pixmap)

    def dstChooseFile(self):
        imgPath = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                              "(*.jpg *.png *.bmp *.tif *.jepg)")[0]
        if len(imgPath) != 0:
            self.ui.lineEditDstPath.setText(imgPath)
            gb.dstImg.clear()
            gb.dstPath = ""
            gb.dstImg, gb.dstPath = gb.readImg(imgPath)
            if gb.dstImg is None:
                QMessageBox.information(self, "通知", "选择的路径中没有图片或视频!", QMessageBox.Yes)
            else:
                pixmap = QPixmap()
                pixmap.load(imgPath)
                pixmap = pixmap.scaled(self.ui.labelDstImg.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.ui.labelDstImg.setPixmap(pixmap)

    def creatNewPlate(self):
        self.flag = 0
        plateNum = self.ui.lineEditDstPath.text()
        if len(plateNum) == 0:
            QMessageBox.information(self, "通知", "请输入车牌!", QMessageBox.Yes)
        else:
            gb.dstPath = 'plate.jpg'
            gb.dstImg.clear()
            gb.dstImg = creatPlate(plateNum)
            if gb.dstImg is None:
                QMessageBox.information(self, "通知", "生成车牌失败!", QMessageBox.Yes)
            else:
                pixmap = QPixmap()
                pixmap.load(gb.dstPath)
                pixmap = pixmap.scaled(self.ui.labelDstImg.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.ui.labelDstImg.setPixmap(pixmap)

    def resChooseDir(self):
        imgPath = QFileDialog.getExistingDirectory(self, "选择目录", "./", QFileDialog.ShowDirsOnly)
        if len(imgPath) != 0:
            self.ui.lineEditResPath.setText(imgPath)

    def startReplace(self):
        respath = self.ui.lineEditResPath.text()
        eachpath = list()
        if len(gb.srcImgs) == 0 or len(gb.dstImg) == 0:
            QMessageBox.information(self, "通知", "请选择文件!", QMessageBox.Yes)
        else:
            resImgs = changePlate(gb.srcImgs, gb.dstImg, self.flag)
            for imgs in resImgs:
                k = 0
                if imgs[0] == 0:
                    for i in range(len(imgs) - 1):
                        cv2.imwrite(respath + '/' + str(i+1) + '.jpg', imgs[i+1])
                        eachpath.append(str(i+1) + '.jpg')
                else:
                    gb.saveVideo(respath + '/' + str(k+1) + '.mp4', imgs[1:], gb.FPScount[k])
                    eachpath.append(str(k + 1) + '.mp4')
                    k += 1

            for path in eachpath:
                pItem = QListWidgetItem()
                pItem.setIcon(QIcon(respath + '/' + path))
                pItem.setText(path)
                pItem.setSizeHint(QSize(100, 100))
                self.ui.listWidgetResImgs.addItem(pItem)




