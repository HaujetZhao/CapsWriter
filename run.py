import json
import os
import pyaudio
import threading
import keyboard

import time
import ali_speech
from ali_speech.callbacks import SpeechRecognizerCallback
from ali_speech.constant import ASRFormat
from ali_speech.constant import ASRSampleRate

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import configparser

""" 在这里填写你的 API 设置 """
accessID = "xxxxxxxxxxxxxxxxxxxxxxxx"
accessKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
appkey = 'xxxxxxxxxxxxxxxx'


"""pyaudio参数"""
CHUNK = 1024    # 数据包或者数据片段
FORMAT = pyaudio.paInt16    # pyaudio.paInt16表示我们使用量化位数 16位来进行录音
CHANNELS = 1    # 声道，1为单声道，2为双声道
RATE = 16000    # 采样率，每秒钟16000次

count = 1   # 计数
pre = True  # 是否准备开始录音
run = False  # 控制录音是否停止


class MyCallback(SpeechRecognizerCallback):
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
        if result[-1] == '。': # 如果最后一个符号是句号，就去掉。
            result = result[0:-1]
        keyboard.write(result) # 输入识别结果
        keyboard.press_and_release('caps lock') # 再按下大写锁定键，还原大写锁定
    def on_task_failed(self, message):
        print('MyCallback.OnRecognitionTaskFailed: %s' % message)
    def on_channel_closed(self):
        # print('MyCallback.OnRecognitionChannelClosed')
        pass

def get_token():
    if not os.path.exists('token.ini'):
        init_id = """[Token]
id = 0000000000000000000
expiretime = 0000000000"""
        fp = open("token.ini",'w')
        fp.write(init_id)
        fp.close()

    config = configparser.ConfigParser()
    config.read_file(open('token.ini'))
    token = config.get("Token","Id")
    expireTime = config.get("Token","ExpireTime")
    # 要是 token 还有 5 秒过期，那就重新获得一个。
    if (int(expireTime) - time.time()) < 5 :
        # 创建AcsClient实例
        global accessID, accessKey
        client = AcsClient(
        accessID, # 填写 AccessID
        accessKey, # 填写 AccessKey
        "cn-shanghai"
        );
        # 创建request，并设置参数
        request = CommonRequest()
        request.set_method('POST')
        request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
        request.set_version('2019-02-28')
        request.set_action_name('CreateToken')
        response = json.loads(client.do_action_with_exception(request))
        token = response['Token']['Id']
        expireTime = str(response['Token']['ExpireTime'])
        config.set('Token', 'Id', token)
        config.set('Token', 'ExpireTime', expireTime)
        config.write(open("token.ini", "w"))
        print
    return token

def get_recognizer(client, appkey):
    token = get_token()
    audio_name = 'none'
    callback = MyCallback(audio_name)
    recognizer = client.create_recognizer(callback)
    recognizer.set_appkey(appkey)
    recognizer.set_token(token)
    recognizer.set_format(ASRFormat.PCM)
    recognizer.set_sample_rate(ASRSampleRate.SAMPLE_RATE_16K)
    recognizer.set_enable_intermediate_result(False)
    recognizer.set_enable_punctuation_prediction(True)
    recognizer.set_enable_inverse_text_normalization(True)
    return(recognizer)

# 因为关闭 recognizer 有点慢，就须做成一个函数，用多线程关闭它。
def close_recognizer():
    global recognizer
    recognizer.close()

# 处理热键响应
def on_hotkey(event):
    global pre, run
    if event.event_type == "down":
        if pre and (not run):
            pre = False
            run = True
            threading.Thread(target=process).start()
        else:
            pass
    else:
        pre, run = True, False

# 处理是否开始录音
def process():
    global run
    # 等待 6 轮 0.05 秒，如果 run 还是 True，就代表还没有松开大写键，是在长按状态，那么就可以开始识别。
    for i in range(6):
        if run:
            time.sleep(0.05)
        else:
            return
    global count, recognizer, p, appkey
    threading.Thread(target=recoder,args=(recognizer, p)).start()      # 开始录音识别
    count += 1
    recognizer = get_recognizer(client, appkey) # 为下一次监听提前准备好 recognizer

# 录音识别处理
def recoder(recognizer, p):
    global run
    try:
        stream = p.open(channels=CHANNELS,
                format=FORMAT,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
        print('\r{}//:在听了，说完了请松开 CapsLock 键...'.format(count), end=' ')
        ret = recognizer.start()
        if ret < 0:
            return ret
        while run:
            data = stream.read(CHUNK)
            ret = recognizer.send(data)
            if ret < 0:
                break
        recognizer.stop()
        stream.stop_stream()
        stream.close()
        # p.terminate()
    except Exception as e:
        print(e)
    finally:
        threading.Thread(target=close_recognizer).start()    # 关闭 recognizer
    print('{}//:按住 CapsLock 键 0.3 秒后开始说话...'.format(count), end=' ')



if __name__ == '__main__':

    print('开始程序')

    client = ali_speech.NlsClient()
    client.set_log_level('WARNING') # 设置 client 输出日志信息的级别：DEBUG、INFO、WARNING、ERROR

    recognizer = get_recognizer(client, appkey)
    p = pyaudio.PyAudio()

    keyboard.hook_key('caps lock', on_hotkey)
    print('{}//:按住 CapsLock 键 0.3 秒后开始说话...'.format(count), end=' ')
    keyboard.wait()
    


    
    