import librosa
import librosa.display

import matplotlib.pyplot as plt

# --------------------------------------------------
# Waveform + Speaker Overlay
# --------------------------------------------------

def generate_waveform_timeline(audio_file, transcript_result):

    # -----------------------------
    # 오디오 로드
    # -----------------------------

    y, sr = librosa.load(audio_file)

    # -----------------------------
    # 그래프 생성
    # -----------------------------

    fig, ax = plt.subplots(
        figsize=(15, 5)
    )

    # -----------------------------
    # waveform 출력
    # -----------------------------

    librosa.display.waveshow(
        y,
        sr=sr,
        alpha=0.6,
        ax=ax
    )

    # -----------------------------
    # speaker 색상
    # -----------------------------

    speaker_colors = {
        "SPEAKER_00": "red",
        "SPEAKER_01": "blue",
        "SPEAKER_02": "green",
        "UNKNOWN": "gray"
    }

    # -----------------------------
    # speaker 영역 표시
    # -----------------------------

    for item in transcript_result:

        speaker = item["speaker"]

        start = item["start"]

        end = item["end"]

        color = speaker_colors.get(
            speaker,
            "gray"
        )

        ax.axvspan(
            start,
            end,
            alpha=0.3,
            color=color,
            label=speaker
        )

        ax.text(
            start,
            0.8,
            speaker,
            fontsize=8
        )

    # -----------------------------
    # 중복 label 제거
    # -----------------------------

    handles, labels = ax.get_legend_handles_labels()

    unique = dict(zip(labels, handles))

    ax.legend(
        unique.values(),
        unique.keys()
    )

    # -----------------------------
    # 제목
    # -----------------------------

    ax.set_title(
        "Waveform + Speaker Timeline"
    )

    ax.set_xlabel("Time (seconds)")

    ax.set_ylabel("Amplitude")

    # -----------------------------
    # 저장
    # -----------------------------

    plt.savefig(
        "waveform_timeline.png"
    )

    print(
        "Saved: waveform_timeline.png"
    )

    plt.close()