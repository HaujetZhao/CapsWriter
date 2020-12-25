import sqlite3
import platform
import subprocess


class NormalValue():
    样式文件 = 'misc/style.css'
    软件版本 = '2.0.0'

    主窗口 = None
    托盘 = None
    状态栏 = None

    Token配置路径 = 'misc/Token.ini'

    数据库路径 = 'misc/database.db'
    数据库连接 = sqlite3.connect(数据库路径)

    偏好设置表单名 = '偏好设置'
    语音引擎表单名 = '语音引擎'

    关闭时隐藏到托盘 = False


    系统平台 = platform.system()

    图标路径 = 'misc/icon.icns' if 系统平台 == 'Darwin' else 'misc/icon.ico'
    聆听图标路径 = 'misc/icon_listning.icns' if 系统平台 == 'Darwin' else 'misc/icon_listning.ico'

    subprocessStartUpInfo = subprocess.STARTUPINFO()
    if 系统平台 == 'Windows':
        subprocessStartUpInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        subprocessStartUpInfo.wShowWindow = subprocess.SW_HIDE

class ThreadValue():
    pass

常量 = NormalValue()
线程值 = ThreadValue()