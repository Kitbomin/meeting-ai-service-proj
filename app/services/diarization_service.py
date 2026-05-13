from pyannote.audio import Pipeline
from dotenv import load_dotenv
import os
import torch

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=HF_TOKEN
)

pipeline.to(torch.device("cuda"))

def diarize_audio(audio_path):
    diarization = pipeline(audio_path)

    segments = []

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({
            "speaker": speaker,
            "start": turn.start,
            "end": turn.end
        })

    return segments