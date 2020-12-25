# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from moduels.component.NormalValue import 常量


class Dialog_AddEngine(QDialog):
    def __init__(self, 列表, 数据库连接, 表单名字, 显示的列名):
        super().__init__(常量.主窗口)
        self.列表 = 列表
        self.数据库连接 = 数据库连接
        self.表单名字 = 表单名字
        self.显示的列名 = 显示的列名
        self.initElements()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayouts()  # 然后布局
        self.initValues()  # 再定义各个控件的值

    def initElements(self):
        self.引擎名称编辑框 = QLineEdit()
        self.服务商选择框 = QComboBox()
        self.appKey输入框 = QLineEdit()
        self.语言Combobox = QComboBox()
        self.accessKeyId输入框 = QLineEdit()
        self.AccessKeySecret输入框 = QLineEdit()

        self.确定按钮 = QPushButton(self.tr('确定'))
        self.取消按钮 = QPushButton(self.tr('取消'))

        self.纵向布局 = QVBoxLayout()
        self.表格布局 = QFormLayout()
        self.按钮横向布局 = QHBoxLayout()

    def initSlots(self):
        self.服务商选择框.currentTextChanged.connect(self.服务商变化)

        self.确定按钮.clicked.connect(self.确认)
        self.取消按钮.clicked.connect(self.取消)

    def initLayouts(self):
        self.表格布局.addRow('引擎名称：', self.引擎名称编辑框)
        self.表格布局.addRow('服务商：', self.服务商选择框)
        self.表格布局.addRow('AppKey：', self.appKey输入框)
        self.表格布局.addRow('语言：', self.语言Combobox)
        self.表格布局.addRow('AccessKeyId：', self.accessKeyId输入框)
        self.表格布局.addRow('AccessKeySecret：', self.AccessKeySecret输入框)

        self.按钮横向布局.addWidget(self.确定按钮)
        self.按钮横向布局.addWidget(self.取消按钮)

        self.纵向布局.addLayout(self.表格布局)
        self.纵向布局.addLayout(self.按钮横向布局)

        self.setLayout(self.纵向布局)

    def initValues(self):
        self.引擎名称编辑框.setPlaceholderText(self.tr('例如：阿里-中文'))

        self.服务商选择框.addItems(['Alibaba'])
        self.服务商选择框.setCurrentText('Alibaba')

        self.accessKeyId输入框.setEchoMode(QLineEdit.Password)
        self.AccessKeySecret输入框.setEchoMode(QLineEdit.Password)

        self.setWindowIcon(QIcon(常量.图标路径))
        self.setWindowTitle(self.tr('添加或更新 Api'))
        self.setWindowModality(Qt.NonModal)

        if self.列表.currentItem():
            已选中的列表项 = self.列表.currentItem().text()
            填充数据 = self.从数据库得到选中项的数据(已选中的列表项)
            self.引擎名称编辑框.setText(填充数据[0])
            self.服务商选择框.setCurrentText(填充数据[1])
            self.appKey输入框.setText(填充数据[2])
            self.语言Combobox.setCurrentText(填充数据[3])
            self.accessKeyId输入框.setText(填充数据[4])
            self.AccessKeySecret输入框.setText(填充数据[5])

        self.show()


    def 服务商变化(self):
        if self.服务商选择框.currentText() == 'Alibaba':
            self.语言Combobox.clear()
            self.语言Combobox.addItem(self.tr('由 Api 的云端配置决定'))
            self.语言Combobox.setCurrentText(self.tr('由 Api 的云端配置决定'))
            self.语言Combobox.setEnabled(False)
            self.appKey输入框.setEnabled(True)
            # self.accessKeyId标签.setText('AccessKeyId：')
            # self.AccessKeySecret标签.setText('AccessKeySecret：')
        elif self.服务商选择框.currentText() == 'Tencent':
            self.语言Combobox.clear()
            self.语言Combobox.addItems(['中文普通话', '英语', '粤语'])
            self.语言Combobox.setCurrentText('中文普通话')
            self.语言Combobox.setEnabled(True)
            self.appKey输入框.setEnabled(False)
            # self.accessKeyId标签.setText('AccessSecretId：')
            # self.AccessKeySecret标签.setText('AccessSecretKey：')


    def 确认(self):
        self.引擎名称 = self.引擎名称编辑框.text() # str
        self.服务商 = self.服务商选择框.currentText() # str
        self.AppKey = self.appKey输入框.text() # str
        self.语言 = self.语言Combobox.currentText() # str
        self.AccessKeyId = self.accessKeyId输入框.text() # str
        self.AccessKeySecret = self.AccessKeySecret输入框.text() # str
        self.有重名项 = self.检查数据库是否有重名项()
        if self.引擎名称 == '':
            return False
        if self.有重名项:
            是否覆盖 = QMessageBox.warning(self, '覆盖确认', '已存在相同名字的引擎，是否覆盖？', QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
            if 是否覆盖 != QMessageBox.Yes:
                return False
            self.更新数据库()
        else:
            self.插入数据库()
        self.close()

    def 取消(self):
        self.close()

    def 从数据库得到选中项的数据(self, 已选中的列表项):
        数据库连接 = self.数据库连接
        cursor = 数据库连接.cursor()
        result = cursor.execute(f'''select 引擎名称, 
                                            服务商, 
                                            AppKey, 
                                            语言, 
                                            AccessKeyId, 
                                            AccessKeySecret 
                                    from {self.表单名字} where {self.显示的列名} = :引擎名称;''',
                                {'引擎名称': 已选中的列表项})
        return result.fetchone()
    #
    def 检查数据库是否有重名项(self):
        数据库连接 = self.数据库连接
        cursor = 数据库连接.cursor()
        result = cursor.execute(f'''select * from {self.表单名字} where {self.显示的列名} = :引擎名称;''', {'引擎名称': self.引擎名称})
        if result.fetchone() == None: return False # 没有重名项，返回 False
        return True
    #
    def 更新数据库(self):
        数据库连接 = self.数据库连接
        cursor = 数据库连接.cursor()
        cursor.execute(f'''update {self.表单名字} set 服务商 = :服务商,
                                        AppKey = :AppKey,
                                        语言 = :语言,
                                        AccessKeyId = :AccessKeyId,
                                        AccessKeySecret = :AccessKeySecret
                                        where {self.显示的列名} = :引擎名称 ''',
                       {'服务商': self.服务商,
                        'AppKey': self.AppKey,
                        '语言': self.语言,
                        'AccessKeyId': self.AccessKeyId,
                        'AccessKeySecret': self.AccessKeySecret,
                        '引擎名称': self.引擎名称})
        数据库连接.commit()
    #
    def 插入数据库(self):
        数据库连接 = self.数据库连接
        cursor = 数据库连接.cursor()
        cursor.execute(f'''insert into {self.表单名字} (引擎名称, 
                                                        服务商, 
                                                        AppKey, 
                                                        语言, 
                                                        AccessKeyId, 
                                                        AccessKeySecret) 
                                                values (:引擎名称, 
                                                        :服务商, 
                                                        :AppKey, 
                                                        :语言, 
                                                        :AccessKeyId, 
                                                        :AccessKeySecret)''',
                                               {'引擎名称': self.引擎名称,
                                                '服务商': self.服务商,
                                                'AppKey': self.AppKey,
                                                '语言': self.语言,
                                                'AccessKeyId': self.AccessKeyId,
                                                'AccessKeySecret': self.AccessKeySecret})
        数据库连接.commit()

    # 根据刚开始预设名字是否为空，设置确定键可否使用
    def closeEvent(self, a0: QCloseEvent) -> None:
        try:
            self.列表.刷新列表()
        except:
            print('引擎列表刷新失败')
