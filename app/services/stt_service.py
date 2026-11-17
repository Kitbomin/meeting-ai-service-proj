import os
import sys

if sys.platform == "win32":
    import importlib.util
    for _pkg in ("nvidia.cudnn", "nvidia.cublas"):
        _spec = importlib.util.find_spec(_pkg)
        if _spec and _spec.submodule_search_locations:
            _bin_dir = os.path.join(list(_spec.submodule_search_locations)[0], "bin")
            if os.path.isdir(_bin_dir):
                os.add_dll_directory(_bin_dir)
                os.environ["PATH"] = _bin_dir + os.pathsep + os.environ.get("PATH", "")

import whisperx
import torch

from whisperx.diarize import DiarizationPipeline

from dotenv import load_dotenv

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

# 정렬·화자분리 모델은 로딩이 무거우므로 첫 요청 때 한 번만 만들고 재사용한다.
_align_models = {}
_diarize_model = None


def _get_align_model(language_code: str):

    if language_code not in _align_models:
        _align_models[language_code] = whisperx.load_align_model(
            language_code=language_code,
            device=device
        )

    return _align_models[language_code]


def _get_diarize_model():

    global _diarize_model

    if _diarize_model is None:
        _diarize_model = DiarizationPipeline(
            use_auth_token=HF_TOKEN,
            device="cpu"
        )

    return _diarize_model


def transcribe_audio(audio_file_path: str):

    # 오디오 로드
    audio = whisperx.load_audio(audio_file_path)

    # STT
    result = model.transcribe(audio)

    # Alignment
    model_a, metadata = _get_align_model(result["language"])

    aligned_result = whisperx.align(
        result["segments"],
        model_a,
        metadata,
        audio,
        device
    )

    # Diarization
    diarize_segments = _get_diarize_model()(audio_file_path)

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


def transcribe_text_only(audio_file_path: str) -> str:
    """화자분리 없이 STT 결과 텍스트만 반환 (WER 평가용)"""

    audio = whisperx.load_audio(audio_file_path)

    result = model.transcribe(audio)

    return " ".join(segment["text"].strip() for segment in result["segments"])