import json
from fastapi import APIRouter, UploadFile, File
import os

from app.services.stt_service import transcribe_audio
from app.services.action_item_service import extract_action_items
from app.services.trello_service import create_trello_card

router = APIRouter()

UPLOAD_DIR = "app/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/meeting/upload")
async def upload_meeting_audio(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # -----------------------------
    # STT + 화자분리
    # -----------------------------

    transcript_result = transcribe_audio(file_path)

    # -----------------------------
    # Action Item 추출
    # -----------------------------

    action_items = extract_action_items(transcript_result)

    try:
        action_items_json = json.loads(action_items)
    except:
        action_items_json = []

    # -----------------------------
    # Trello 등록
    # -----------------------------

    trello_results = []

    for item in action_items_json:

        title = item.get("title", "회의 업무")
        description = item.get("description", "")

        trello_result = create_trello_card(
            title,
            description
        )

        trello_results.append(trello_result)

    return {
        "transcript": transcript_result,
        "action_items": action_items_json,
        "trello": trello_results
    }