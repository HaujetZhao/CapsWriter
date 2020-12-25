# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *

from moduels.component.NormalValue import 常量
from moduels.component.Stream import Stream
from moduels.gui.Tab_CapsWriter import Tab_CapsWriter
# from moduels.gui.Tab_Stdout import Tab_Stdout
from moduels.gui.Tab_Config import Tab_Config
from moduels.gui.Tab_Help import Tab_Help

import sys, os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        常量.主窗口 = self
        self.loadStyleSheet()
        self.initElements()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayouts()  # 然后布局
        self.initValues()  # 再定义各个控件的值


        # self.setWindowState(Qt.WindowMaximized)
        # sys.stdout = Stream(newText=self.onUpdateText)

    def initElements(self):
        self.状态栏 = self.statusBar()
        # 定义中心控件为多 tab 页面
        self.tabs = QTabWidget()

        # 定义多个不同功能的 tab
        self.设置标签页 = Tab_Config() # 设置页要在前排加载，以确保一些设置加载成功
        self.CapsWriter标签页 = Tab_CapsWriter()  # 主要功能的 tab
        # self.打印输出标签页 = Tab_Stdout()
        self.帮助标签页 = Tab_Help()

        self.标准输出流 = Stream()



    def initLayouts(self):

        self.tabs.addTab(self.CapsWriter标签页, 'CapsWriter')
        self.tabs.addTab(self.设置标签页, '设置')
        self.tabs.addTab(self.帮助标签页, '帮助')
        self.setCentralWidget(self.tabs)

    def initSlots(self):
        self.CapsWriter标签页.状态栏消息.connect(lambda 消息, 时间: self.状态栏.showMessage(消息, 时间))
        # self.打印输出标签页.状态栏消息.connect(lambda 消息, 时间: self.状态栏.showMessage(消息, 时间))
        # self.设置标签页.状态栏消息.connect(lambda 消息, 时间: self.状态栏.showMessage(消息, 时间))
        self.帮助标签页.状态栏消息.connect(lambda 消息, 时间: self.状态栏.showMessage(消息, 时间))

        self.标准输出流.newText.connect(self.CapsWriter标签页.更新控制台输出)
        pass

    def initValues(self):
        # self.adjustSize()
        # self.setGeometry(QStyle(Qt.LeftToRight, Qt.AlignCenter, self.size(), QApplication.desktop().availableGeometry()))
        常量.状态栏 = self.状态栏
        sys.stdout = self.标准输出流
        self.setWindowIcon(QIcon(常量.图标路径))
        self.setWindowTitle('CapsWriter 语音输入工具')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 始终在前台
        print("""\n软件介绍：

CapsWriter，顾名思义，就是按下大写锁定键来打字的工具。它的具体作用是：当你按下键盘上的大写锁定键后，软件开始语音识别，当你松开大写锁定键时，识别的结果就可以立马上屏。

目前软件内置了对阿里云一句话识别 API 的支持。如果你要使用，就需要先在阿里云上实名认证，申请语音识别 API，在设置页面添加一个语音识别引擎。

具体申请阿里云 API 的方法，可以参考我这个视频：https://www.bilibili.com/video/BV1qK4y1s7Fb/

添加上引擎后，在当前页面选择一个引擎，点击启用按钮，就可以进行语音识别了！嗯

启用后，在实际使用中，只要按下 CapsLock 键，软件就会立刻开始录音：

    如果只是单击 CapsLock 后松开，录音数据会立刻被删除；
    如果按下 CapsLock 键时长超过 0.3 秒，就会开始连网进行语音识别，松开 CapsLock 键时，语音识别结果会被立刻输入。

所以你只需要按下 CapsLock 键，无需等待，就可以开始说话，因为当你按下按下 CapsLock 键的时候，程序就开始录音了。说完后，松开，识别结果立马上屏。\r\n""")

        self.show()

    def 移动到屏幕中央(self):
        rectangle = self.frameGeometry()
        center = QApplication.desktop().availableGeometry().center()
        rectangle.moveCenter(center)
        self.move(rectangle.topLeft())

    def 更新控制台输出(self, text):
        self.打印输出标签页.print(text)

    def loadStyleSheet(self):
        try:
            try:
                with open(常量.样式文件, 'r', encoding='utf-8') as style:
                    self.setStyleSheet(style.read())
            except:
                with open(常量.样式文件, 'r', encoding='gbk') as style:
                    self.setStyleSheet(style.read())
        except:
            QMessageBox.warning(self, self.tr('主题载入错误'), self.tr('未能成功载入主题，请确保软件 misc 目录有 "style.css" 文件存在。'))

    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if (event.key() == Qt.Key_F5):
            self.loadStyleSheet()
            self.status.showMessage('已成功更新主题', 800)

    def onUpdateText(self, text):
        """Write console output to text widget."""

        cursor = self.consoleTab.consoleEditBox.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.consoleTab.consoleEditBox.setTextCursor(cursor)
        self.consoleTab.consoleEditBox.ensureCursorVisible()

    def 状态栏提示(self, 提示文字:str, 时间:int):
        self.状态栏.showMessage(提示文字, 时间)


    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        if 常量.关闭时隐藏到托盘:
            event.ignore()
            self.hide()
        else:
            sys.stdout = sys.__stdout__
            super().closeEvent(event)
