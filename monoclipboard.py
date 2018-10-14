# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
import sys
import time


def read_clipboard(app):
    return app.clipboard().text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start = time.time()
    text = ''
    while int(time.time() - start) < 60:
        text_ = read_clipboard(app)
        if text_ != text:
            text = text_
            print(text)