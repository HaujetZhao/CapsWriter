# -*- coding: UTF-8 -*-
import json
import os
import pyaudio
import threading
import keyboard
import time

from ali_speech.callbacks import SpeechRecognizerCallback

class Ali_Callback(SpeechRecognizerCallback):
    """
    构造函数的参数没有要求，可根据需要设置添加
    示例中的name参数可作为待识别的音频文件名，用于在多线程中进行区分
    """
    def __init__(self, name='default'):
        self._name = name
    def on_started(self, message):
        #print('MyCallback.OnRecognitionStarted: %s' % message)
        pass
    def on_result_changed(self, message):
        print('任务信息: task_id: %s, result: %s' % (
            message['header']['task_id'], message['payload']['result']))
    def on_completed(self, message):
        print('结果: %s' % (
            message['payload']['result']))
        result = message['payload']['result']
        try:
            if result[-1] == '。': # 如果最后一个符号是句号，就去掉。
                result = result[0:-1]
        except Exception as e:
            pass
        keyboard.write(result)  # 输入识别结果
    def on_task_failed(self, message):
        print('MyCallback.OnRecognitionTaskFailed: %s' % message)
    def on_channel_closed(self):
        # print('MyCallback.OnRecognitionChannelClosed')
        pass