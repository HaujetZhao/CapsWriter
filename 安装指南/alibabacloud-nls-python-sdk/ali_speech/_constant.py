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


class Status:
    # 初始状态
    STATUS_INIT = 1
    # websocker 网络连接建立成功，on_open
    STATUS_WS_CONNECTED = 2
    # 与gateway服务建立连接中
    STATUS_STARTING = 3
    # 与服务建立连接成功，on_message RecognitionStarted
    STATUS_STARTED = 4
    # 客户端正主动断开连接
    STATUS_STOPPING = 5
    # 与服务已断开连接
    STATUS_STOPPED = 6
    # 开启VAD，服务主动返回completed事件
    STATUS_COMPLETED_WITH_OUT_STOP = 7


class Constant:
    CONTEXT = 'context'
    CONTEXT_SDK_KEY = 'sdk'
    CONTEXT_SDK_KEY_NAME = 'name'
    CONTEXT_SDK_VALUE_NAME = 'nls-sdk-python'
    CONTEXT_SDK_KEY_VERSION = 'version'
    CONTEXT_SDK_VALUE_VERSION = '2.0.1'

    HEADER_TOKEN = 'X-NLS-Token'

    HEADER = 'header'
    HEADER_KEY_NAMESPACE = 'namespace'
    HEADER_KEY_NAME = 'name'
    HEADER_KEY_MESSAGE_ID = 'message_id'
    HEADER_KEY_APPKEY = 'appkey'
    HEADER_KEY_TASK_ID = 'task_id'
    HEADER_KEY_STATUS = 'status'
    HEADER_KEY_STATUS_TEXT = 'status_text'

    PAYLOAD = 'payload'
    PAYLOAD_KEY_SAMPLE_RATE = 'sample_rate'
    PAYLOAD_KEY_FORMAT = 'format'
    PAYLOAD_KEY_ENABLE_ITN = 'enable_inverse_text_normalization'
    PAYLOAD_KEY_ENABLE_INTERMEDIATE_RESULT = 'enable_intermediate_result'
    PAYLOAD_KEY_ENABLE_PUNCTUATION_PREDICTION = 'enable_punctuation_prediction'

    PAYLOAD_KEY_VOICE = 'voice'
    PAYLOAD_KEY_TEXT = 'text'
    PAYLOAD_KEY_VOLUME = 'volume'
    PAYLOAD_KEY_SPEECH_RATE = 'speech_rate'
    PAYLOAD_KEY_PITCH_RATE = 'pitch_rate'

    HEADER_VALUE_ASR_NAMESPACE = 'SpeechRecognizer'
    HEADER_VALUE_ASR_NAME_START = 'StartRecognition'
    HEADER_VALUE_ASR_NAME_STOP = 'StopRecognition'
    HEADER_VALUE_ASR_NAME_STARTED = 'RecognitionStarted'
    HEADER_VALUE_ASR_NAME_RESULT_CHANGED = 'RecognitionResultChanged'
    HEADER_VALUE_ASR_NAME_COMPLETED = 'RecognitionCompleted'

    HEADER_VALUE_NAME_TASK_FAILED = 'TaskFailed'

    HEADER_VALUE_TRANS_NAMESPACE = 'SpeechTranscriber'
    HEADER_VALUE_TRANS_NAME_START = 'StartTranscription'
    HEADER_VALUE_TRANS_NAME_STOP = 'StopTranscription'
    HEADER_VALUE_TRANS_NAME_STARTED = 'TranscriptionStarted'
    HEADER_VALUE_TRANS_NAME_SENTENCE_BEGIN = 'SentenceBegin'
    HEADER_VALUE_TRANS_NAME_SENTENCE_END = 'SentenceEnd'
    HEADER_VALUE_TRANS_NAME_RESULT_CHANGE = 'TranscriptionResultChanged'
    HEADER_VALUE_TRANS_NAME_COMPLETED = 'TranscriptionCompleted'

    HEADER_VALUE_TTS_NAMESPACE = 'SpeechSynthesizer'
    HEADER_VALUE_TTS_NAME_START = 'StartSynthesis'
    HEADER_VALUE_TTS_NAME_COMPLETED = 'SynthesisCompleted'

