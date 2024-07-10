from faster_whisper import WhisperModel
import json

def parse_segments(segments, save_path):
    STT_results  = []
    for segment in segments:
        result = {}
        result['id'] = segment.id
        result['start'] = segment.start
        result['end'] = segment.end
        result['text'] = segment.text

    STT_results.append(result)

    with open(save_path, 'w', encoding='utf-8') as f:
       json.dump(STT_results, f, ensure_ascii=False, indent=4)



model_size = "large-v3"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(test_audio, beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

# for segment in segments:
#     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

segments = list(segments)


parse_segments(segments, 'STT_results.json')

