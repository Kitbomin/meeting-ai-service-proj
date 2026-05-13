from pyannote.audio import Pipeline
from dotenv import load_dotenv
from pydub import AudioSegment
import torch
import whisper
import os
import json

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

AUDIO_FILE = "test1.wav"

OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("1. Whisper 로딩중ㅇㅇ")
whisper_model = whisper.load_model("large").to("cuda")

print("2. pyannote 모델 로딩중ㅇ")
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=HF_TOKEN
)

pipeline.to(torch.device("cuda"))

print("화자 분리 진행 중")
diarization = pipeline(AUDIO_FILE)

audio = AudioSegment.from_wav(AUDIO_FILE)

result = []

index = 0

print("4. STT 진행 중")

for turn, _, speaker in diarization.itertracks(yield_label=True):
    start_ms = int(turn.start * 1000)
    end_ms = int(turn.end * 1000)

    #음성 자르기ㅣㅣㅣ
    segment = audio[start_ms:end_ms]

    segment_path = os.path.join(
        OUTPUT_DIR,
        f"segment_{index}.wav"
    )

    segment.export(segment_path, format="wav")

    # 전사하기
    stt_result = whisper_model.transcribe(
        segment_path,
        language="ko"
    )

    text = stt_result["text"].strip()

    item = {
        "speaker": speaker,
        "start": round(turn.start, 2),
        "end": round(turn.end, 2),
        "text": text
    }

    result.append(item)

    print(item)

    index += 1

json_path = os.path.join(
    OUTPUT_DIR,
    "result.json"
)

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("\n 완료???????")
print(f"결과 저장 위치: {json_path}")

