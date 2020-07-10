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

import time
import ali_speech

if __name__ == "__main__":
    ali_speech.NlsClient.set_log_level('INFO')
    # 用户信息
    access_key_id = '您的AccessKeyId'
    access_key_secret = '您的AccessKeySecret'
    token, expire_time = ali_speech.NlsClient.create_token(access_key_id, access_key_secret)
    print('token: %s, expire time(s): %s' % (token, expire_time))
    if expire_time:
        print('token有效期的北京时间：%s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expire_time))))
