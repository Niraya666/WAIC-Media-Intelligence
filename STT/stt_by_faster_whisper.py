import argparse
from faster_whisper import WhisperModel
import json

def parse_segments(segments, save_path):
    STT_results = []
    for segment in segments:
        result = {
            'id': segment.id,
            'start': segment.start,
            'end': segment.end,
            'text': segment.text
        }
        STT_results.append(result)
        
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(STT_results, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using WhisperModel")
    parser.add_argument("audio_path", type=str, help="Path to the audio file")
    parser.add_argument("--model_size", type=str, default="large-v3", help="Size of the Whisper model")
    parser.add_argument("--device", type=str, default="cuda", help="Device to run the model on (e.g., 'cuda' or 'cpu')")
    parser.add_argument("--compute_type", type=str, default="int8", help="Compute type (e.g., 'float16' or 'int8')")
    parser.add_argument("--beam_size", type=int, default=5, help="Beam size for transcription")
    parser.add_argument("--output_path", type=str, default="STT_results.json", help="Path to save the transcription results")
    
    args = parser.parse_args()

    model = WhisperModel(args.model_size, device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(args.audio_path, beam_size=args.beam_size)
    
    print(f"Detected language '{info.language}' with probability {info.language_probability}")
    
    segments = list(segments)
    parse_segments(segments, args.output_path)

if __name__ == "__main__":
    main()
