from pyannote.audio import Pipeline
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("HUGGINGFACE_TOKEN")

print("모델 로딩 중...")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=token
)

print("모델 로드 완료")

audio_file = "sample.wav"

diarization = pipeline(audio_file)

print("화자 분리 결과")

for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(
        f"{speaker}: "
        f"{turn.start:.1f}s ~ {turn.end:.1f}s"
    )