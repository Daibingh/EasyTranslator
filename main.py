# -*- coding: utf-8 -*-

from EasyTranslator import EasyTranslator
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import sip

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w= EasyTranslator()
    w.show()
    sys.exit(app.exec_())