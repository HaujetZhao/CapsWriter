# -*- coding: UTF-8 -*-

import json
import os
import pyaudio
import threading
import keyboard
import sqlite3
import time

import ali_speech

from PySide2.QtCore import QThread, Signal
from PySide2.QtWidgets import QApplication

from moduels.component.NormalValue import 常量
from moduels.function.getAlibabaRecognizer import getAlibabaRecognizer




class Thread_AliEngine(QThread):
    状态栏消息 = Signal(str, int)
    引擎出错信号 = Signal()

    CHUNK = 1024  # 数据包或者数据片段
    FORMAT = pyaudio.paInt16  # pyaudio.paInt16表示我们使用量化位数 16位来进行录音
    CHANNELS = 1  # 声道，1为单声道，2为双声道
    RATE = 16000  # 采样率，每秒钟16000次
    总共写入音频片段数 = 0

    count = 1  # 计数
    待命中 = True  # 是否准备开始录音
    识别中 = False  # 控制录音是否停止

    识别中的信号 = Signal()
    结束识别的信号 = Signal()


    def __init__(self, 引擎名称, parent=None):
        super().__init__(parent)
        self.持续录音 = True
        self.正在运行 = 0
        self.引擎名称 = 引擎名称
        self.得到引擎信息()
        self.tokenId = 0
        self.tokenExpireTime = 0
        self.构建按键发送器()
        QApplication.instance().aboutToQuit.connect(self.要退出了)

    def 要退出了(self):
        self.terminate()

    def 构建按键发送器(self):
        if 常量.系统平台 == 'Windows':
            import win32com.client as comclt
            self.按键发送器 = comclt.Dispatch("WScript.Shell")

    def 发送大写锁定键(self):
        if 常量.系统平台 == 'Windows':
            self.按键发送器.SendKeys("{CAPSLOCK}")
        else:
            self.取消监听大写锁定键()
            keyboard.press_and_release('caps lock')
            self.开始监听大写锁定键()

    def 开始监听大写锁定键(self):
        keyboard.hook_key('caps lock', self.大写锁定键被触发)

    def 取消监听大写锁定键(self):
        try:
            keyboard.unhook('caps lock')
        except:
            pass

    def 停止引擎(self):
        self.取消监听大写锁定键()
        keyboard.unhook_all()
        self.setTerminationEnabled(True)
        self.terminate()
        print('引擎已停止\n\n')
        self.正在运行 = 0

    def 得到引擎信息(self):
        数据库连接 = sqlite3.connect(常量.数据库路径)
        self.appKey, self.accessKeyId, self.accessKeySecret = 数据库连接.execute(f'''select AppKey,
                                                                    AccessKeyId,
                                                                    AccessKeySecret
                                                                from {常量.语音引擎表单名}
                                                                where 引擎名称 = :引擎名称''',
                                                     {'引擎名称': self.引擎名称}).fetchone()
        数据库连接.close()

    def 大写锁定键被触发(self, event):
        if event.event_type == "down":
            if self.识别中:
                return
            self.识别中 = True
            try:
                self.data = []
                if not self.持续录音: # 如果录音进程不是被持续开启着，那么就需要在这里主动开启
                    threading.Thread(target=self.录音线程, args=[self.p]).start()  # 开始录音
                threading.Thread(target=self.识别线程).start()  # 开始识别

            except:
                print('process 启动失败')
        elif event.event_type == "up":
            # self.访问录音数据的线程锁.acquire()
            self.识别中 = False
            # self.访问录音数据的线程锁.release()
        else:
            # print(event.event_type)
            pass

    def 为下一次输入准备识别器(self):
        self.识别器 = getAlibabaRecognizer(self.client,
                                        self.appKey,
                                        self.accessKeyId,
                                        self.accessKeySecret,
                                        self.tokenId,
                                        self.tokenExpireTime,
                                        线程=self)
        if self.识别器 == False:
            print('获取云端识别器出错\n')
            self.引擎出错信号.emit()
            return False

    def 录音线程(self, p):
        self.录音(p)

    def 识别线程(self):
        self.识别中的信号.emit()
        if not self.识别():
            self.count += 1
            self.总共写入音频片段数 = 0
            self.结束识别的信号.emit()

    def 录音(self, p):
        # print('准备录制')
        stream = p.open(channels=self.CHANNELS,
                        format=self.FORMAT,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        if self.持续录音:
            while self.isRunning():
                if self.识别中:
                    self.录音数据存入内存(stream)
                else:
                    stream.read(self.CHUNK)
        else:
            self.录音数据存入内存(stream)

        stream.stop_stream()# print('停止录制流')
        stream.close()

    def 录音数据存入内存(self, stream):
        for i in range(5):
            if not self.识别中:
                self.data = []
                # self.访问录音数据的线程锁.release()
                return
            # print(f'录音{录音写入序号}，开始写入，时间 {time.time()}')
            self.data.append(stream.read(self.CHUNK))
            # print(f'录音{录音写入序号}，写入结束，时间 {time.time()}')
            # 录音写入序号 += 1
        # 在这里录下5个小片段，大约录制了0.32秒，如果这个时候松开了大写锁定键，就不打开连接。如果还继续按着，那就开始识别。

        while self.识别中:
            # self.访问录音数据的线程锁.acquire()
            # print(f'录音{录音写入序号}，开始写入，时间 {time.time()}')
            self.data.append(stream.read(self.CHUNK))
            # print(f'录音{录音写入序号}，写入结束，时间 {time.time()}\n')
            # 录音写入序号 += 1
            # self.访问录音数据的线程锁.release()
        # self.访问录音数据的线程锁.acquire()
        time.sleep(0.0)
        self.总共写入音频片段数 = len(self.data)
        # self.访问录音数据的线程锁.release()
        self.发送大写锁定键()  # 再按下大写锁定键，还原大写锁定

    # 这边开始上传识别
    def 识别(self):
        # print('识别器开始等待')
        for i in range(5):
            time.sleep(0.06)
            if not self.识别中:
                return # 如果这个时候大写锁定键松开了  那就返回
        # print('识别器等待完闭')
        # try:
        print(self.tr('\n{}:在识别了，说完后请松开 CapsLock 键...').format(self.count))
        识别器 = self.识别器
        self.识别器 = None
        threading.Thread(target=self.为下一次输入准备识别器).start()  # 用新线程为下一次识别准备识别器
        # print('准备新的识别器')
        try:
            ret = 识别器.start() # 识别器开始识别
        except:
            print('识别器开启失败')
            return False
        if ret < 0:
            return False # 如果开始识别出错了，那就返回
        已发送音频片段数 = 0  # 对音频片段记数
        # j = 1
        当前进程测得数据片段总数 = len(self.data)
        while self.识别中 or 已发送音频片段数 < 当前进程测得数据片段总数 or 已发送音频片段数 < self.总共写入音频片段数:
            # self.访问录音数据的线程锁.acquire()
            当前进程测得数据片段总数 = len(self.data)
            # self.访问录音数据的线程锁.release()
            # print(f'       已发送音频片段数: {已发送音频片段数}, 当前进程测得数据片段总数: {当前进程测得数据片段总数}')
            if 已发送音频片段数 > 当前进程测得数据片段总数:
                return True
            elif 已发送音频片段数 == 当前进程测得数据片段总数:
                time.sleep(0.05)
            if 已发送音频片段数 < 当前进程测得数据片段总数:
                # self.访问录音数据的线程锁.acquire()
                要发送的音频数据 = self.data[已发送音频片段数]
                # self.访问录音数据的线程锁.release()
                try:
                    # print(f'       发送器{j}，开始发送，时间 {time.time()}')
                    ret = 识别器.send(要发送的音频数据) # 发送音频数据
                    # print(f'       发送器{j}，发送结束，时间 {time.time()}\n')
                    # j += 1
                except:
                    print('识别器发送失败')
                    return False
                已发送音频片段数 += 1
        # print(self.tr('\n{}:按住 CapsLock 键后开始说话...').format(self.count + 1))
        self.总共写入音频片段数 = 0
        self.结束识别的信号.emit()
        self.count += 1
        识别器.stop()
        识别器.close()
        return True


    def run(self):
        if self.正在运行 == 1: return False
        self.正在运行 = 1

        self.client = ali_speech.NlsClient()
        self.client.set_log_level('WARNING')  # 设置 client 输出日志信息的级别：DEBUG、INFO、WARNING、ERROR

        self.tokenId = 0
        self.tokenExpireTime = 0
        # try:
        self.识别器 = getAlibabaRecognizer(self.client,
                                               self.appKey,
                                               self.accessKeyId,
                                               self.accessKeySecret,
                                               self.tokenId,
                                               self.tokenExpireTime,
                                               线程=self)
        if self.识别器 == False:
            print('获取云端识别器出错\n')
            self.引擎出错信号.emit()
            return False

        self.p = pyaudio.PyAudio() # 在 QThread 中引入 PyAudio 会使得 PySide2 图形界面阻塞
        if self.持续录音:
            threading.Thread(target=self.录音线程, args=[self.p]).start()

        self.开始监听大写锁定键()

        print("""引擎初始化完成\n""")
        print('按住 CapsLock 键后开始说话...'.format(self.count))
        keyboard.wait()




