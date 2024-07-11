import os
from pydub import AudioSegment
from groq import Groq

import time
import glob

# Initialize the Groq client
GROQ_API_KEY = "your_api_key_here"
client = Groq(api_key=GROQ_API_KEY)

# Folders for audio files and chunks
mp3_file_folder = "mp3-files"
mp3_chunk_folder = "mp3-chunks"
output_folder = "output-text"
chunk_length_ms = 400000  # Split into 400s chunks， 25MB limit for groq API
overlap_ms = 5000  # 5s overlap between chunks

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

def split_audio(mp3_file_folder, mp3_chunk_folder, episode_id, chunk_length_ms, overlap_ms, print_output):
    """
    Split the audio file into chunks and export them as individual files.
    """
    # Load the audio file
    audio = AudioSegment.from_file(os.path.join(mp3_file_folder, f"{episode_id}.wav"), format="wav")
    
    # Calculate the number of chunks
    num_chunks = len(audio) // (chunk_length_ms - overlap_ms) + (1 if len(audio) % chunk_length_ms else 0)
    
    # Split the file into chunks
    for i in range(num_chunks):
        start_ms = i * chunk_length_ms - (i * overlap_ms)
        end_ms = start_ms + chunk_length_ms
        chunk = audio[start_ms:end_ms]
        
        # Export each chunk to a file
        export_fp = os.path.join(mp3_chunk_folder, f"{episode_id}_chunk{i+1}.wav")
        chunk.export(export_fp, format="wav")
        if print_output:
            print('Exporting', export_fp)
        
    return chunk  # Return last chunk for demo purposes

def audio_to_text(filepath):
    """
    Convert audio file to text using Groq API.
    """
    with open(filepath, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filepath, file.read()),
            model="whisper-large-v3",
            language="zh"
        )
    return transcription.text

def main(audio_format="wav"):
    """
    Main function to split audio files and convert them to text.
    """
    print_output = True
    audio_files = glob.glob(os.path.join(mp3_file_folder, f"*.{audio_format}"))

    for audio_file in audio_files:
        episode_id = os.path.splitext(os.path.basename(audio_file))[0]
        print('Splitting Episode ID:', episode_id)
        
        # Split the audio file into chunks
        num_chunks = split_audio(mp3_file_folder, mp3_chunk_folder, episode_id, chunk_length_ms, overlap_ms, print_output)
        print_output = False

        # Convert each chunk to text
        text_output = []
        for i in range(1, num_chunks + 1):
            chunk_path = os.path.join(mp3_chunk_folder, f"{episode_id}_chunk{i}.wav")
            text = audio_to_text(chunk_path)
            text_output.append(text)
            
            # Save the output text to a file incrementally
            output_fp = os.path.join(output_folder, f"{episode_id}.txt")
            with open(output_fp, "a", encoding="utf-8") as output_file:
                output_file.write(text + "\n")
            print(f"Chunk {i} transcription saved to {output_fp}")

if __name__ == "__main__":
    main()
