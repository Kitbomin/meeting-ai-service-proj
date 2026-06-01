import whisperx
import torch

from whisperx.diarize import DiarizationPipeline

from dotenv import load_dotenv

import os

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

device = "cuda" if torch.cuda.is_available() else "cpu"

print("WhisperX Device: ", device)

if device == "cuda":
    print(torch.cuda.get_device_name(0))
    
model = whisperx.load_model(
    "medium",
    device=device,
    compute_type="float32"
)

def transcribe_audio(audio_file_path: str):

    # 오디오 로드
    audio = whisperx.load_audio(audio_file_path)

    # STT
    result = model.transcribe(audio)

    # Alignment
    model_a, metadata = whisperx.load_align_model(
        language_code=result["language"],
        device=device
    )

    aligned_result = whisperx.align(
        result["segments"],
        model_a,
        metadata,
        audio,
        device
    )

    # Diarization
    diarize_model = DiarizationPipeline(
    token=HF_TOKEN,
    device="cpu"
)

    diarize_segments = diarize_model(audio_file_path)

    # 화자 매핑
    final_result = whisperx.assign_word_speakers(
        diarize_segments,
        aligned_result
    )

    transcript_result = []

    for segment in final_result["segments"]:

        transcript_result.append({
            "speaker": segment.get("speaker", "UNKNOWN"),
            "start": segment.get("start", 0),
            "end": segment.get("end", 0),
            "text": segment.get("text", "")
        })

    return transcript_result