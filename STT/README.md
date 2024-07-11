# 语音识别

## 基于 Whisper 的语音识别
（需要GPU，但速度比较慢）

环境：
```
pip install git+https://github.com/openai/whisper.git
```


## 基于 Faster-Whisper 的语音识别
(需要GPU， 但速度快)
环境：
```
pip install faster-whisper
```

使用：
```
python stt_by_faster_whisper.py path/to/your/audio/file \
--model_size large-v3 \
--device cuda \
--compute_type float16 \
--beam_size 5 \
--output_path STT_results.json

```
## 基于Groq-API的语音识别
(非常快，但有使用限制)

有关Groq-API的用量限制：[Rate Limits](https://console.groq.com/docs/rate-limits#status-code--rate-limit-headers)
对于	`whisper-large-v3` 的使用限制： `on seconds of audio per hour (ASPH): Limit 7200`

有关groq文档：[Documentation](https://console.groq.com/docs/quickstart)
有关groq-audio 有关参数源码：[transcriptions](https://github.com/groq/groq-python/blob/8bcc29478315e59c2a9a730ade712511e0540f7b/src/groq/resources/audio/transcriptions.py#L34)


前提： 需要注册Groq并获得API-key

环境：
```
pip install groq --quiet
pip install openai --quiet
pip install pydub --quiet
```

使用：
修改`stt_by_groq_api.py` 中的对应参数：

```
# Initialize the Groq client
GROQ_API_KEY = "your_api_key_here"
client = Groq(api_key=GROQ_API_KEY)

# Folders for audio files and chunks
mp3_file_folder = "mp3-files"
mp3_chunk_folder = "mp3-chunks"
output_folder = "output-text"
chunk_length_ms = 400000  # Split into 400s chunks， 25MB limit for groq API
overlap_ms = 5000  # 5s overlap between chunks
```
执行`python stt_by_groq_api.py`

