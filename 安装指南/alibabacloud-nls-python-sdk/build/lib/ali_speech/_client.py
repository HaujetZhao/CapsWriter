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

import websocket

try:
    import thread
except ImportError:
    import _thread as thread

from ali_speech._logging import _log
from ali_speech._create_token import AccessToken
from ali_speech._speech_recognizer import SpeechRecognizer
from ali_speech._speech_transcriber import SpeechTranscriber
from ali_speech._speech_synthesizer import SpeechSynthesizer

__all__ = ["NlsClient"]


class NlsClient:
    URL_GATEWAY = 'wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1'

    def __init__(self):
        websocket.enableTrace(False)

    @staticmethod
    def set_log_level(level):
        _log.setLevel(level)

    @staticmethod
    def create_token(access_key_id, access_key_secret):
        return AccessToken.create_token(access_key_id, access_key_secret)

    def create_recognizer(self, callback, gateway_url=URL_GATEWAY):
        request = SpeechRecognizer(callback, gateway_url)
        return request

    def create_transcriber(self, callback, gateway_url=URL_GATEWAY):
        transcriber = SpeechTranscriber(callback, gateway_url)
        return transcriber

    def create_synthesizer(self, callback, gateway_url=URL_GATEWAY):
        synthesizer = SpeechSynthesizer(callback, gateway_url)
        return synthesizer
