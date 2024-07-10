import whisper
import json


model = whisper.load_model("large")

result = model.transcribe(test_audio_path)

with open('STT_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

