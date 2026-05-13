from fastapi import APIRouter, UploadFile, File

from app.services.diarization_service import diarize_audio
from app.services.stt_service import transcribe_segments

import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_meeting_audio(
    file: UploadFile = File(...)
):
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 화자 분리 기능
    segments = diarize_audio(file_path)

    # STT
    results = transcribe_segments(
        file_path,
        segments
    )

    return {
        "message": "처리 완료",
        "result": results
    }

