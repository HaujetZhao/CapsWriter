# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import QGroupBox, QLineEdit, QPushButton, QGridLayout
from moduels.gui.List_List import List_List

# 添加预设对话框
class Group_EditableList(QGroupBox):
    def __init__(self, 组名, 对话框类, 数据库连接, 表单名字, 显示的列名):
        super().__init__(组名)
        self.对话框类 = 对话框类
        self.数据库连接 = 数据库连接
        self.表单名字 = 表单名字
        self.显示的列名 = 显示的列名
        self.initElements()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayouts()  # 然后布局
        self.initValues()  # 再定义各个控件的值

    def initElements(self):
        self.筛选文字输入框 = QLineEdit()
        self.列表 = List_List(self.数据库连接, self.表单名字, self.显示的列名)
        self.添加按钮 = QPushButton('+')
        self.删除按钮 = QPushButton('-')
        self.上移按钮 = QPushButton('↑')
        self.下移按钮 = QPushButton('↓')
        self.部件布局 = QGridLayout()

    def initSlots(self):
        self.筛选文字输入框.textChanged.connect(self.筛选)
        self.添加按钮.clicked.connect(self.添加或修改)
        self.删除按钮.clicked.connect(self.删除)
        self.上移按钮.clicked.connect(self.上移)
        self.下移按钮.clicked.connect(self.下移)

    def initLayouts(self):
        self.部件布局.addWidget(self.筛选文字输入框, 0, 0, 1, 2)
        self.部件布局.addWidget(self.列表, 1, 0, 1, 2)
        self.部件布局.addWidget(self.添加按钮, 2, 0, 1, 1)
        self.部件布局.addWidget(self.删除按钮, 2, 1, 1, 1)
        self.部件布局.addWidget(self.上移按钮, 3, 0, 1, 1)
        self.部件布局.addWidget(self.下移按钮, 3, 1, 1, 1)
        self.setLayout(self.部件布局)

    def initValues(self):
        self.筛选文字输入框.setPlaceholderText('筛选')
        self.列表.刷新列表()


    def 添加或修改(self):
        '''
        打开对话框，添加或修改条目
        '''
        对话框 = self.对话框类(self.列表, self.数据库连接, self.表单名字, self.显示的列名)

    def 删除(self):
        if not self.列表.currentItem(): return False
        当前排 = self.列表.currentRow()
        已选中的列表项 = self.列表.currentItem().text()
        answer = QMessageBox.question(self, self.tr('删除预设'), self.tr(f'将要删除“{已选中的列表项}”项，是否确认？'))
        if answer != QMessageBox.Yes: return False
        id = self.数据库连接.cursor().execute(
            f'''select id from {self.表单名字} where {self.显示的列名} = :已选中的列表项''', {'已选中的列表项': 已选中的列表项}).fetchone()[0]
        self.数据库连接.cursor().execute(f'''delete from {self.表单名字} where id = :id''', {'id': id})
        self.数据库连接.cursor().execute(f'''update {self.表单名字} set id=id-1 where id > :id''', {'id': id})
        self.数据库连接.commit()
        self.列表.刷新列表()
        if self.列表.count() >= 当前排:
            self.列表.setCurrentRow(当前排)

    def 上移(self):
        当前排 = self.列表.currentRow()
        if 当前排 > 0:
            已选中的列表项 = self.列表.currentItem().text()
            id = self.数据库连接.cursor().execute(
                f'''select id from {self.表单名字} where {self.显示的列名} = :已选中的列表项 ''', {'已选中的列表项': 已选中的列表项}).fetchone()[0]
            self.数据库连接.cursor().execute(f'''update {self.表单名字} set id = 100000 where id = :id - 1 ''', {'id': id})
            self.数据库连接.cursor().execute(f'''update {self.表单名字} set id = id - 1 where {self.显示的列名} = :已选中的列表项''', {'已选中的列表项': 已选中的列表项})
            self.数据库连接.cursor().execute(f'''update {self.表单名字} set id = :id where id=100000 ''', {'id': id})
            self.数据库连接.commit()
            self.列表.刷新列表()
            if self.列表.筛选文字 == '':
                self.列表.setCurrentRow(当前排 - 1)
        return

    # 向下移动预设
    def 下移(self):
        当前排 = self.列表.currentRow()
        总行数 = self.列表.count()
        if 当前排 > -1 and 当前排 < 总行数 - 1:
            已选中的列表项 = self.列表.currentItem().text()
            id = self.数据库连接.cursor().execute(
                f'''select id from {self.表单名字} where {self.显示的列名} = :已选中的列表项''', {'已选中的列表项': 已选中的列表项}).fetchone()[0]
            self.数据库连接.cursor().execute(f'''update {self.表单名字} set id = 100000 where id = :id + 1 ''', {'id': id})
            self.数据库连接.cursor().execute(f'''update {self.表单名字} set id = id + 1 where {self.显示的列名} = :已选中的列表项''', {'已选中的列表项': 已选中的列表项})
            self.数据库连接.cursor().execute(f'''update {self.表单名字} set id = :id where id=100000 ''', {'id': id})
            self.数据库连接.commit()
            self.列表.刷新列表()
            if self.列表.筛选文字 == '':
                if 当前排 < 总行数:
                    self.列表.setCurrentRow(当前排 + 1)
                else:
                    self.列表.setCurrentRow(当前排)
        return

    def 筛选(self):
        self.列表.筛选文字 = self.筛选文字输入框.text()
        self.列表.刷新列表()

