from app.services.diarization_service import diarize_audio
from app.services.stt_service import transcribe_segments
from app.services.action_item_service import extract_action_items
from app.services.trello_service import create_trello_cards

def run_pipeline(audio_path):

    # 화자 분리 먼저
    segments = diarize_audio(audio_path)

    # 전사
    stt_results = transcribe_segments(
        audio_path,
        segments
    )

    # 전체 회의 텍스트
    meeting_text = ""

    for item in stt_results:
        meeting_text += (
            f"{item['speaker']}:\n"
            f"{item['text']}\n\n"
        )

    # Action Item 가져오기
    action_items = extract_action_items(
        meeting_text
    )

    # trello 올리기
    create_trello_cards(action_items)

    return{
        "segments": segments,
        "stt_results": stt_results,
        "action_items": action_items
    }
    
