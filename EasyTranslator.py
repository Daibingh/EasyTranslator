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
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QPixmap
from requests.exceptions import ConnectionError
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Work_1(QThread):

    done = pyqtSignal()

    def __init__(self, text):
        QThread.__init__(self)
        self.text = text

    def run(self):
        try:
            self.direct = langdetect(self.text)
        except ConnectionError as e:
            self.direct = -1
            print('网络连接错误，检测语言失败！')
        except Exception as e:
            self.e = e
            self.direct = -2
            print(e, '检测语言失败！')
        self.done.emit()


class Work_2(QThread):

    done = pyqtSignal(str, str)

    def __init__(self, text, direct, fun_handle):
        QThread.__init__(self)
        self.text = text
        self.direct = direct
        self.fun_handle = fun_handle

    def run(self):
        try:
            self.result = self.fun_handle(self.text, self.direct)
        except ConnectionError as e:
            self.result = -1
            print('网络连接错误，'+self.fun_handle.__name__+'翻译失败！')
        except Exception as e:
            self.e = e
            self.result = -2
            print('e, ' + self.fun_handle.__name__ + '翻译失败！')
        self.done.emit(self.fun_handle.__name__, str(self.result))


class EasyTranslator(QMainWindow):

    ui = Ui_MainWindow()
    count = 0
    trans = pyqtSignal(str, int)
    work_1 = Work_1('')
    work_2s = []
    text = ''
    direct = 0
    work_2s.append(Work_2(text, direct, googleTraslator))
    work_2s.append(Work_2(text, direct, baiduTranslator))
    work_2s.append(Work_2(text, direct, bingTranslator))
    work_2s.append(Work_2(text, direct, jinshanTranslator))
    work_2s.append(Work_2(text, direct, youdaoTranslator))
    work_2s.append(Work_2(text, direct, cnkiTranslator))

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
        self.trans.connect(self.transapi)
        # self.trans.connect(self.baiduTrans)
        # self.trans.connect(self.bingTrans)
        # self.trans.connect(self.jinshanTrans)
        # self.trans.connect(self.youdaoTrans)
        # self.trans.connect(self.cnkiTrans)
        self.ui.button_goo.clicked.connect(self.on_button_goo)
        self.ui.button_bai.clicked.connect(self.on_button_bai)
        self.ui.button_bing.clicked.connect(self.on_button_bing)
        self.ui.button_jin.clicked.connect(self.on_button_jin)
        self.ui.button_you.clicked.connect(self.on_button_you)
        self.ui.button_zhi.clicked.connect(self.on_button_zhi)
        aboutAct.triggered.connect(self.on_aboutAction)
        self.work_1.done.connect(self.landet)
        for work_2 in self.work_2s:
            work_2.done.connect(self.disp)

    def disp(self, fun_name, result):
        if fun_name == 'googleTraslator':
            if result == '-1':
                self.ui.textEdit_goo.setText('网络连接错误，'+fun_name+'翻译失败！')
            elif result == '-2':
                self.ui.textEdit_goo.setText(str(self.work_2s[0].e) + '，' + fun_name + '翻译失败！')
            else:
                self.ui.textEdit_goo.setText(result)
        elif fun_name == 'baiduTranslator':
            if result == '-1':
                self.ui.textEdit_bai.setText('网络连接错误，'+fun_name+'翻译失败！')
            elif result == '-2':
                self.ui.textEdit_bai.setText(str(self.work_2s[1].e) + '，' + fun_name + '翻译失败！')
            else:
                self.ui.textEdit_bai.setText(result)
        elif fun_name == 'bingTranslator':
            if result == '-1':
                self.ui.textEdit_bing.setText('网络连接错误，' + fun_name + '翻译失败！')
            elif result == '-2':
                self.ui.textEdit_bing.setText(str(self.work_2s[2].e) + '，' + fun_name + '翻译失败！')
            else:
                self.ui.textEdit_bing.setText(result)
        elif fun_name == 'jinshanTranslator':
            if result == '-1':
                self.ui.textEdit_jin.setText('网络连接错误，' + fun_name + '翻译失败！')
            elif result == '-2':
                self.ui.textEdit_jin.setText(str(self.work_2s[3].e) + '，' + fun_name + '翻译失败！')
            else:
                self.ui.textEdit_jin.setText(result)
        elif fun_name == 'youdaoTranslator':
            if result == '-1':
                self.ui.textEdit_you.setText('网络连接错误，' + fun_name + '翻译失败！')
            elif result == '-2':
                self.ui.textEdit_you.setText(str(self.work_2s[4].e) + '，' + fun_name + '翻译失败！')
            else:
                self.ui.textEdit_you.setText(result)
        else:
            if result == '-1':
                self.ui.textEdit_zhi.setText('网络连接错误，' + fun_name + '翻译失败！')
            elif result == '-2':
                self.ui.textEdit_zhi.setText(str(self.work_2s[5].e) + '，' + fun_name + '翻译失败！')
            else:
                self.ui.textEdit_zhi.setText(result)
        self.count += 1
        if self.count == 6:
            self.work()
            self.count = 0

    def transapi(self, text, direct):
        # self.work_2s.append(Work_2(text, direct, googleTraslator))
        # self.work_2s.append(Work_2(text, direct, bingTranslator))
        # self.work_2s.append(Work_2(text, direct, jinshanTranslator))
        # self.work_2s.append(Work_2(text, direct, youdaoTranslator))
        # self.work_2s.append(Work_2(text, direct, cnkiTranslator))
        transfuns = [googleTraslator, baiduTranslator, bingTranslator, jinshanTranslator, youdaoTranslator, cnkiTranslator]
        i = 0
        for work_2 in self.work_2s:
            work_2.text = text
            work_2.direct =direct
            work_2.fun_handle = transfuns[i]
            i += 1
            work_2.start()


    def landet(self):
        # self.ui.textEdit_goo.setPlainText(str(self.work_1.direct))
        if self.work_1.direct == -1:
            QMessageBox.information(self, '错误', '网络连接错误，检测语言失败！')
            self.work()
        elif self.work_1.direct == -2:
            QMessageBox.information(self, '错误', str(self.work_1.e) + '，检测语言失败！')
            self.work()
        else:
            self.trans.emit(self.text, self.work_1.direct)

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
        self.text = text
        if text == '':
            print('no input')
            return
        ind = self.ui.comboBox.currentIndex()
        self.wait()
        if ind == 0:
            self.work_1.text = text
            self.work_1.start()
            return
        else:
            direct = ind - 1
            self.trans.emit(text, direct)
            return

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

    # def googleTrans(self, text, direct):
    #     try:
    #         r = googleTraslator(text, direct)
    #     except ConnectionError as e:
    #         self.ui.textEdit_goo.setText('网络连接错误，Google翻译失败！')
    #     else:
    #         self.ui.textEdit_goo.setText(r)
    #     self.count += 1
    #     if self.count == 6:
    #         self.work()
    #
    # def baiduTrans(self, text, direct):
    #     try:
    #         r = baiduTranslator(text, direct)
    #     except ConnectionError as e:
    #         self.ui.textEdit_bai.setText('网络连接错误，百度翻译失败！')
    #     else:
    #         self.ui.textEdit_bai.setText(r)
    #     self.count += 1
    #     if self.count == 6:
    #         self.work()
    #
    # def bingTrans(self, text, direct):
    #     try:
    #         r = bingTranslator(text, direct)
    #     except ConnectionError as e:
    #         self.ui.textEdit_bing.setText('网络连接错误，必应翻译失败！')
    #     else:
    #         self.ui.textEdit_bing.setText(r)
    #     self.count += 1
    #     if self.count == 6:
    #         self.work()
    #
    # def jinshanTrans(self, text, direct):
    #     try:
    #         r = jinshanTranslator(text, direct)
    #     except ConnectionError as e:
    #         self.ui.textEdit_jin.setText('网络连接错误，金山翻译失败！')
    #     else:
    #         self.ui.textEdit_jin.setText(r)
    #     self.count += 1
    #     if self.count == 6:
    #         self.work()
    #
    # def youdaoTrans(self, text, direct):
    #     try:
    #         r = youdaoTranslator(text, direct)
    #     except ConnectionError as e:
    #         self.ui.textEdit_you.setText('网络连接错误，有道翻译失败！')
    #     else:
    #         self.ui.textEdit_you.setText(r)
    #     self.count += 1
    #     if self.count == 6:
    #         self.work()
    #
    # def cnkiTrans(self, text, direct):
    #     try:
    #         r = cnkiTranslator(text, direct)
    #     except ConnectionError as e:
    #         self.ui.textEdit_zhi.setText('网络连接错误，知网翻译失败！')
    #     else:
    #         self.ui.textEdit_zhi.setText(str(r))
    #     self.count += 1
    #     if self.count == 6:
    #         self.work()

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