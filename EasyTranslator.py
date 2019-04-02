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
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import QObject
from requests.exceptions import ConnectionError
import sys
import os
import sources


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Work(QThread):

    def __init__(self, fun_handle):
        super().__init__()
        self.text = ''
        self.flg = 0
        self.fun_handle = fun_handle
        self.result = ''

    def run(self):
        try:
            self.result = self.fun_handle(self.text, self.flg)
        except Exception as e:
            self.result = 'error!'
        # print(self.result)


class Loader(QObject):

    done = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.works = []
        funs = [googleTraslator, baiduTranslator, bingTranslator, jinshanTranslator, youdaoTranslator, cnkiTranslator]
        for fun in funs:
            self.works.append(Work(fun))

    def load_threads(self, index, text):
        if text == '':
            print('no input')
            self.done.emit()
            return

        if index == 0:  # 自动检测语言
            lan_type = langdetect(text)  # lan_type 0: zh; 1: en
        else:  # 否则，采用选用的语言
            lan_type = index - 1

        for work in self.works:
            work.text = text
            work.flg = lan_type
            work.start()

        for work in self.works:
            work.wait()
            # print(work.result)
        self.done.emit()

class EasyTranslator(QMainWindow, Ui_MainWindow):

    launch = pyqtSignal(int, str)

    def __init__(self):

        super().__init__()
        self.setupUi(self)
        self.textEdit_bai.setFontPointSize(12)
        self.textEdit_bing.setFontPointSize(12)
        self.textEdit_goo.setFontPointSize(12)
        self.textEdit_jin.setFontPointSize(12)
        self.textEdit_you.setFontPointSize(12)
        self.textEdit_zhi.setFontPointSize(12)

        self.setWindowTitle('EasyTranslator')
        self.setWindowIcon(QIcon(resource_path('icon.png')))
        self.label.setPixmap(QPixmap(resource_path('google.png')))
        self.label_2.setPixmap(QPixmap(resource_path('baidu.png')))
        self.label_3.setPixmap(QPixmap(resource_path('bing.png')))
        self.label_4.setPixmap(QPixmap(resource_path('powerword.png')))
        self.label_5.setPixmap(QPixmap(resource_path('youdao.png')))
        self.label_6.setPixmap(QPixmap(resource_path('cnki.png')))
        self.checkBox_bai.setCheckState(2)
        self.checkBox_goo.setCheckState(2)
        self.checkBox_bing.setCheckState(2)
        self.checkBox_you.setCheckState(2)
        self.checkBox_zhi.setCheckState(2)
        self.checkBox_jin.setCheckState(2)
        self.aboutAct = QAction('Version', self)
        self.aboutMenu = self.menuBar().addMenu("About")
        self.aboutMenu.addAction(self.aboutAct)
        self.loadStyleSheet(resource_path('dark.qss'))
        self.resize(860, 650)
        self.center()

        self.loader = Loader()
        self.thread = QThread()
        self.loader.moveToThread(self.thread)
        self.textEdit_objs = [self.textEdit_goo, self.textEdit_bai, self.textEdit_bing, self.textEdit_jin, self.textEdit_you, self.textEdit_zhi]

        self.thread.finished.connect(self.loader.deleteLater)
        self.button_trans.clicked.connect(self.on_button_trans)
        self.launch.connect(self.loader.load_threads)
        self.loader.done.connect(self.show_result)
        self.button_clear.clicked.connect(self.on_button_clear)
        self.button_goo.clicked.connect(self.on_button_goo)
        self.button_bai.clicked.connect(self.on_button_bai)
        self.button_bing.clicked.connect(self.on_button_bing)
        self.button_jin.clicked.connect(self.on_button_jin)
        self.button_you.clicked.connect(self.on_button_you)
        self.button_zhi.clicked.connect(self.on_button_zhi)
        self.aboutAct.triggered.connect(self.on_aboutAction)

        self.thread.start()

    def closeEvent(self, event):
        self.thread.quit()
        self.thread.wait()
        event.accept()  # let the window close

    def on_button_goo(self):
        QApplication.clipboard().setText(self.textEdit_goo.toPlainText())

    def on_button_bai(self):
        QApplication.clipboard().setText(self.textEdit_bai.toPlainText())


    def on_button_bing(self):
        QApplication.clipboard().setText(self.textEdit_bing.toPlainText())

    def on_button_jin(self):
        QApplication.clipboard().setText(self.textEdit_jin.toPlainText())

    def on_button_you(self):
        QApplication.clipboard().setText(self.textEdit_you.toPlainText())

    def on_button_zhi(self):
        QApplication.clipboard().setText(self.textEdit_zhi.toPlainText())

    def on_button_clear(self):
        self.textEdit_in.clear()

    def show_result(self):
        # for i, work in enumerate(self.loader.works):
        if self.textEdit_in.toPlainText() != '':
            for obj, work in zip(self.textEdit_objs, self.loader.works):
                obj.setText(str(work.result))

        self.enable_ui()

    def on_button_trans(self):
        self.disable_ui()
        self.launch.emit(self.comboBox.currentIndex(), self.textEdit_in.toPlainText())

    def disable_ui(self):
        self.button_trans.setEnabled(False)
        self.button_clear.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.button_goo.setEnabled(False)
        self.button_bai.setEnabled(False)
        self.button_bing.setEnabled(False)
        self.button_jin.setEnabled(False)
        self.button_you.setEnabled(False)
        self.button_zhi.setEnabled(False)

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

    def enable_ui(self):
        self.button_trans.setEnabled(True)
        self.button_clear.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.button_goo.setEnabled(True)
        self.button_bai.setEnabled(True)
        self.button_bing.setEnabled(True)
        self.button_jin.setEnabled(True)
        self.button_you.setEnabled(True)
        self.button_zhi.setEnabled(True)

    def keyPressEvent(self, event):
        if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_Q:
            self.on_button_trans()
        event.accept()

    def on_checkBox_goo_stateChanged(self, state):
        if state == 0:
            self.gridLayout_10.removeWidget(self.widget_goo)
            self.widget_goo.hide()
        else:
            self.gridLayout_10.addWidget(self.widget_goo)
            self.widget_goo.show()

    def on_checkBox_bai_stateChanged(self, state):
        if state == 0:
            self.gridLayout_10.removeWidget(self.widget_bai)
            self.widget_bai.hide()
        else:
            self.gridLayout_10.addWidget(self.widget_bai)
            self.widget_bai.show()

    def on_checkBox_bing_stateChanged(self, state):
        if state == 0:
            self.gridLayout_10.removeWidget(self.widget_bing)
            self.widget_bing.hide()
        else:
            self.gridLayout_10.addWidget(self.widget_bing)
            self.widget_bing.show()

    def on_checkBox_jin_stateChanged(self, state):
        if state == 0:
            self.gridLayout_10.removeWidget(self.widget_jin)
            self.widget_jin.hide()
        else:
            self.gridLayout_10.addWidget(self.widget_jin)
            self.widget_jin.show()

    def on_checkBox_you_stateChanged(self, state):
        if state == 0:
            self.gridLayout_10.removeWidget(self.widget_you)
            self.widget_you.hide()
        else:
            self.gridLayout_10.addWidget(self.widget_you)
            self.widget_you.show()

    def on_checkBox_zhi_stateChanged(self, state):
        if state == 0:
            self.gridLayout_10.removeWidget(self.widget_zhi)
            self.widget_zhi.hide()
        else:
            self.gridLayout_10.addWidget(self.widget_zhi)
            self.widget_zhi.show()
    def on_aboutAction(self):
        QMessageBox.information(self, 'About', 'EasyTranslator version 2.0\nDeveloped by Daibingh')


# def resource_path(relative_path):
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)
#
#
# class Work_1(QThread):
#
#     done = pyqtSignal()
#
#     def __init__(self, text):
#         QThread.__init__(self)
#         self.text = text
#
#     def run(self):
#         try:
#             self.direct = langdetect(self.text)
#             pass
#         except ConnectionError as e:
#             self.direct = -1
#             print('网络连接错误，检测语言失败！')
#         except Exception as e:
#             self.e = e
#             self.direct = -2
#             print(e, '检测语言失败！')
#         self.done.emit()
#
#
# class Work_2(QThread):
#
#     done = pyqtSignal(str, str)
#
#     def __init__(self, text, direct, fun_handle):
#         QThread.__init__(self)
#         self.text = text
#         self.direct = direct
#         self.fun_handle = fun_handle
#
#     def run(self):
#         try:
#             self.result = self.fun_handle(self.text, self.direct)
#         except ConnectionError as e:
#             self.result = -1
#             print('网络连接错误，'+self.fun_handle.__name__+'翻译失败！')
#         except Exception as e:
#             self.e = e
#             self.result = -2
#             print(e, self.fun_handle.__name__ + '翻译失败！')
#         self.done.emit(self.fun_handle.__name__, str(self.result))
#
#
# class Work_3(QThread):
#
#     has_new = pyqtSignal(str)
#
#     def __int__(self):
#         super().__init__()
#
#     def run(self):
#         self.text = ''
#         while True:
#             text_ = QApplication.clipboard().text()
#             if text_ != self.text:
#                 self.text = text_
#                 self.has_new.emit(self.text)
#                 print(self.text)
#
#
# class EasyTranslator(QMainWindow):
#
#     ui = Ui_MainWindow()
#     count = 0
#     trans = pyqtSignal(str, int)
#     work_1 = Work_1('')
#     work_2s = []
#     text = ''
#     direct = 0
#     work_2s.append(Work_2(text, direct, googleTraslator))
#     work_2s.append(Work_2(text, direct, baiduTranslator))
#     work_2s.append(Work_2(text, direct, bingTranslator))
#     work_2s.append(Work_2(text, direct, jinshanTranslator))
#     work_2s.append(Work_2(text, direct, youdaoTranslator))
#     work_2s.append(Work_2(text, direct, cnkiTranslator))
#     work_3 = Work_3()
#
#     def __init__(self):
#         super().__init__()
#         self.ui.setupUi(self)
#         self.setWindowTitle('EasyTranslator')
#         self.setWindowIcon(QIcon(resource_path('icon.png')))
#         self.ui.label.setPixmap(QPixmap(resource_path('google.png')))
#         self.ui.label_2.setPixmap(QPixmap(resource_path('baidu.png')))
#         self.ui.label_3.setPixmap(QPixmap(resource_path('bing.png')))
#         self.ui.label_4.setPixmap(QPixmap(resource_path('powerword.png')))
#         self.ui.label_5.setPixmap(QPixmap(resource_path('youdao.png')))
#         self.ui.label_6.setPixmap(QPixmap(resource_path('cnki.png')))
#         self.ui.checkBox_bai.setCheckState(2)
#         self.ui.checkBox_goo.setCheckState(2)
#         self.ui.checkBox_bing.setCheckState(2)
#         self.ui.checkBox_you.setCheckState(2)
#         self.ui.checkBox_zhi.setCheckState(2)
#         self.ui.checkBox_jin.setCheckState(2)
#         aboutAct = QAction('关于', self)
#         self.moni = QAction('开始监控', self)
#         self.moni.setObjectName('moni_action')
#         self.menuBar().addAction(aboutAct)
#         self.menuBar().addAction(self.moni)
#         self.loadStyleSheet(resource_path('white.qss'))
#         self.resize(860, 650)
#         self.center()
#
#         self.ui.button_trans.clicked.connect(self.on_button_trans)
#         self.ui.button_clear.clicked.connect(self.on_button_clear)
#         self.trans.connect(self.transapi)
#
#         self.ui.button_goo.clicked.connect(self.on_button_goo)
#         self.ui.button_bai.clicked.connect(self.on_button_bai)
#         self.ui.button_bing.clicked.connect(self.on_button_bing)
#         self.ui.button_jin.clicked.connect(self.on_button_jin)
#         self.ui.button_you.clicked.connect(self.on_button_you)
#         self.ui.button_zhi.clicked.connect(self.on_button_zhi)
#
#         aboutAct.triggered.connect(self.on_aboutAction)
#         self.moni.triggered.connect(self.on_moni_triggered)
#         self.work_3.has_new.connect(self.copy_trans)
#         self.work_1.done.connect(self.landet)
#         for work_2 in self.work_2s:
#             work_2.done.connect(self.disp)
#
#     def keyPressEvent(self, event):
#         if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier \
#                 and event.key() == QtCore.Qt.Key_Q:
#             self.on_button_trans()
#         event.accept()
#
#     def on_checkBox_goo_stateChanged(self, state):
#         if state == 0:
#             self.ui.gridLayout_10.removeWidget(self.ui.widget_goo)
#             self.ui.widget_goo.hide()
#         else:
#             self.ui.gridLayout_10.addWidget(self.ui.widget_goo)
#             self.ui.widget_goo.show()
#
#     def on_checkBox_bai_stateChanged(self, state):
#         if state == 0:
#             self.ui.gridLayout_10.removeWidget(self.ui.widget_bai)
#             self.ui.widget_bai.hide()
#         else:
#             self.ui.gridLayout_10.addWidget(self.ui.widget_bai)
#             self.ui.widget_bai.show()
#
#     def on_checkBox_bing_stateChanged(self, state):
#         if state == 0:
#             self.ui.gridLayout_10.removeWidget(self.ui.widget_bing)
#             self.ui.widget_bing.hide()
#         else:
#             self.ui.gridLayout_10.addWidget(self.ui.widget_bing)
#             self.ui.widget_bing.show()
#
#     def on_checkBox_jin_stateChanged(self, state):
#         if state == 0:
#             self.ui.gridLayout_10.removeWidget(self.ui.widget_jin)
#             self.ui.widget_jin.hide()
#         else:
#             self.ui.gridLayout_10.addWidget(self.ui.widget_jin)
#             self.ui.widget_jin.show()
#
#     def on_checkBox_you_stateChanged(self, state):
#         if state == 0:
#             self.ui.gridLayout_10.removeWidget(self.ui.widget_you)
#             self.ui.widget_you.hide()
#         else:
#             self.ui.gridLayout_10.addWidget(self.ui.widget_you)
#             self.ui.widget_you.show()
#
#     def on_checkBox_zhi_stateChanged(self, state):
#         if state == 0:
#             self.ui.gridLayout_10.removeWidget(self.ui.widget_zhi)
#             self.ui.widget_zhi.hide()
#         else:
#             self.ui.gridLayout_10.addWidget(self.ui.widget_zhi)
#             self.ui.widget_zhi.show()
#
#     def on_moni_triggered(self):
#         if self.moni.text() == '开始监控':
#             self.moni.setText('停止监控')
#             self.menuBar().setStyleSheet('QMenuBar{background:red}')
#             self.work_3.start()
#         else:
#             self.moni.setText('开始监控')
#             self.menuBar().setStyleSheet('QMenuBar{background:rgb(187, 212, 238)}')
#             self.work_3.terminate()
#
#     def copy_trans(self, text):
#         self.ui.textEdit_in.setText(text)
#         self.showNormal()
#         self.hide()
#         self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
#         self.show()
#         self.hide()
#         self.setWindowFlags(QtCore.Qt.Widget)
#         self.show()
#         self.on_button_trans()
#
#     def disp(self, fun_name, result):
#         if fun_name == 'googleTraslator':
#             if result == '-1':
#                 self.ui.textEdit_goo.setText('网络连接错误，'+fun_name+'翻译失败！')
#             elif result == '-2':
#                 self.ui.textEdit_goo.setText(str(self.work_2s[0].e) + '，' + fun_name + '翻译失败！')
#             else:
#                 self.ui.textEdit_goo.setText(result)
#         elif fun_name == 'baiduTranslator':
#             if result == '-1':
#                 self.ui.textEdit_bai.setText('网络连接错误，'+fun_name+'翻译失败！')
#             elif result == '-2':
#                 self.ui.textEdit_bai.setText(str(self.work_2s[1].e) + '，' + fun_name + '翻译失败！')
#             else:
#                 self.ui.textEdit_bai.setText(result)
#         elif fun_name == 'bingTranslator':
#             if result == '-1':
#                 self.ui.textEdit_bing.setText('网络连接错误，' + fun_name + '翻译失败！')
#             elif result == '-2':
#                 self.ui.textEdit_bing.setText(str(self.work_2s[2].e) + '，' + fun_name + '翻译失败！')
#             else:
#                 self.ui.textEdit_bing.setText(result)
#         elif fun_name == 'jinshanTranslator':
#             if result == '-1':
#                 self.ui.textEdit_jin.setText('网络连接错误，' + fun_name + '翻译失败！')
#             elif result == '-2':
#                 self.ui.textEdit_jin.setText(str(self.work_2s[3].e) + '，' + fun_name + '翻译失败！')
#             else:
#                 self.ui.textEdit_jin.setText(result)
#         elif fun_name == 'youdaoTranslator':
#             if result == '-1':
#                 self.ui.textEdit_you.setText('网络连接错误，' + fun_name + '翻译失败！')
#             elif result == '-2':
#                 self.ui.textEdit_you.setText(str(self.work_2s[4].e) + '，' + fun_name + '翻译失败！')
#             else:
#                 self.ui.textEdit_you.setText(result)
#         else:
#             if result == '-1':
#                 self.ui.textEdit_zhi.setText('网络连接错误，' + fun_name + '翻译失败！')
#             elif result == '-2':
#                 self.ui.textEdit_zhi.setText(str(self.work_2s[5].e) + '，' + fun_name + '翻译失败！')
#             else:
#                 self.ui.textEdit_zhi.setText(result)
#         self.count += 1
#         if self.count == 6:
#             self.work()
#             self.count = 0
#
#     def transapi(self, text, direct):
#         transfuns = [googleTraslator, baiduTranslator, bingTranslator, jinshanTranslator, youdaoTranslator, cnkiTranslator]
#         i = 0
#         for work_2 in self.work_2s:
#             work_2.text = text
#             work_2.direct =direct
#             work_2.fun_handle = transfuns[i]
#             i += 1
#             work_2.start()
#
#
#     def landet(self):
#         # self.ui.textEdit_goo.setPlainText(str(self.work_1.direct))
#         if self.work_1.direct == -1:
#             QMessageBox.information(self, '错误', '网络连接错误，检测语言失败！')
#             self.work()
#         elif self.work_1.direct == -2:
#             QMessageBox.information(self, '错误', str(self.work_1.e) + '，检测语言失败！')
#             self.work()
#         else:
#             self.trans.emit(self.text, self.work_1.direct)
#
#     def wait(self):
#         self.ui.button_trans.setEnabled(False)
#         self.ui.button_clear.setEnabled(False)
#         self.ui.comboBox.setEnabled(False)
#         self.ui.button_goo.setEnabled(False)
#         self.ui.button_bai.setEnabled(False)
#         self.ui.button_bing.setEnabled(False)
#         self.ui.button_jin.setEnabled(False)
#         self.ui.button_you.setEnabled(False)
#         self.ui.button_zhi.setEnabled(False)
#
#     def work(self):
#         self.ui.button_trans.setEnabled(True)
#         self.ui.button_clear.setEnabled(True)
#         self.ui.comboBox.setEnabled(True)
#         self.ui.button_goo.setEnabled(True)
#         self.ui.button_bai.setEnabled(True)
#         self.ui.button_bing.setEnabled(True)
#         self.ui.button_jin.setEnabled(True)
#         self.ui.button_you.setEnabled(True)
#         self.ui.button_zhi.setEnabled(True)
#
#     def on_button_trans(self):
#
#         self.count = 0
#         text = self.ui.textEdit_in.toPlainText()
#         self.text = text
#         if text == '':
#             print('no input')
#             return
#         ind = self.ui.comboBox.currentIndex()
#         self.wait()
#         if ind == 0:
#             self.work_1.text = text
#             self.work_1.start()
#             return
#         else:
#             direct = ind - 1
#             self.trans.emit(text, direct)
#             return
#
    # def on_button_clear(self):
    #     self.ui.textEdit_in.clear()
#
#     def on_button_goo(self):
#         QApplication.clipboard().setText(self.ui.textEdit_goo.toPlainText())
#
#     def on_button_bai(self):
#         QApplication.clipboard().setText(self.ui.textEdit_bai.toPlainText())
#
#
#     def on_button_bing(self):
#         QApplication.clipboard().setText(self.ui.textEdit_bing.toPlainText())
#
#     def on_button_jin(self):
#         QApplication.clipboard().setText(self.ui.textEdit_jin.toPlainText())
#
#     def on_button_you(self):
#         QApplication.clipboard().setText(self.ui.textEdit_you.toPlainText())
#
#     def on_button_zhi(self):
#         QApplication.clipboard().setText(self.ui.textEdit_zhi.toPlainText())
#
#     def loadStyleSheet(self, file):
#         with open(file, 'r', encoding='utf-8') as f:
#             s = f.readlines()
#             s = ''.join(s).strip('\n')
#         self.setStyleSheet(s)
#
    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.setGeometry(qr)
#
#     def on_aboutAction(self):
#         QMessageBox.information(self, 'About', 'EasyTranslator version 2.0\nDeveloped by Daibingh')