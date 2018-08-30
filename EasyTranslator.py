# -*- coding: utf-8 -*-

from translator import googleTraslator
from translator import bingTranslator
from translator import baiduTranslator
from translator import jinshanTranslator
from translator import youdaoTranslator
from translator import cnkiTranslator
from translator import langdetect
from MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDesktopWidget, QAction
from PyQt5.QtCore import pyqtSignal, QFile
from PyQt5.QtGui import QIcon, QPixmap
from requests.exceptions import ConnectionError
import sys
import os
import time


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class EasyTranslator(QMainWindow):

    ui = Ui_MainWindow()
    count = 0
    trans = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.ui.setupUi(self)
        self.setWindowTitle('EasyTranslator')
        self.setWindowIcon(QIcon(resource_path('icon.png')))
        self.ui.label.setPixmap(QPixmap(resource_path('google.png')))
        self.ui.label_2.setPixmap(QPixmap(resource_path('baidu.png')))
        self.ui.label_3.setPixmap(QPixmap(resource_path('bing.png')))
        self.ui.label_4.setPixmap(QPixmap(resource_path('powerword.png')))
        self.ui.label_5.setPixmap(QPixmap(resource_path('youdao.png')))
        self.ui.label_6.setPixmap(QPixmap(resource_path('cnki.png')))
        aboutAct = QAction('关于', self)
        self.menuBar().addAction(aboutAct)
        self.loadStyleSheet(resource_path('white.qss'))
        self.resize( 820,650)
        self.center()

        self.ui.button_trans.clicked.connect(self.on_button_trans)
        self.ui.button_clear.clicked.connect(self.on_button_clear)
        self.trans.connect(self.googleTrans)
        self.trans.connect(self.baiduTrans)
        self.trans.connect(self.bingTrans)
        self.trans.connect(self.jinshanTrans)
        self.trans.connect(self.youdaoTrans)
        self.trans.connect(self.cnkiTrans)
        self.ui.button_goo.clicked.connect(self.on_button_goo)
        self.ui.button_bai.clicked.connect(self.on_button_bai)
        self.ui.button_bing.clicked.connect(self.on_button_bing)
        self.ui.button_jin.clicked.connect(self.on_button_jin)
        self.ui.button_you.clicked.connect(self.on_button_you)
        self.ui.button_zhi.clicked.connect(self.on_button_zhi)
        aboutAct.triggered.connect(self.on_aboutAction)

    def wait(self):
        self.ui.button_trans.setEnabled(False)
        self.ui.button_clear.setEnabled(False)
        self.ui.comboBox.setEnabled(False)
        self.ui.button_goo.setEnabled(False)
        self.ui.button_bai.setEnabled(False)
        self.ui.button_bing.setEnabled(False)
        self.ui.button_jin.setEnabled(False)
        self.ui.button_you.setEnabled(False)
        self.ui.button_zhi.setEnabled(False)

    def work(self):
        self.ui.button_trans.setEnabled(True)
        self.ui.button_clear.setEnabled(True)
        self.ui.comboBox.setEnabled(True)
        self.ui.button_goo.setEnabled(True)
        self.ui.button_bai.setEnabled(True)
        self.ui.button_bing.setEnabled(True)
        self.ui.button_jin.setEnabled(True)
        self.ui.button_you.setEnabled(True)
        self.ui.button_zhi.setEnabled(True)

    def on_button_trans(self):
        self.count = 0
        text = self.ui.textEdit_in.toPlainText()
        if text == '':
            print('no input')
            return
        # time.sleep(10)
        ind = self.ui.comboBox.currentIndex()
        self.wait()
        QApplication.processEvents()
        if ind == 0:
            try:
                direct = langdetect(text)
            except ConnectionError as e:
                # print(e)
                QMessageBox.information(self, '警告', '网络连接错误，自动语言检测失败！')
                self.work()
                return
            if direct is None:
                QMessageBox.information(self, '警告', '自动语言检测失败，请尝试手动！')
                self.work()
                return
        else:
            direct = ind - 1
        self.trans.emit(text, direct)

        # print(text)
        # ind = self.ui.comboBox.currentIndex()
        # if ind == 0:
        #     direct = langdetect(text)
        # else:
        #     direct = ind - 1
        # r1 = googleTraslator(text, direct)
        # r2 = baiduTranslator(text, direct)
        # r3 = bingTranslator(text, direct)
        # r4 = jinshanTranslator(text, direct)
        # r5 = youdaoTranslator(text, direct)
        # r6 = cnkiTranslator(text, direct)
        # self.ui.textEdit_goo.setText(r1)
        # self.ui.textEdit_bai.setText(r2)
        # self.ui.textEdit_bing.setText(r3)
        # self.ui.textEdit_jin.setText(r4)
        # self.ui.textEdit_you.setText(r5)
        # self.ui.textEdit_zhi.setText(str(r6))

    def googleTrans(self, text, direct):
        try:
            r = googleTraslator(text, direct)
        except ConnectionError as e:
            self.ui.textEdit_goo.setText('网络连接错误，Google翻译失败！')
        else:
            self.ui.textEdit_goo.setText(r)
        self.count += 1
        if self.count == 6:
            self.work()

    def baiduTrans(self, text, direct):
        try:
            r = baiduTranslator(text, direct)
        except ConnectionError as e:
            self.ui.textEdit_bai.setText('网络连接错误，百度翻译失败！')
        else:
            self.ui.textEdit_bai.setText(r)
        self.count += 1
        if self.count == 6:
            self.work()

    def bingTrans(self, text, direct):
        try:
            r = bingTranslator(text, direct)
        except ConnectionError as e:
            self.ui.textEdit_bing.setText('网络连接错误，必应翻译失败！')
        else:
            self.ui.textEdit_bing.setText(r)
        self.count += 1
        if self.count == 6:
            self.work()

    def jinshanTrans(self, text, direct):
        try:
            r = jinshanTranslator(text, direct)
        except ConnectionError as e:
            self.ui.textEdit_jin.setText('网络连接错误，金山翻译失败！')
        else:
            self.ui.textEdit_jin.setText(r)
        self.count += 1
        if self.count == 6:
            self.work()

    def youdaoTrans(self, text, direct):
        try:
            r = youdaoTranslator(text, direct)
        except ConnectionError as e:
            self.ui.textEdit_you.setText('网络连接错误，有道翻译失败！')
        else:
            self.ui.textEdit_you.setText(r)
        self.count += 1
        if self.count == 6:
            self.work()

    def cnkiTrans(self, text, direct):
        try:
            r = cnkiTranslator(text, direct)
        except ConnectionError as e:
            self.ui.textEdit_zhi.setText('网络连接错误，知网翻译失败！')
        else:
            self.ui.textEdit_zhi.setText(str(r))
        self.count += 1
        if self.count == 6:
            self.work()

    def on_button_clear(self):
        self.ui.textEdit_in.clear()

    def on_button_goo(self):
        QApplication.clipboard().setText(self.ui.textEdit_goo.toPlainText())

    def on_button_bai(self):
        QApplication.clipboard().setText(self.ui.textEdit_bai.toPlainText())


    def on_button_bing(self):
        QApplication.clipboard().setText(self.ui.textEdit_bing.toPlainText())

    def on_button_jin(self):
        QApplication.clipboard().setText(self.ui.textEdit_jin.toPlainText())

    def on_button_you(self):
        QApplication.clipboard().setText(self.ui.textEdit_you.toPlainText())

    def on_button_zhi(self):
        QApplication.clipboard().setText(self.ui.textEdit_zhi.toPlainText())

    def loadStyleSheet(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            s = f.readlines()
            s = ''.join(s).strip('\n')
        self.setStyleSheet(s)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.setGeometry(qr)

    def on_aboutAction(self):
        QMessageBox.information(self, 'About', 'EasyTranslator version 1.0\nDeveloped by Daibingh')