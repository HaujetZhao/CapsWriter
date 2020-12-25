# -*- coding: UTF-8 -*-
import configparser, sqlite3, json, time, sys


from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from moduels.component.NormalValue import 常量

def getAlibabaToken(accessID, accessKey, tokenId, tokenExpireTime):
    # 要是 token 还有 50 秒过期，那就重新获得一个。
    if (int(tokenExpireTime) - time.time()) < 50 :
        # 创建AcsClient实例
        client = AcsClient(
            accessID, # 填写 AccessID
            accessKey, # 填写 AccessKey = 得到AccessKey(引擎名称)
            "cn-shanghai"
            );
        # 创建request，并设置参数
        request = CommonRequest()
        request.set_method('POST')
        request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
        request.set_version('2019-02-28')
        request.set_action_name('CreateToken')
        try:
            response = json.loads(client.do_action_with_exception(request))
        except Exception as e:
            print(f'''获取 Token 出错了，出错信息如下：\n{e}\n''')
            return False, False
        tokenId = response['Token']['Id']
        tokenExpireTime = str(response['Token']['ExpireTime'])
    return tokenId, tokenExpireTime

# def 得到AccessKey(引擎名称):
#     数据库连接 = sqlite3.connect(常量.数据库路径)
#     AccessKeyId, AccessKeySecret = 数据库连接.execute(f'''select AccessKeyId,
#                                                                 AccessKeySecret
#                                                         from {常量.语音引擎表单名}
#                                                         where 引擎名称 = :引擎名称''',
#                                                  {'引擎名称': 引擎名称}).fetchone()
#     数据库连接.close()
#     return AccessKeyId, AccessKeySecret