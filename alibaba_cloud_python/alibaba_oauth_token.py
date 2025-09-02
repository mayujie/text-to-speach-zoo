#! /usr/bin/env python
# coding=utf-8
import os
import time
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def get_alibaba_token():
    # @TODO: Add here your API key and Secret Key
    os.environ["ALIYUN_AK_ID"] = ""
    os.environ["ALIYUN_AK_SECRET"] = ""

    # 创建AcsClient实例
    client = AcsClient(
        ak=os.getenv('ALIYUN_AK_ID'),
        secret=os.getenv('ALIYUN_AK_SECRET'),
        region_id="cn-shanghai"
    )

    # 创建request，并设置参数。
    request = CommonRequest()
    request.set_method('POST')
    request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request.set_version('2019-02-28')
    request.set_action_name('CreateToken')

    try:
        response = client.do_action_with_exception(request)
        print(response)

        jss = json.loads(response)
        if 'Token' in jss and 'Id' in jss['Token']:
            token = jss['Token']['Id']
            expireTime = jss['Token']['ExpireTime']
            print("token = " + token)
            print("expireTime = " + str(expireTime))
            return token

    except Exception as e:
        print(e)


if __name__ == "__main__":
    alibaba_token = get_alibaba_token()
    print(alibaba_token)
