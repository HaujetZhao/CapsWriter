# -*- coding: UTF-8 -*-
import configparser, sqlite3, json

from ali_speech.constant import ASRFormat
from ali_speech.constant import ASRSampleRate

from moduels.component.NormalValue import 常量
from moduels.component.Ali_CallBack import Ali_Callback
from moduels.function.getAlibabaToken import getAlibabaToken

def getAlibabaRecognizer(client, appkey, accessKeyId, accessKeySecret, tokenId, tokenExpireTime, 线程):
    tokenId, tokenExpireTime = getAlibabaToken(accessKeyId, accessKeySecret, tokenId, tokenExpireTime)
    if tokenId == False: return False
    线程.tokenId = tokenId
    线程.tokenExpireTime = tokenExpireTime
    audio_name = 'none'
    callback = Ali_Callback(audio_name)
    recognizer = client.create_recognizer(callback)
    recognizer.set_appkey(appkey)
    recognizer.set_token(tokenId)
    recognizer.set_format(ASRFormat.PCM)
    recognizer.set_sample_rate(ASRSampleRate.SAMPLE_RATE_16K)
    recognizer.set_enable_intermediate_result(False)
    recognizer.set_enable_punctuation_prediction(True)
    recognizer.set_enable_inverse_text_normalization(True)
    return (recognizer)