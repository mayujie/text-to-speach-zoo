import os
import glob
import simpleaudio as sa

ROOT_DIR = "tts-paddlespeech/try"

def play_audio_files():
    result_dirs = [d for d in os.listdir(ROOT_DIR) if d.startswith("results_tts")]
    result_dirs.sort()

    for d in result_dirs:
        if "fastspeech2_aishell3" not in d:
        # if "fastspeech2_mix" not in d:
            continue

        folder_path = os.path.join(ROOT_DIR, d)
        print(f"\n🔊 Entering folder: {folder_path}")

        wav_files = sorted(glob.glob(os.path.join(folder_path, "*.wav")))
        if not wav_files:
            print("⚠️ No wav files found in", folder_path)
            continue

        for wav in wav_files:
            print(f"▶ Playing: {wav}")
            wave_obj = sa.WaveObject.from_wave_file(wav)
            play_obj = wave_obj.play()

            play_obj.wait_done()  # Wait until finished before playing next

            # Wait until finished or user presses Enter to skip
            # while play_obj.is_playing():
            #     try:
            #         user_input = input("Press ENTER for next, or type 'q' to quit: ")
            #         if user_input.lower() == "q":
            #             play_obj.stop()
            #             print("🛑 Exiting...")
            #             return
            #         else:
            #             play_obj.stop()
            #             break
            #     except EOFError:
            #         # In case of ctrl+D in terminal
            #         break

if __name__ == "__main__":
    play_audio_files()
