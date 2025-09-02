import os
import time
from urllib.parse import quote_plus

import requests
from tqdm import tqdm

API_KEY = ""
SECRET_KEY = ""


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    return str(requests.post(url, params=params).json().get("access_token"))


def main(
        input_text: str,
        voice_role: int,
        lan: str,
        save_audio_file: str,
        max_retries: int = 5,
        retry_wait: float = 2.0
):
    tex_encoded = quote_plus(input_text, encoding="utf-8")  # default is UTF-8

    url = "https://tsn.baidu.com/text2audio"
    token = get_access_token()
    cuid = "YgpG17BGGmd4xMsGHUhomKHvqu3F4xus"  # Unique user identifier, used for calculating UV (Unique Visitors).
    ctp = 1  # Client type, use fixed value 1 for web clients.
    spd = 5  # Speech speed, range 0–15. Default is 5 (medium speed).
    pit = 5  # Pitch, range 0–15. Default is 5 (medium pitch).
    vol = 5  # Volume. Basic voices: 0–9, Premium voices: 0–15. Default is 5 (medium volume). Note: 0 is the lowest volume, not silent.
    per = voice_role  # Voice selection:
    # Duxiaoyu = 1, Duxiaomei = 0, Duxiaoyao (basic) = 3, Duyaya = 4
    # Duxiaoyao (premium) = 5003, Duxiaolu = 5118, Dubowen = 106,
    # Duxiaotong = 110, Duxiaomeng = 111, Dumiduo = 103, Duxiaojiao = 5
    aue = 6  # # the format of download file, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav

    params = (
        f"tex={tex_encoded}"
        f"&tok={token}"
        f"&cuid={cuid}"
        f"&ctp={ctp}"
        f"&lan={lan}"
        f"&spd={spd}"
        f"&pit={pit}"
        f"&vol={vol}"
        f"&per={per}"
        f"&aue={aue}"
    )
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }
    response = requests.request("POST", url, headers=headers, data=params.encode('utf-8'))
    print(response.status_code)

    for attempt in range(max_retries):
        try:
            response = requests.request("POST", url, headers=headers, data=params.encode('utf-8'), timeout=20)
            print(response.status_code)

            # Check if response is audio
            if 'audio/' in response.headers.get('Content-Type', ''):
                with open(save_audio_file, "wb") as f:
                    f.write(response.content)
                print(f"Audio saved as {save_audio_file}")
                return True
            else:
                print("Error response:", response.text)
                return False
        except (requests.Timeout, requests.ConnectionError) as e:
            print(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(retry_wait)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

    print("All retries failed.")
    return False


if __name__ == '__main__':
    SAVE_ROOT = "/nas/projects/aecc/wakeup_dataset/old/exp_baidu_cloud_samples"
    list_voice = [
        0,  # Basic 度小美-标准女主播
        1,  # Basic 度小宇-亲切男声
        3,  # Basic 度逍遥-情感男声
        4,  # Basic 度丫丫-童声

        5003,  # premium 度逍遥-情感男声
        5118,  # premium 度小鹿-甜美女声
        106,  # premium 度博文-专业男主播
        103,  # premium 度米朵-可爱童声
        110,  # premium 度小童-童声主播
        111,  # premium 度小萌-软萌妹子
        5,  # premium 度小娇-成熟女主播
        # check more voice type details https://ai.baidu.com/ai-doc/SPEECH/Rluv3uq3d
    ]

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
    lan = "zh"  # Fixed value "zh". Language selection (Chinese).

    for voice_role in tqdm(list_voice):
        save_dir = os.path.join(SAVE_ROOT, f"voice_{voice_role}")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
            print(save_dir)
        for idx, input_text in enumerate(tqdm(list_texts, total=num_samples)):
            save_audio_file = os.path.join(save_dir, f"output_{lan}_{idx}.wav")
            if os.path.exists(save_audio_file):
                print(f"Audio file already exists {save_audio_file}!")
            else:
                success = False
                while not success:
                    success = main(
                        input_text=input_text,
                        voice_role=voice_role,
                        lan=lan,
                        save_audio_file=save_audio_file
                    )
