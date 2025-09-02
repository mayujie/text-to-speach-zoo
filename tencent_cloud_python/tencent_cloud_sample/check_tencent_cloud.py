# -*- coding: utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# Import the client models of the corresponding product module.
from tencentcloud.cvm.v20170312 import cvm_client, models
try:
    # Instantiate an authentication object. The Tencent Cloud account secretId and secretKey need to be passed in as the input parameters.
    cred = credential.Credential(
        "",
        ""
    )

    # Instantiate the client object to request the product (with CVM as an example).
    client = cvm_client.CvmClient(cred, "ap-shanghai")

    # Instantiate a request object.
    req = models.DescribeZonesRequest()

    # Call the API you want to access through the client object; you need to pass in the request object.
    resp = client.DescribeZones(req)
    # A string return packet in json format is output.
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)