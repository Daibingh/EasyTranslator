# -*- coding: utf-8 -*-

from EasyTranslator import EasyTranslator
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5 import sip
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
import PyQt5.QtCore as QtCore
from pyqtkeybind import keybinder
import os


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


if __name__ == '__main__':	
	os.environ["QT_IM_MODULE"] = "fcitx"
	# os.environ["XMODIFIERS"] = "@im=fcitx"
	app = QApplication(sys.argv)
	window = EasyTranslator()

	def callback():
	    window.setWindowState(window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
	    window.activateWindow()
	    text = QApplication.clipboard().text()
	    text = text.strip().replace('\r\n', ' ').replace('\n', ' ')
	    window.textEdit_in.setText(text)
	    window.on_button_trans()

	def exit_app():
	    window.close()

	keybinder.init()
	keybinder.register_hotkey(window.winId(), "Ctrl+Q", callback)
	keybinder.register_hotkey(window.winId(), "Ctrl+E", exit_app)

	# Install a native event filter to receive events from the OS
	win_event_filter = WinEventFilter(keybinder)
	event_dispatcher = QAbstractEventDispatcher.instance()
	event_dispatcher.installNativeEventFilter(win_event_filter)

	window.show()
	sys.exit(app.exec_())
	keybinder.unregister_hotkey(window.winId(), "Ctrl+Q")
	keybinder.unregister_hotkey(window.winId(), "Ctrl+E")
