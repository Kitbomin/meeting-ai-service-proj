"""회의 음성 1개를 파이프라인에 통과시켜 결과를 JSON으로 저장하는 CLI.

    python run_pipeline.py 회의.m4a                 # Trello 전송 없이 결과만 저장
    python run_pipeline.py 회의.m4a --trello        # Trello 카드까지 등록
    python run_pipeline.py 회의.m4a -o result.json

출력 JSON: {audio, duration, timing, transcript[], action_items[], trello[]}
"""

import argparse
import json
import os
import time


def main():

    parser = argparse.ArgumentParser(description="Meeting AI pipeline (STT → 화자분리 → Action Item → Trello)")
    parser.add_argument("audio", help="회의 음성 파일 (wav/mp3/m4a/mp4)")
    parser.add_argument("-o", "--output", default="outputs/result.json", help="결과 JSON 경로")
    parser.add_argument("--trello", action="store_true", help="추출된 업무를 Trello 카드로 등록")
    args = parser.parse_args()

    t0 = time.perf_counter()
    from app.services.stt_service import transcribe_audio
    from app.services.action_item_service import extract_action_items
    t_load = time.perf_counter() - t0

    t0 = time.perf_counter()
    transcript = transcribe_audio(args.audio)
    t_stt = time.perf_counter() - t0

    t0 = time.perf_counter()
    action_items = extract_action_items(transcript)
    t_llm = time.perf_counter() - t0

    trello = []
    if args.trello:
        from app.services.trello_service import create_trello_card
        trello = [create_trello_card(i.get("title", "회의 업무"), i.get("description", "")) for i in action_items]

    result = {
        "audio": os.path.basename(args.audio),
        "duration": round(max((s["end"] for s in transcript), default=0), 2),
        "timing": {
            "model_load_sec": round(t_load, 1),
            "stt_diarization_sec": round(t_stt, 1),
            "action_item_sec": round(t_llm, 1),
        },
        "transcript": [
            {**s, "start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip()}
            for s in transcript
        ],
        "action_items": action_items,
        "trello": trello,
    }

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n발화 {len(transcript)}개 · 업무 {len(action_items)}개 → {args.output}")
    print(json.dumps(result["timing"], ensure_ascii=False))


if __name__ == "__main__":
    main()
