# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import sys

from moduels.component.NormalValue import 常量

class SystemTray(QSystemTrayIcon):
    def __init__(self, 主窗口):
        super(SystemTray, self).__init__()
        self.主窗口 = 主窗口
        self.initElements()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayouts()  # 然后布局
        self.initValues()  # 再定义各个控件的值

        # self.RestoreAction = QAction(u'还原 ', self, triggered=self.showWindow)  # 添加一级菜单动作选项(还原主窗口)
        # self.StyleAction = QAction(self.tr('更新主题'), self, triggered=mainWindow.loadStyleSheet)  # 添加一级菜单动作选项(更新 QSS)
        # self.tray_menu.addAction(self.RestoreAction)  # 为菜单添加动作
        # self.tray_menu.addAction(self.StyleAction)

    def initElements(self):
        self.托盘菜单 = QMenu(QApplication.desktop())  # 创建菜单
        self.QuitAction = QAction(self.tr('退出'), self, triggered=self.退出)  # 添加一级菜单动作选项(退出程序)

    def initSlots(self):
        self.activated.connect(self.trayEvent)  # 设置托盘点击事件处理函数

    def initLayouts(self):
        self.托盘菜单.addAction(self.QuitAction)

    def initValues(self):
        self.setIcon(QIcon(常量.图标路径))
        self.setParent(self.主窗口)
        self.setContextMenu(self.托盘菜单)  # 设置系统托盘菜单
        self.show()

    def 显示主窗口(self):
        self.主窗口.showNormal()
        self.主窗口.activateWindow()
        self.主窗口.setWindowFlag(Qt.Window, Qt.WindowStaysOnTopHint)  # 始终在前台
        self.主窗口.show()

    def 退出(self):
        sys.stdout = sys.__stdout__
        self.hide()
        QApplication.quit()

    def 切换聆听中的图标(self):
        self.setIcon(QIcon(常量.聆听图标路径))

    def 切换正常图标(self):
        self.setIcon(QIcon(常量.图标路径))

    def trayEvent(self, reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            if 常量.主窗口.isMinimized() or not 常量.主窗口.isVisible():
                # 若是最小化或者最小化到托盘，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.显示主窗口()
            else:
                # 若不是最小化，则最小化
                # self.window.showMinimized()
                self.主窗口.hide()
                pass