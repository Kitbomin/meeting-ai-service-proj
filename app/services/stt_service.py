import whisper
from pydub import AudioSegment
import os

model = whisper.load_model(
    "medium"
).to("cuda")

OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def transcribe_segments(
        audio_path,
        segments
):
    audio = AudioSegment.from_wav(audio_path)
    results = []

    for idx, segment in enumerate(segments):

        start_ms = int(segment["start"] * 1000)
        end_ms = int(segment["end"] * 1000)

        chunk = audio[start_ms:end_ms]

        chunk_path = os.path.join(
            OUTPUT_DIR,
            f"chunk_{idx}.wav"
        )

        chunk.export(
            chunk_path,
            format="wav"
        )

        result = model.transcribe(
            chunk_path,
            language="ko"
        )

        results.append({
            "speaker": segment["speaker"],
            "start": segment["start"],
            "end": segment["end"],
            "text": result["text"]
        })

    return results