import webbrowser
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QPushButton, QCheckBox
from moduels.component.NormalValue import 常量
from moduels.gui.Group_EditableList import Group_EditableList
from moduels.gui.Dialog_AddEngine import  Dialog_AddEngine
# from moduels.gui.Group_PathSetting import Group_PathSetting


class Tab_Config(QWidget):
    状态栏消息 = Signal(str, int)

    def __init__(self, parent=None):
        super(Tab_Config, self).__init__(parent)
        self.initElements()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayouts()  # 然后布局
        self.initValues()  # 再定义各个控件的值

    def initElements(self):
        self.程序设置Box = QGroupBox(self.tr('程序设置'))
        self.开关_关闭窗口时隐藏到托盘 = QCheckBox(self.tr('点击关闭按钮时隐藏到托盘'))
        self.程序设置横向布局 = QHBoxLayout()

        self.引擎列表 = Group_EditableList('语音引擎', Dialog_AddEngine, 常量.数据库连接, 常量.语音引擎表单名, '引擎名称')

        self.常用网址Box = QGroupBox('网页控制台')
        self.常用网址Box布局 = QGridLayout()
        self.智能语音交互控制台按钮 = QPushButton('智能语音交互')
        self.RAM访问控制控制台按钮 = QPushButton('RAM访问控制')

        self.页面布局 = QVBoxLayout()


    def initSlots(self):
        self.开关_关闭窗口时隐藏到托盘.stateChanged.connect(self.设置_隐藏到状态栏)
        self.智能语音交互控制台按钮.clicked.connect(lambda: webbrowser.open(r'https://nls-portal.console.aliyun.com/'))
        self.RAM访问控制控制台按钮.clicked.connect(lambda: webbrowser.open(r'https://ram.console.aliyun.com/'))
        # self.路径设置Box.皮肤输出路径输入框.textChanged.connect(self.设置_皮肤输出路径)
        # self.路径设置Box.音效文件路径输入框.textChanged.connect(self.设置_音效文件路径)

    def initLayouts(self):
        self.程序设置横向布局.addWidget(self.开关_关闭窗口时隐藏到托盘)
        self.程序设置Box.setLayout(self.程序设置横向布局)

        self.常用网址Box布局.addWidget(self.智能语音交互控制台按钮, 0, 0)
        self.常用网址Box布局.addWidget(self.RAM访问控制控制台按钮, 0, 1)
        self.常用网址Box.setLayout(self.常用网址Box布局)

        self.页面布局.addWidget(self.程序设置Box)
        self.页面布局.addWidget(self.引擎列表)
        self.页面布局.addWidget(self.常用网址Box)
        self.页面布局.addStretch(1)

        self.setLayout(self.页面布局)

    def initValues(self):
        self.检查数据库()


    def 检查数据库(self):
        数据库连接 = 常量.数据库连接
        self.检查数据库_关闭时最小化(数据库连接)

    def 检查数据库_关闭时最小化(self, 数据库连接):
        result = 数据库连接.cursor().execute(f'''select value from {常量.偏好设置表单名} where item = :item''',
                                {'item': 'hideToTrayWhenHitCloseButton'}).fetchone()
        if result == None: # 如果关闭窗口最小化到状态栏这个选项还没有在数据库创建，那就创建一个
            初始值 = 'False'
            数据库连接.cursor().execute(f'''insert into {常量.偏好设置表单名} (item, value) values (:item, :value) ''',
                           {'item': 'hideToTrayWhenHitCloseButton',
                            'value':初始值})
            数据库连接.commit()
            self.开关_关闭窗口时隐藏到托盘.setChecked(初始值 == 'True')
        else:
            self.开关_关闭窗口时隐藏到托盘.setChecked(result[0] == 'True')
    #
    # def 检查数据库_皮肤输出路径(self, 数据库连接):
    #     result = 数据库连接.cursor().execute(f'''select value from {常量.偏好设置表单名} where item = :item''',
    #                                     {'item': 'skinOutputPath'}).fetchone()
    #     if result == None:  # 如果关闭窗口最小化到状态栏这个选项还没有在数据库创建，那就创建一个
    #         初始值 = 'output'
    #         数据库连接.cursor().execute(f'''insert into {常量.偏好设置表单名} (item, value) values (:item, :value) ''',
    #                                {'item': 'skinOutputPath',
    #                                 'value': 初始值})
    #         数据库连接.commit()
    #         self.路径设置Box.皮肤输出路径输入框.setText(初始值)
    #     else:
    #         self.路径设置Box.皮肤输出路径输入框.setText(result[0])
    #
    # def 检查数据库_音效文件路径(self, 数据库连接):
    #     result = 数据库连接.cursor().execute(f'''select value from {常量.偏好设置表单名} where item = :item''',
    #                                     {'item': 'soundFilePath'}).fetchone()
    #     if result == None:  # 如果关闭窗口最小化到状态栏这个选项还没有在数据库创建，那就创建一个
    #         初始值 = 'sound'
    #         数据库连接.cursor().execute(f'''insert into {常量.偏好设置表单名} (item, value) values (:item, :value) ''',
    #                                {'item': 'soundFilePath',
    #                                 'value': 初始值})
    #         数据库连接.commit()
    #         self.路径设置Box.音效文件路径输入框.setText(初始值)
    #     else:
    #         self.路径设置Box.音效文件路径输入框.setText(result[0])

    def 设置_隐藏到状态栏(self):
        数据库连接 = 常量.数据库连接
        数据库连接.cursor().execute(f'''update {常量.偏好设置表单名} set value = :value where item = :item''',
                               {'item': 'hideToTrayWhenHitCloseButton',
                                'value': str(self.开关_关闭窗口时隐藏到托盘.isChecked())})
        数据库连接.commit()
        常量.关闭时隐藏到托盘 = self.开关_关闭窗口时隐藏到托盘.isChecked()

    # def 设置_皮肤输出路径(self):
    #     数据库连接 = 常量.数据库连接
    #     数据库连接.cursor().execute(f'''update {常量.数据库偏好设置表单名} set value = :value where item = :item''',
    #                            {'item': 'skinOutputPath',
    #                             'value': self.路径设置Box.皮肤输出路径输入框.text()})
    #     数据库连接.commit()
    #     常量.皮肤输出路径 = self.路径设置Box.皮肤输出路径输入框.text()
    #
    #
    # def 设置_音效文件路径(self):
    #     数据库连接 = 常量.数据库连接
    #     数据库连接.cursor().execute(f'''update {常量.数据库偏好设置表单名} set value = :value where item = :item''',
    #                            {'item': 'soundFilePath',
    #                             'value': self.路径设置Box.音效文件路径输入框.text()})
    #     数据库连接.commit()
    #     常量.音效文件路径 = self.路径设置Box.音效文件路径输入框.text()

    def 隐藏到状态栏开关被点击(self):
        cursor = 常量.数据库连接.cursor()
        cursor.execute(f'''update {常量.数据库偏好设置表单名} set value='{str(self.开关_关闭窗口时隐藏到托盘.isChecked())}' where item = '{'hideToTrayWhenHitCloseButton'}';''')
        常量.数据库连接.commit()
