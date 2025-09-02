# -*- coding: utf-8 -*-

import json
import os.path
import types
import time
import base64
from tqdm import tqdm
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tts.v20190823 import tts_client, models

SAVE_ROOT = "/nas/projects/aecc/wakeup_dataset/old/exp_tencent_cloud_samples"
list_texts = [
    "草地上布满了小T小T的印子，像是谁掉了玩具。",
    "他画了一张图，上面全是小T小T的符号，密密麻麻的。",
    "这件衣服上的图案都是小T小T的，很特别。",
    "小T小T的铁钉整齐地排成一排，看着真舒服。",
    "他设计了一种新字体，每个字母都有点小T小T的感觉。",
    "远处的电线杆看上去一个个像小T小T地立在田野里。",
    "她在纸上随手画了些小T小T的图案，竟然成了一幅作品。",
    "我记得那款游戏里有一种小T小T的敌人，很难打。",
    "孩子们把积木拼成了一排小T小T的形状，非常可爱。",
    "天花板上吊着很多小T小T的装饰品，在灯光下闪闪发亮。",
]
num_samples = len(list_texts)

list_voice = [
    # 10510000,  # - zhixiaoyao(Chinese)
    # 1001,  # - zhiyu(Chinese)
    1002,  # - zhiling(Chinese)
    1003,  # - zhimei(Chinese)
    1004,  # - zhiyun(Chinese)
    1005,  # - zhili(Chinese)
    1007,  # - zhina(Chinese)
    1008,  # - zhiqi(Chinese)
    1009,  # - zhiyun(Chinese)
    1010,  # - zhihua(Chinese)
    1017,  # - zhirong(Chinese)
    1018,  # - zhijing(Chinese)
]
for voice_role in tqdm(list_voice):
    save_dir = os.path.join(SAVE_ROOT, f"voice_{voice_role}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(save_dir)
    for idx, s_text in enumerate(tqdm(list_texts, total=num_samples)):
        while True:
            try:
                session_uuid = f"pl_{voice_role}_{idx}"
                save_audio_file = os.path.join(save_dir, f"output_{session_uuid}.wav")
                if os.path.exists(save_audio_file):
                    print(f"Audio file already exists {save_audio_file}!")
                    break

                # Required steps:
                # Instantiate an authentication object. The Tencent Cloud account key pair `secretId` and `secretKey` need to be passed in as the input parameters
                # This example uses the way to read from the environment variable, so you need to set these two values in the environment variable in advance
                # You can also write the key pair directly into the code, but be careful not to copy, upload, or share the code to others
                # Query the CAM key: https://console.tencentcloud.com/capi
                cred = credential.Credential(
                    # @TODO: Add here your API key and Secret Key
                    secret_id="",
                    secret_key=""
                )
                # Using an ephemeral key example
                # cred = credential.Credential("SecretId", "SecretKey", "Token")
                # Instantiate an HTTP option (optional; skip if there are no special requirements)
                httpProfile = HttpProfile()
                httpProfile.endpoint = "tts.intl.tencentcloudapi.com"
                # httpProfile.endpoint = "tts.ap-guangzhou.tencentcloudapi.com"

                # Optional steps:
                # Instantiate a client configuration object. You can specify the timeout period and other configuration items
                clientProfile = ClientProfile()
                clientProfile.httpProfile = httpProfile
                # Instantiate an client object
                # The second parameter is the region information. You can directly enter the string "ap-guangzhou" or import the preset constant
                client = tts_client.TtsClient(cred, "ap-singapore", clientProfile)
                # client = tts_client.TtsClient(cred, "ap-guangzhou", clientProfile)

                # Instantiate a request object. You can further set the request parameters according to the API called and actual conditions
                req = models.TextToVoiceRequest()
                params = {
                    "Text": s_text,
                    "SessionId": session_uuid,
                    "Volume": 10,
                    "ModelType": 1,
                    "VoiceType": voice_role,
                    "PrimaryLanguage": 1,
                }
                req.from_json_string(json.dumps(params))

                # The returned "resp" is an instance of the TextToVoiceResponse class which corresponds to the request object
                resp = client.TextToVoice(req)
                # A string return packet in JSON format is output
                # print(resp.to_json_string())

                # Your Base64-encoded audio string
                audio_base64 = resp.Audio

                # Decode the Base64 string
                audio_bytes = base64.b64decode(audio_base64)

                # Save as .wav file
                with open(save_audio_file, "wb") as f:
                    f.write(audio_bytes)

                print(f"Audio saved as {save_audio_file}")
                break  # Exit the retry loop if successful

            except TencentCloudSDKException as err:
                print(f"Error occurred (retrying): {err}")
                time.sleep(2)  # Add a short delay before retrying to avoid hammering the API
