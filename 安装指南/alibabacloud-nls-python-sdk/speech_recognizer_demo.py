# -*- coding: utf-8 -*-

"""
 * Copyright 2015 Alibaba Group Holding Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

import os
import time
import threading
import ali_speech
from ali_speech.callbacks import SpeechRecognizerCallback
from ali_speech.constant import ASRFormat
from ali_speech.constant import ASRSampleRate


class MyCallback(SpeechRecognizerCallback):
    """
    构造函数的参数没有要求，可根据需要设置添加
    示例中的name参数可作为待识别的音频文件名，用于在多线程中进行区分
    """
    def __init__(self, name='default'):
        self._name = name

    def on_started(self, message):
        print('MyCallback.OnRecognitionStarted: %s' % message)

    def on_result_changed(self, message):
        print('MyCallback.OnRecognitionResultChanged: file: %s, task_id: %s, result: %s' % (
            self._name, message['header']['task_id'], message['payload']['result']))

    def on_completed(self, message):
        print('MyCallback.OnRecognitionCompleted: file: %s, task_id:%s, result:%s' % (
            self._name, message['header']['task_id'], message['payload']['result']))

    def on_task_failed(self, message):
        print('MyCallback.OnRecognitionTaskFailed: %s' % message)

    def on_channel_closed(self):
        print('MyCallback.OnRecognitionChannelClosed')


def process(client, appkey, token):
    audio_name = 'nls-sample-16k.wav'
    callback = MyCallback(audio_name)
    recognizer = client.create_recognizer(callback)
    recognizer.set_appkey(appkey)
    recognizer.set_token(token)
    recognizer.set_format(ASRFormat.PCM)
    recognizer.set_sample_rate(ASRSampleRate.SAMPLE_RATE_16K)
    recognizer.set_enable_intermediate_result(False)
    recognizer.set_enable_punctuation_prediction(True)
    recognizer.set_enable_inverse_text_normalization(True)

    try:
        ret = recognizer.start()
        if ret < 0:
            return ret

        print('sending audio...')
        with open(audio_name, 'rb') as f:
            audio = f.read(3200)
            while audio:
                ret = recognizer.send(audio)
                if ret < 0:
                    break
                time.sleep(0.1)
                audio = f.read(3200)

        recognizer.stop()
    except Exception as e:
        print(e)
    finally:
        recognizer.close()


def process_multithread(client, appkey, token, number):
    thread_list = []
    for i in range(0, number):
        thread = threading.Thread(target=process, args=(client, appkey, token))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
    client = ali_speech.NlsClient()
    # 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR
    client.set_log_level('INFO')

    appkey = '您的appkey'
    token = '您的Token'

    process(client, appkey, token)

    # 多线程示例
    # process_multithread(client, appkey, token, 10)




