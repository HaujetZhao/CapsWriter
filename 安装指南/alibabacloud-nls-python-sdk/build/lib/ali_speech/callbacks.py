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


class SpeechRecognizerCallback:
    """
    * @brief 调用start(), 成功与服务建立连接, sdk内部线程上报started事件
    * @note 请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_started(self, message):
        raise Exception('Not implemented!')

    """
    * @brief 设置允许返回中间结果参数, sdk在接收到服务返回到中间结果时, sdk内部线程上报ResultChanged事件
    * @note 请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_result_changed(self, message):
        raise Exception('Not implemented!')

    """
    * @brief sdk在接收到服务返回识别结束消息时, sdk内部线程上报Completed事件
    * @note 上报Completed事件之后, SDK内部会关闭识别连接通道. 此时调用send()会返回-1, 请停止发送.
    *       请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_completed(self, message):
        raise Exception('Not implemented!')

    """
    * @brief 识别过程(包含start(), send(), stop())发生异常时, sdk内部线程上报TaskFailed事件
    * @note 上报TaskFailed事件之后, SDK内部会关闭识别连接通道. 此时调用send()会返回-1, 请停止发送.
    *       请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_task_failed(self, message):
        raise Exception('Not implemented!')

    """
    * @brief 识别结束或发生异常时，会关闭websocket连接通道
    * @note 请勿在回调函数内部调用stop()操作
    * @return
    """
    def on_channel_closed(self):
        raise Exception('Not implemented!')


class SpeechTranscriberCallback:
    """
    * @brief 调用start(), 成功与服务建立连接, sdk内部线程上报started事件
    * @note 请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_started(self, message):
        raise Exception('Not implemented!')

    """
    * @brief 设置允许返回中间结果参数, sdk在接收到服务返回到中间结果时, sdk内部线程上报ResultChanged事件
    * @note 请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_result_changed(self, message):
        raise Exception('Not implemented!')

    """
    * @brief sdk在接收到服务返回的识别到一句话的开始, sdk内部线程上报SentenceBegin事件
    * @note 该事件作为检测到一句话的开始，请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_sentence_begin(self, message):
        raise Exception('Not implemented!')

    """
        * @brief sdk在接收到服务返回的识别到一句话的开始, sdk内部线程上报SentenceBegin事件
        * @note 该事件作为检测到一句话的开始，请勿在回调函数内部调用stop()操作
        * @param message 服务返回的响应
        * @return
        """
    def on_sentence_end(self, message):
        raise Exception('Not implemented!')

    """
    * @brief sdk在接收到服务返回识别结束消息时, sdk内部线程上报Completed事件
    * @note 上报Completed事件之后, SDK内部会关闭识别连接通道. 此时调用send()会返回-1, 请停止发送.
    *       请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_completed(self, message):
        raise Exception('Not implemented!')

    """
    * @brief 识别过程(包含start(), send(), stop())发生异常时, sdk内部线程上报TaskFailed事件
    * @note 上报TaskFailed事件之后, SDK内部会关闭识别连接通道. 此时调用send()会返回-1, 请停止发送.
    *       请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_task_failed(self, message):
        raise Exception('Not implemented!')

    """
    * @brief 识别结束或发生异常时，会关闭websocket连接通道
    * @note 请勿在回调函数内部调用stop()操作
    * @return
    """
    def on_channel_closed(self):
        raise Exception('Not implemented!')


class SpeechSynthesizerCallback:

    def on_binary_data_received(self, raw):
        raise Exception('Not implemented!')

    """
    * @brief sdk在接收到服务返回识别结束消息时, sdk内部线程上报Completed事件
    * @note 上报Completed事件之后, SDK内部会关闭识别连接通道. 此时调用send()会返回-1, 请停止发送.
    *       请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_completed(self, message):
        raise Exception('Not implemented!')

    """
    * @brief 识别过程(包含start(), send(), stop())发生异常时, sdk内部线程上报TaskFailed事件
    * @note 上报TaskFailed事件之后, SDK内部会关闭识别连接通道. 此时调用send()会返回-1, 请停止发送.
    *       请勿在回调函数内部调用stop()操作
    * @param message 服务返回的响应
    * @return
    """
    def on_task_failed(self, message):
        raise Exception('Not implemented!')

    """
    * @brief 识别结束或发生异常时，会关闭websocket连接通道
    * @note 请勿在回调函数内部调用stop()操作
    * @return
    """
    def on_channel_closed(self):
        raise Exception('Not implemented!')
