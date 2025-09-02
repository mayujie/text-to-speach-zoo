import os
import threading
import wave
from alibaba_oauth_token import get_alibaba_token
import nls
import time
from tqdm import tqdm

URL = "wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1"
TOKEN = get_alibaba_token()
APPKEY = "1GAPpb2VqpBa69V6"


class AlibabaTTS:
    def __init__(self, text: str, voice_role: str, output_wav_path: str):
        self.text = text
        self.voice_role = voice_role
        self.output_wav_path = output_wav_path
        self.output_pcm_path = output_wav_path.replace(".wav", ".pcm")
        self._thread = threading.Thread(target=self._run)
        self._pcm_data = bytearray()

    def start(self):
        self._thread.start()

    def join(self):
        self._thread.join()

    def _on_metainfo(self, message, *args):
        print(f"[INFO] MetaInfo: {message}")

    def _on_error(self, message, *args):
        print(f"[ERROR] {message}")

    def _on_close(self, *args):
        print("[INFO] Connection closed.")

    def _on_data(self, data, *args):
        self._pcm_data.extend(data)

    def _on_completed(self, message, *args):
        print(f"[INFO] Completed: {message}")
        self._save_pcm()
        self._convert_pcm_to_wav()

    def _save_pcm(self):
        with open(self.output_pcm_path, "wb") as f:
            f.write(self._pcm_data)

    def _convert_pcm_to_wav(self):
        with wave.open(self.output_wav_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit PCM = 2 bytes
            wf.setframerate(16000)
            wf.writeframes(self._pcm_data)
        print(f"[INFO] WAV file saved at {self.output_wav_path}")
        os.remove(self.output_pcm_path)

    def _run(self):
        print(f"[INFO] Starting synthesis for: {self.output_wav_path}")
        tts = nls.NlsSpeechSynthesizer(
            url=URL,
            token=TOKEN,
            appkey=APPKEY,
            on_metainfo=self._on_metainfo,
            on_data=self._on_data,
            on_completed=self._on_completed,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        # https://help.aliyun.com/zh/isi/developer-reference/sdk-for-python-1#sectiondiv-971-l0a-puc
        result = tts.start(
            text=self.text,
            voice=self.voice_role,
            aformat='pcm',
            sample_rate=16000,
            volume=50,
            speech_rate=0,
            pitch_rate=0,
            wait_complete=True,
            start_timeout=10,
            completed_timeout=60,
        )
        print(f"[INFO] Synthesis result: {result}")


def synthesize_texts_to_wav(text: str, voice_role: str, output_wav: str) -> bool:
    try:
        tts = AlibabaTTS(
            text=text,
            voice_role=voice_role,
            output_wav_path=output_wav
        )
        tts.start()
        tts.join()  # wait current task finish
        return True
    except Exception as e:
        print(f"[ERROR] Synthesis failed: {e}")
        return False


if __name__ == "__main__":
    nls.enableTrace(True)
    SAVE_ROOT = "/nas/projects/aecc/wakeup_dataset/old/exp_alibaba_cloud_SDK_samples"
    list_voice = [
        'abin',  # standard
        'zhixiaobai',  # standard
        'zhixiaoxia',  # standard
        'zhixiaomei',  # standard
        'zhigui',  # standard
        'zhishuo',  # standard
        'aixia',  # standard

        'zhifeng_emo',  # standard
        'zhimiao_emo',  # standard
        'zhimi_emo',  # standard
        'zhiyan_emo',  # standard
        'zhibei_emo',  # standard
        'zhitian_emo',  # standard

        'xiaoyun',  # lite version
        'xiaogang',  # lite version

        'ruoxi',  # standard
        'siqi',  # standard
        'sijia',  # standard
        'sicheng',  # standard
        'aiqi',  # standard
        'aijia',  # standard
        'aicheng',  # standard
        'aida',  # standard
        'ninger',  # standard
        'ruilin',  # standard
        'siyue',  # standard
        'aiya',  # standard
        'aimei',  # standard
        'aiyu',  # standard
        'aiyue',  # standard
        'aijing',  # standard
        'xiaomei',  # standard

        'aina',  # standard
        'yina',  # standard
        'sijing',  # standard

        'sitong',  # standard
        'xiaobei',  # standard
        'aitong',  # standard
        'aiwei',  # standard
        'aibao',  # standard

        'aiyuan',  # Premium
        'aiying',  # Premium
        'aixiang',  # Premium
        'aimo',  # Premium
        'aiye',  # Premium
        'aiting',  # Premium
        'aifan',  # Premium

        'aishuo',  # standard

        'ainan',  # Premium
        'aihao',  # Premium
        'aiming',  # Premium
        'aixiao',  # Premium
        'aichu',  # Premium
        'aiqian',  # Premium

        'aishu',  # Premium
        'airu',  # Premium

        'guijie',  # standard
        'stella',  # standard
        'stanley',  # standard
        'kenny',  # standard
        'rosa',  # standard
        'mashu',  # standard

        'zhiqi',  # Premium
        'zhichu',  # Premium

        'xiaoxian',  # standard
        'yuer',  # standard
        'maoxiaomei',  # standard

        'zhixiang',  # Premium
        'zhijia',  # Premium
        'zhinan',  # Premium
        'zhiqian',  # Premium
        'zhiru',  # Premium
        'zhide',  # Premium
        'zhifei',  # Premium

        'aifei',  # standard
        'yaqun',  # standard
        'qiaowei',  # standard
        'dahu',  # standard

        'ailun',  # standard
        'jielidou',  # standard

        'zhimao',  # standard
        'zhiyuan',  # standard
        'zhiya',  # standard
        'zhiyue',  # standard
        'zhida',  # standard
        'zhistella',  # standard
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
    MAX_RETRIES = 5  # 最大重试次数
    print(f'number of voices: {len(list_voice)}')

    for voice_role in tqdm(list_voice):
        save_dir = os.path.join(SAVE_ROOT, f"voice_{voice_role}")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
            print(save_dir)

        for idx, input_text in enumerate(tqdm(list_texts, total=num_samples)):
            save_audio_file = os.path.join(save_dir, f"tts_output_{idx}.wav")

            if os.path.exists(save_audio_file):
                print(f"Audio file already exists {save_audio_file}!")
                continue

            retries = 0
            success = False

            while not success and retries < MAX_RETRIES:
                success = synthesize_texts_to_wav(
                    text=input_text,
                    voice_role=voice_role,
                    output_wav=save_audio_file
                )
                if not success:
                    retries += 1
                    print(f"[WARN] Retrying {save_audio_file} in 3 seconds... ({retries}/{MAX_RETRIES})")
                    time.sleep(3)

            if not success:
                print(f"[ERROR] Failed to synthesize after {MAX_RETRIES} retries: {save_audio_file}")
