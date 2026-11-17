import os
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.action_item_service import extract_action_items
from app.services.stt_service import transcribe_audio
from app.services.trello_service import create_trello_card

router = APIRouter()

UPLOAD_DIR = "app/uploads"
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".mp4"}

os.makedirs(UPLOAD_DIR, exist_ok=True)


def _safe_upload_path(filename: str) -> str:
    """사용자가 보낸 파일명을 경로로 그대로 쓰지 않는다 (../ 경로 조작 방지)."""

    ext = os.path.splitext(os.path.basename(filename or ""))[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"지원하지 않는 형식입니다: {ext or '(없음)'}")

    return os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}{ext}")


@router.post("/meeting/upload")
async def upload_meeting_audio(file: UploadFile = File(...), send_to_trello: bool = True):

    file_path = _safe_upload_path(file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # STT + 화자분리
    transcript_result = transcribe_audio(file_path)

    # Action Item 추출 (이미 list[dict] 로 반환됨 — 다시 json.loads 하면 안 됨)
    action_items = extract_action_items(transcript_result)

    # Trello 등록
    trello_results = []

    if send_to_trello:
        for item in action_items:
            trello_results.append(
                create_trello_card(
                    item.get("title", "회의 업무"),
                    item.get("description", "")
                )
            )

    return {
        "transcript": transcript_result,
        "action_items": action_items,
        "trello": trello_results
    }
