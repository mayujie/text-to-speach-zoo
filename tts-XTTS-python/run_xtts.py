import os
import torch
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig

# torch.serialization.add_safe_globals([XttsConfig])
torch.serialization._DEFAULT_LOAD_WEIGHTS_ONLY = False
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

texts = [
    "年轻的时候你总想要最好的，但年华老去，你不得不选一些便宜货。",
    "闻着是肉味，吃在嘴里就成毒药了。",
    "有些朋友常是一闪而过，就像路上的行人。",
    "你朋友不及格，你感觉很糟；你朋友考第一，你感觉更糟。",
    "女人和小孩能够粗心大意，但男人不行。",
    "我不知道将去何方，但我已在路上。",
    "世界上有太多孤独的人，害怕先踏出第一步。",
    "我表现得我不喜欢任何事物，是因为我从来没得到过我想要的。",
    "如果你不出去走走，就会以为眼前的就是全世界。",
    "当你挽救了一条生命就等于挽救了全世界。",
]

speakers = [
    "speaker_clone_file/tts_output_6_aifei.wav",
    "speaker_clone_file/tts_output_6_jielidou.wav",
    "speaker_clone_file/tts_output_6_yina.wav",
    "speaker_clone_file/tts_output_6_aihao.wav",
]

result_dir = "/nas/projects/md/data/open_tts_results/output_xtts/results_xtts"

for speaker_sample in speakers:
    speaker_role = os.path.splitext(os.path.basename(speaker_sample))[0]
    result_dir_new = result_dir + f"_{speaker_role}"
    if not os.path.exists(result_dir_new):
        os.makedirs(result_dir_new)
    for idx, s_text in enumerate(texts):
        tts.tts_to_file(
            # text="It took me quite a long time to develop a voice, and now that I have it I'm not going to be silent.",
            text=s_text,
            speaker_wav=speaker_sample,
            language="zh-cn",
            # language="en",
            file_path=os.path.join(result_dir_new, f"output_{idx}.wav")
        )
