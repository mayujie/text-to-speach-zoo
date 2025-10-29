from paddlespeech.cli.tts import TTSExecutor
import os
import nltk
from pydub import AudioSegment
from tqdm import tqdm
import shutil

# @TODO: need to run these 3 command for 1st time running
# nltk.data.path.append(os.path.join(os.getcwd(), "nltk_data"))
# nltk.data.find("taggers/averaged_perceptron_tagger")
# nltk.download('averaged_perceptron_tagger_eng')

tts_executor = TTSExecutor()

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

list_acoustic_models = [
    'fastspeech2_aishell3',
    'fastspeech2_mix',

    # @TODO: not good
    # 'tacotron2_csmsc',
    # 'fastspeech2_male',
    # 'speedyspeech_csmsc',
    # 'fastspeech2_csmsc',
    # 'fastspeech2_ljspeech',
    # 'fastspeech2_vctk',
    # 'tacotron2_ljspeech',
    # 'fastspeech2_canton',
]

list_vocoders = [
    'pwgan_csmsc',
    'pwgan_aishell3',
    'mb_melgan_csmsc',
    'style_melgan_csmsc',
    'hifigan_csmsc',  # standard
    'wavernn_csmsc',
    'pwgan_male',
    'hifigan_male',
    'hifigan_aishell3',  # only zh, cannot identify mix chinese with English for fastspeech2_aishell3 acoustic_model

    # @TODO: not good
    # 'pwgan_ljspeech',
    # 'hifigan_ljspeech',
    # 'pwgan_vctk',
    # 'hifigan_vctk',
]

# 语速配置：播放速度因子
speed_configs = {
    "slow": 0.8,
    # "normal": 1.0,
    "fast": 1.2
}


def change_speed(input_wav, output_wav, speed=1.0):
    sound = AudioSegment.from_wav(input_wav)
    # pydub 改变速度：通过改变帧率实现
    new_sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    }).set_frame_rate(sound.frame_rate)
    new_sound.export(output_wav, format="wav")


num_samples = len(list_texts)
MAX_RETRIES = 5  # 最大重试次数
print(f'number of voices: {len(list_vocoders)}')

for model_voice in list_vocoders:
    for acoustic_model in list_acoustic_models:
        save_dir = f'ttt/results_tts_AM_{acoustic_model}_Vo_{model_voice}'
        success = False  # track if at least one wav is generated

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for idx, input_text in enumerate(tqdm(list_texts, total=num_samples)):

            base_output = os.path.join(save_dir, f'output_{idx}.wav')

            try:
                wav_file = tts_executor(
                    text=input_text,
                    output=base_output,
                    am=acoustic_model,
                    voc=model_voice,
                    lang='mix',  # first try
                    spk_id=174,
                )
                success = True

            except Exception as e2:
                print(f"❌ Failed with both 'mix' and 'zh': {e2}")
                wav_file = None

            if wav_file:
                # 根据不同语速生成新文件
                for speed_name, speed_value in speed_configs.items():
                    speed_output = os.path.join(save_dir, f'output_{idx}_{speed_name}.wav')
                    change_speed(base_output, speed_output, speed=speed_value)

        # After finishing one model+vocoder
        if success:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)  # ensure folder exists only if needed
            print(f"✅ Kept folder {save_dir}")
        else:
            if os.path.exists(save_dir):
                shutil.rmtree(save_dir)  # delete failed/empty folder
                print(f"🗑 Deleted folder {save_dir} (no successful wavs)")
