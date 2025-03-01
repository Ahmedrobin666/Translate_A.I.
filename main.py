import os
import whisper
from googletrans import Translator
from moviepy.editor import VideoFileClip

input_folder = "VIDEOS"
output_folder = "translated_videos"
os.makedirs(output_folder, exist_ok=True)

model = whisper.load_model("large")  

 
translator = Translator()

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

for file in os.listdir(input_folder):
    if file.endswith((".mp4", ".avi", ".mov")):
        video_path = os.path.join(input_folder, file)
        subtitle_path = os.path.join(output_folder, f"{file}.srt")

        if os.path.exists(subtitle_path):
            print(f"⚠️ الترجمة موجودة مسبقًا للملف {file}، تخطي الترجمة.")
            continue

        video_clip = VideoFileClip(video_path)
        audio_path = os.path.join(output_folder, f"{file}.mp3")
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()

        result = model.transcribe(audio_path, language="en")  
        segments = result["segments"]  

        with open(subtitle_path, "w", encoding="utf-8") as srt_file:
            for i, segment in enumerate(segments, start=1):
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                original_text = segment["text"]

                translated_text = translator.translate(original_text, dest="ar").text

                srt_file.write(f"{i}\n")
                srt_file.write(f"{start_time} --> {end_time}\n")
                srt_file.write(f"{translated_text}\n\n")

        print(f"✅ تمت ترجمة {file} وحفظ الترجمة في {subtitle_path}")
