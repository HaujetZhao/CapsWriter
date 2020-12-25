from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class Stream(QObject):
    # 用于将控制台的输出定向到一个槽
    newText = Signal(str)

    # def __init__(self):
    #     super().__init__()
        # self.newText = Signal(str)

    def write(self, text):
        self.newText.emit(str(text))
        # QApplication.processEvents()

    def flush(self):
        pass