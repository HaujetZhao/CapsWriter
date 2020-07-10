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

from ali_speech._constant import Status
from ali_speech._constant import Constant


class SpeechReqProtocol:
    def __init__(self, callback, url):
        self._header = {}
        self._context = {}
        self._payload = {}
        self._token = None
        self._gateway_url = url
        self._callback = callback
        self._status = Status.STATUS_INIT
        self._ws = None
        self._thread = None
        self._task_id = None

        sdk_info = {Constant.CONTEXT_SDK_KEY_NAME: Constant.CONTEXT_SDK_VALUE_NAME,
                    Constant.CONTEXT_SDK_KEY_VERSION: Constant.CONTEXT_SDK_VALUE_VERSION}
        self._context[Constant.CONTEXT_SDK_KEY] = sdk_info

    def set_appkey(self, appkey):
        self._header[Constant.HEADER_KEY_APPKEY] = appkey

    def get_appkey(self):
        return self._header[Constant.HEADER_KEY_APPKEY]

    def set_token(self, token):
        self._token = token

    def get_token(self):
        return self._token

    def set_format(self, format):
        self._payload[Constant.PAYLOAD_KEY_FORMAT] = format

    def get_format(self):
        return self._payload[Constant.PAYLOAD_KEY_FORMAT]

    def set_sample_rate(self, sample_rate):
        self._payload[Constant.PAYLOAD_KEY_SAMPLE_RATE] = sample_rate

    def get_sample_rate(self):
        return self._payload[Constant.PAYLOAD_KEY_SAMPLE_RATE]

    def get_task_id(self):
        return self._header[Constant.HEADER_KEY_TASK_ID]

    def put_context(self, key, obj):
        self._context[key] = obj

    def add_payload_param(self, key, obj):
        self._payload[key] = obj

    def get_status(self):
        return self._status

    def serialize(self):
        root = {Constant.HEADER: self._header}

        if len(self._payload) != 0:
            root[Constant.CONTEXT] = self._context
            root[Constant.PAYLOAD] = self._payload

        return json.dumps(root)
