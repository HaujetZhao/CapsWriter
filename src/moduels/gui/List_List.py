# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from moduels.component.NormalValue import 常量

# 添加预设对话框
class List_List(QListWidget):

    选中文字 = Signal(str)

    def __init__(self, 数据库连接, 表单名字, 显示的列名):
        super().__init__()
        self.筛选文字 = ''
        self.数据库连接 = 数据库连接
        self.表单名字 = 表单名字
        self.显示的列名 = 显示的列名
        self.initElements()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayouts()  # 然后布局
        self.initValues()  # 再定义各个控件的值

    def initElements(self):
        pass

    def initSlots(self):
        pass

    def initLayouts(self):
        pass

    def initValues(self):
        self.刷新列表()

    def currentChanged(self, current, previous):
        if current.row() > -1:
            self.选中文字.emit(current.data())

    def 刷新列表(self):
        cursor = self.数据库连接.cursor()
        if self.筛选文字 == '':
            显示项 = cursor.execute(
                f'''select id, {self.显示的列名} from {self.表单名字} order by id''')
            self.clear()
            for i in 显示项:
                self.addItem(i[1])
        else:
            显示项 = cursor.execute(
                f'''select id, {self.显示的列名}, * from {self.表单名字} order by id''')
            self.clear()
            for i in 显示项:
                for j in i[2:]:
                    if self.筛选文字 in str(j):
                        self.addItem(i[1])
                        break

