# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "librosa",
#     "noisereduce",
#     "soundfile",
# ]
# ///

import os
import subprocess
import librosa
import soundfile as sf
import noisereduce as nr
import warnings

# Suppress warnings from librosa/audioread
warnings.filterwarnings("ignore")

def process_video(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    temp_wav = f"temp_{os.path.splitext(os.path.basename(input_file))[0]}.wav"
    
    # 1. Ses Çıkarma (WAV)
    print(f"[{input_file}] Sesi WAV olarak dışa aktarılıyor...")
    subprocess.run(["ffmpeg", "-y", "-i", input_file, "-vn", "-ar", "48000", "-ac", "2", temp_wav], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # 2. Gürültü ve Boşluk Temizleme (Python kütüphaneleri)
    print(f"[{input_file}] Dip ses temizleniyor ve boşluklar kırpılıyor...")
    y, sr = librosa.load(temp_wav, sr=48000, mono=False)
    
    # Gürültü azaltma (agresif dip ses silme, %95)
    y_denoised = nr.reduce_noise(y=y, sr=sr, stationary=True, prop_decrease=0.95)
    
    # Baş/Son sessizliği kırpma (pik değerinin 45 dB altı sessizlik sayılır)
    y_mono = librosa.to_mono(y_denoised)
    _, index = librosa.effects.trim(y_mono, top_db=45)
    y_trimmed = y_denoised[:, index[0]:index[1]]
    
    # Geçici WAV dosyasına geri yazma
    sf.write(temp_wav, y_trimmed.T, sr)
    
    # 3. OPUS'a Dönüştürme (Sesi %50 artırarak)
    print(f"[{input_file}] Sesi %50 artırılarak OPUS formatına dönüştürülüyor...")
    subprocess.run(["ffmpeg", "-y", "-i", temp_wav, "-af", "volume=1.8", "-c:a", "libopus", "-b:a", "64k", output_file],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Temizlik
    os.remove(temp_wav)
    print(f"[{input_file}] Başarıyla işlendi -> {output_file}\n")

if __name__ == "__main__":
    videos = ["ding_3.mp4", "ding_tek.mp4"]
    for video in videos:
        output_name = f"clean_{os.path.splitext(video)[0]}.opus"
        process_video(video, output_name)
    print("Tüm işlemler tamamlandı!")
