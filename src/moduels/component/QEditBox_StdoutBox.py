# -*- coding: UTF-8 -*-
import sys

from PySide2.QtWidgets import QTextEdit
from PySide2.QtGui import QTextCursor

from moduels.component.Stream import Stream

# 命令输出窗口中的多行文本框
class QEditBox_StdoutBox(QTextEdit):
    # 定义一个 QTextEdit 类，写入 print 方法。用于输出显示。
    def __init__(self, parent=None):
        super(QEditBox_StdoutBox, self).__init__(parent)
        self.setReadOnly(True)
        self.标准输出流 = Stream()
        self.标准输出流.newText.connect(self.print)
        sys.stdout = self.标准输出流

    def print(self, text):
        try:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(text)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
        except:
            print('文本框更新文本失败')
