import matplotlib.pyplot as plt

# --------------------------------------------------
# Speaker Timeline 시각화
# --------------------------------------------------

def generate_timeline(transcript_result):

    fig, ax = plt.subplots(figsize=(12, 4))

    speakers = []

    y_positions = {}

    current_y = 10

    # -----------------------------
    # speaker 목록 생성
    # -----------------------------

    for item in transcript_result:

        speaker = item["speaker"]

        if speaker not in speakers:

            speakers.append(speaker)

            y_positions[speaker] = current_y

            current_y += 10

    # -----------------------------
    # timeline 그리기
    # -----------------------------

    for item in transcript_result:

        speaker = item["speaker"]

        start = item["start"]

        end = item["end"]

        duration = end - start

        y = y_positions[speaker]

        ax.broken_barh(
            [(start, duration)],
            (y, 5)
        )

        ax.text(
            start,
            y + 2,
            speaker,
            fontsize=8
        )

    # -----------------------------
    # 축 설정
    # -----------------------------

    ax.set_xlabel("Time (seconds)")

    ax.set_ylabel("Speaker")

    ax.set_title("Speaker Timeline")

    ax.set_yticks(
        [y + 2 for y in y_positions.values()]
    )

    ax.set_yticklabels(
        speakers
    )

    ax.grid(True)

    # -----------------------------
    # 저장
    # -----------------------------

    plt.savefig("speaker_timeline.png")

    print("Timeline saved: speaker_timeline.png")

    plt.close()