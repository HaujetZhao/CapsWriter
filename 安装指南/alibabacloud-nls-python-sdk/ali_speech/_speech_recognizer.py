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

import json
import six
import websocket
import uuid
import threading
import time

from ali_speech._logging import _log
from ali_speech._constant import Status
from ali_speech._constant import Constant
from ali_speech._speech_reqprotocol import SpeechReqProtocol


class SpeechRecognizer(SpeechReqProtocol):

    def __init__(self, callback, url):
        super(SpeechRecognizer, self).__init__(callback, url)
        self._last_start_retry = False
        self._is_connected = False

        self._header[Constant.HEADER_KEY_NAMESPACE] = Constant.HEADER_VALUE_ASR_NAMESPACE
        self._payload[Constant.PAYLOAD_KEY_FORMAT] = "pcm"
        self._payload[Constant.PAYLOAD_KEY_SAMPLE_RATE] = 16000

    def set_enable_intermediate_result(self, flag):
        self._payload[Constant.PAYLOAD_KEY_ENABLE_INTERMEDIATE_RESULT] = flag

    def set_enable_punctuation_prediction(self, flag):
        self._payload[Constant.PAYLOAD_KEY_ENABLE_PUNCTUATION_PREDICTION] = flag

    def set_enable_inverse_text_normalization(self, flag):
        self._payload[Constant.PAYLOAD_KEY_ENABLE_ITN] = flag

    def start(self, ping_interval=5, ping_timeout=3):
        """
        开始识别，新建到服务端的连接
        :param ping_interval: 自动发送ping命令，指定发送间隔，单位为秒
        :param ping_timeout: 等待接收pong消息的超时时间，单位为秒
        :return: 与服务端建立连接成功，返回0
                 与服务端建立连接失败，返回-1
        """
        if self._status == Status.STATUS_INIT:
            _log.debug('starting recognizer...')
            self._status = Status.STATUS_STARTING
        else:
            _log.error("Illegal status: %s" % self._status)
            return -1

        def _on_open(ws):
            _log.debug('websocket connected')
            self._status = Status.STATUS_WS_CONNECTED
            self._is_connected = True
            msg_id = six.u(uuid.uuid1().hex)
            self._task_id = six.u(uuid.uuid1().hex)
            self._header[Constant.HEADER_KEY_NAME] = Constant.HEADER_VALUE_ASR_NAME_START
            self._header[Constant.HEADER_KEY_MESSAGE_ID] = msg_id
            self._header[Constant.HEADER_KEY_TASK_ID] = self._task_id

            text = self.serialize()
            _log.info('sending start cmd: ' + text)
            ws.send(text)

        def _on_message(ws, raw):
            _log.debug('websocket message received: ' + raw)
            msg = json.loads(raw)
            name = msg[Constant.HEADER][Constant.HEADER_KEY_NAME]
            if name == Constant.HEADER_VALUE_ASR_NAME_STARTED:
                self._status = Status.STATUS_STARTED
                _log.debug('callback on_started')
                self._callback.on_started(msg)
            elif name == Constant.HEADER_VALUE_ASR_NAME_RESULT_CHANGED:
                _log.debug('callback on_result_changed')
                self._callback.on_result_changed(msg)
            elif name == Constant.HEADER_VALUE_ASR_NAME_COMPLETED:
                if self._status == Status.STATUS_STOPPING:
                    # 客户端主动调用stop返回的completed事件
                    self._status = Status.STATUS_STOPPED
                else:
                    # 开启VAD，服务端主动返回的completed事件
                    self._status = Status.STATUS_COMPLETED_WITH_OUT_STOP

                _log.debug('websocket status changed to stopped')
                _log.debug('callback on_completed')
                self._callback.on_completed(msg)
            elif name == Constant.HEADER_VALUE_NAME_TASK_FAILED:
                self._status = Status.STATUS_STOPPED
                _log.error(msg)
                _log.debug('websocket status changed to stopped')
                _log.debug('callback on_task_failed')
                self._callback.on_task_failed(msg)

        def _on_close(ws):
            _log.debug('callback on_channel_closed')
            self._callback.on_channel_closed()

        def _on_error(ws, error):
            if self._is_connected or self._last_start_retry:
                _log.error(error)
                self._status = Status.STATUS_STOPPED
                message = json.loads('{"header":{"namespace":"Default","name":"TaskFailed",'
                                     '"status":400,"message_id":"0","task_id":"0",'
                                     '"status_text":"%s"}}'
                                     % error)
                self._callback.on_task_failed(message)
            else:
                _log.warning('retry start: %s' % error)

        retry_count = 3
        for count in range(retry_count):
            self._status = Status.STATUS_STARTING
            if count == (retry_count - 1):
                self._last_start_retry = True

            # Init WebSocket
            self._ws = websocket.WebSocketApp(self._gateway_url,
                                              on_open=_on_open,
                                              on_message=_on_message,
                                              on_error=_on_error,
                                              on_close=_on_close,
                                              header={Constant.HEADER_TOKEN: self._token})

            self._thread = threading.Thread(target=self._ws.run_forever,
                                            args=(None, None, ping_interval, ping_timeout))
            self._thread.daemon = True
            self._thread.start()
            # waite for no more than 10 seconds
            for i in range(1000):
                if self._status == Status.STATUS_STARTED or self._status == Status.STATUS_STOPPED:
                    break
                else:
                    time.sleep(0.01)

            if self._status == Status.STATUS_STARTED:
                # 与服务端连接建立成功
                _log.debug('start succeed!')
                return 0
            else:
                if self._is_connected or self._last_start_retry:
                    # 已建立了WebSocket链接但是与服务端的连接失败， 或者是最后一次重试，则返回-1
                    _log.error("start failed, status: %s" % self._status)
                    return -1
                else:
                    # 尝试重连
                    continue

    def send(self, audio_data):
        """
        发送语音数据到服务端，建议每次发送 1000 ~ 8000 字节
        :param audio_data: 二进制音频数据
        :return: 发送成功，返回0
                 发送失败，返回-1
        """
        if self._status == Status.STATUS_STARTED:
            self._ws.send(audio_data, opcode=websocket.ABNF.OPCODE_BINARY)
            return 0
        elif self._status == Status.STATUS_COMPLETED_WITH_OUT_STOP:
            _log.info('the recognizer finished with VAD, no need to send data anymore!')
            return -1
        else:
            _log.error('should not send data in state %d', self._status)
            return -1

    def stop(self):
        """
        结束识别并关闭与服务端的连接
        :return: 关闭成功，返回0
                 关闭失败，返回-1
        """
        ret = 0
        if self._status == Status.STATUS_COMPLETED_WITH_OUT_STOP:
            _log.info('the recognizer finished with VAD')
            ret = 0
        elif self._status == Status.STATUS_STARTED:
            self._status = Status.STATUS_STOPPING
            msg_id = six.u(uuid.uuid1().hex)
            self._header[Constant.HEADER_KEY_NAME] = Constant.HEADER_VALUE_ASR_NAME_STOP
            self._header[Constant.HEADER_KEY_MESSAGE_ID] = msg_id
            self._payload.clear()
            text = self.serialize()
            _log.info('sending stop cmd: ' + text)
            self._ws.send(text)

            for i in range(100):
                if self._status == Status.STATUS_STOPPED:
                    break
                else:
                    time.sleep(0.1)
                    _log.debug('waite 100ms')

            if self._status != Status.STATUS_STOPPED:
                ret = -1
            else:
                ret = 0
        else:
            _log.error('should not stop in state %d', self._status)
            ret = -1

        return ret

    def close(self):
        """
        关闭WebSocket链接
        """
        if self._ws:
            if self._thread and self._thread.is_alive():
                self._ws.keep_running = False
                self._thread.join()
            self._ws.close()

