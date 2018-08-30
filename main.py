# -*- coding: utf-8 -*-

from EasyTranslator import EasyTranslator
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import sip

if __name__ == '__main__':
    # if getattr(sys, 'frozen', False):  # we are running in a |PyInstaller| bundle
    #     basedir = sys._MEIPASS
    # else:  # we are running in a normal Python environment
    #     basedir = os.path.dirname(__file__)
    app = QApplication(sys.argv)
    w= EasyTranslator()
    w.show()
    sys.exit(app.exec_())