import json

from app.services.stt_service import transcribe_text_only
from app.services.wer_evaluation import evaluate_wer

REFERENCES_FILE = "wer_references.json"


def main():

    with open(REFERENCES_FILE, "r", encoding="utf-8") as f:
        references = json.load(f)

    results = []

    total_S = total_D = total_I = total_N = 0

    for audio_file, entry in references.items():

        reference = entry.get("reference", "").strip()

        if not reference:
            print(f"[SKIP] {audio_file}: reference 텍스트가 비어있어 건너뜁니다.")
            continue

        print(f"[STT] {audio_file} 인식 중...")

        hypothesis = transcribe_text_only(audio_file)

        metrics = evaluate_wer(reference, hypothesis)

        results.append({
            "file": audio_file,
            "reference": reference,
            "hypothesis": hypothesis,
            **metrics,
        })

        total_S += metrics["S"]
        total_D += metrics["D"]
        total_I += metrics["I"]
        total_N += metrics["N"]

    print("\n=== 파일별 WER 결과 ===")

    for r in results:
        print(f"\n[{r['file']}]")
        print(f"  reference : {r['reference']}")
        print(f"  hypothesis: {r['hypothesis']}")
        print(f"  S={r['S']}  D={r['D']}  I={r['I']}  N={r['N']}  WER={r['wer'] * 100:.2f}%")

    overall_wer = (total_S + total_D + total_I) / total_N if total_N > 0 else 0.0

    print("\n=== 전체 평균 WER ===")
    print(f"S={total_S}  D={total_D}  I={total_I}  N={total_N}  WER={overall_wer * 100:.2f}%")

    with open("wer_report.json", "w", encoding="utf-8") as f:
        json.dump({
            "results": results,
            "overall": {
                "S": total_S,
                "D": total_D,
                "I": total_I,
                "N": total_N,
                "wer": overall_wer,
            },
        }, f, ensure_ascii=False, indent=2)

    print("\n결과가 wer_report.json 에 저장되었습니다.")


if __name__ == "__main__":
    main()
