#  DashScope SDK 版本不低于 1.24.6
import os
import time
os.environ["DASHSCOPE_API_KEY"] = ""

import requests
import dashscope

voice_roles = [
    # Qwen3-tts roles https://help.aliyun.com/zh/model-studio/qwen-tts#1e9f1d69e21jg
    "Cherry",
    "Ethan",
    "Nofish",
    "Jennifer",
    "Ryan",
    "Katerina",
    "Elias",
    "Dylan"
]

texts = [
    "年轻的时候你总想要最好的，但年华老去，你不得不选一些便宜货。",
    "那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。",
    "有些朋友常是一闪而过，就像路上的行人。",
    "你朋友不及格，你感觉很糟；你朋友考第一，你感觉更糟。",
    "女人和小孩能够粗心大意，但男人不行。",
    "我不知道将去何方，但我已在路上。",
    "世界上有太多孤独的人，害怕先踏出第一步。",
    "我表现得我不喜欢任何事物，是因为我从来没得到过我想要的。",
    "如果你不出去走走，就会以为眼前的就是全世界。",
    "当你挽救了一条生命就等于挽救了全世界。",
]
result_dir = "/nas/projects/md/data/open_tts_results/output_Qwen3_tts/results"

for role in voice_roles:
    result_dir_new = result_dir + f"_{role}"
    if not os.path.exists(result_dir_new):
        os.makedirs(result_dir_new)

    for idx, s_text in enumerate(texts):
        # SpeechSynthesizer接口使用方法：dashscope.audio.qwen_tts.SpeechSynthesizer.call(...)
        response = dashscope.MultiModalConversation.call(
            model="qwen3-tts-flash",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            text=s_text,
            voice=role,
            # Chinese、English、German、Italian、Portuguese、Spanish、Japanese、Korean、French、Russian、Auto
            language_type="Chinese",  # 建议与文本语种一致，以获得正确的发音和自然的语调。
            stream=False
        )
        audio_url = response.output.audio.url
        save_path = os.path.join(result_dir_new, f"output_{idx}.wav")  # 自定义保存路径
        print(f"[WARN] Retrying {save_path} in 3 seconds... ")
        time.sleep(3)

        try:
            response = requests.get(audio_url)
            response.raise_for_status()  # 检查请求是否成功
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"音频文件已保存至：{save_path}")
        except Exception as e:
            print(f"下载失败：{str(e)}")
