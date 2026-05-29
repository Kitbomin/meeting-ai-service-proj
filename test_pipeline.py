# import whisperx
# import torch

# device = "cuda" if torch.cuda.is_available() else "cpu"

# print("Device:", device)

# if device == "cuda":
#     print(torch.cuda.get_device_name(0))

# audio_file = "sample.wav"

# model = whisperx.load_model(
#     "base",
#     device=device,
#     compute_type="float32"
# )

# audio = whisperx.load_audio(audio_file)

# result = model.transcribe(audio)

# print(result["segments"])

from app.services.stt_service import transcribe_audio
from app.services.timeline_visualizer import generate_timeline
from app.services.waveform_visualizer import generate_waveform_timeline
from app.services.progress_service import ProgressManager
# --------------------------------------------------
# Progress 시작
# --------------------------------------------------

progress = ProgressManager()

# --------------------------------------------------
# STEP 1
# --------------------------------------------------

progress.update(
    10,
    "Audio Upload Completed"
)

# --------------------------------------------------
# STEP 2
# --------------------------------------------------

progress.update(
    30,
    "Speaker Diarization Running"
)

# --------------------------------------------------
# STT + 화자분리
# --------------------------------------------------

result = transcribe_audio("sample.wav")

# --------------------------------------------------
# STEP 3
# --------------------------------------------------

progress.update(
    60,
    "Generating Speaker Timeline"
)

generate_timeline(result)

# --------------------------------------------------
# STEP 4
# --------------------------------------------------

progress.update(
    80,
    "Generating Waveform Visualization"
)

generate_waveform_timeline(
    "sample.wav",
    result
)

# --------------------------------------------------
# STEP 5
# --------------------------------------------------

progress.update(
    100,
    "Trello Automation Completed"
)

# --------------------------------------------------
# 종료
# --------------------------------------------------

progress.finish()