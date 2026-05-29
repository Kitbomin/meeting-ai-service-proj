import os
import streamlit as st

from app.services.trello_service import (
    create_trello_card
)

from app.services.stt_service import transcribe_audio

from app.services.timeline_visualizer import generate_timeline

from app.services.waveform_visualizer import (
    generate_waveform_timeline
)

from app.services.action_item_service import (
    extract_action_items
)

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="AI Meeting Automation",
    layout="wide"
)

# --------------------------------------------------
# 제목
# --------------------------------------------------

st.title("AI Meeting Automation System")

st.markdown("""
회의 음성 파일을 업로드하면:

- 화자 분리
- 음성 텍스트 변환(STT)
- Action Item 추출
- Trello 자동화
- 시각화 생성

을 수행합니다.
""")

# --------------------------------------------------
# 업로드 폴더 생성
# --------------------------------------------------

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

# --------------------------------------------------
# 파일 업로드
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "회의 음성 파일 업로드",
    type=["wav", "mp3", "m4a"]
)

# --------------------------------------------------
# 파일 업로드 처리
# --------------------------------------------------

if uploaded_file:

    save_path = os.path.join(
        UPLOAD_DIR,
        uploaded_file.name
    )

    # 파일 저장
    with open(save_path, "wb") as f:

        f.write(uploaded_file.read())

    st.success("파일 업로드 완료")

    # --------------------------------------------------
    # 분석 버튼
    # --------------------------------------------------

    if st.button("회의 분석 시작"):

        # 진행률 UI
        progress_bar = st.progress(0)

        status_text = st.empty()

        # --------------------------------------------------
        # STEP 1
        # --------------------------------------------------

        status_text.text(
            "음성 분석 준비중..."
        )

        progress_bar.progress(10)

        # --------------------------------------------------
        # STEP 2
        # --------------------------------------------------

        status_text.text(
            "화자 분리 및 STT 진행중..."
        )

        progress_bar.progress(30)

        # STT + 화자분리
        transcript_result = transcribe_audio(
            save_path
        )

        # --------------------------------------------------
        # STEP 3
        # --------------------------------------------------

        status_text.text(
            "Speaker Timeline 생성중..."
        )

        progress_bar.progress(60)

        generate_timeline(
            transcript_result
        )

        # --------------------------------------------------
        # STEP 4
        # --------------------------------------------------

        status_text.text(
            "Waveform 시각화 생성중..."
        )

        progress_bar.progress(80)

        generate_waveform_timeline(
            save_path,
            transcript_result
        )

        # --------------------------------------------------
        # STEP 5
        # --------------------------------------------------

        status_text.text(
            "Action Item 추출중..."
        )

        action_items = extract_action_items(
            transcript_result
        )

        progress_bar.progress(100)

        status_text.text(
            "분석 완료"
        )

        st.success(
            "회의 분석 완료"
        )

        # ==================================================
        # Transcript 출력
        # ==================================================

        st.divider()

        st.subheader(
            "Transcript"
        )

        for item in transcript_result:

            speaker = item.get(
                "speaker",
                "UNKNOWN"
            )

            start = item.get(
                "start",
                0
            )

            end = item.get(
                "end",
                0
            )

            text = item.get(
                "text",
                ""
            )

            st.markdown(f"""
**[{speaker}]**
({start:.1f}s ~ {end:.1f}s)

{text}
""")

        # ==================================================
        # Speaker Timeline
        # ==================================================

        st.divider()

        st.subheader(
            "Speaker Timeline"
        )

        st.image(
            "speaker_timeline.png"
        )

        # ==================================================
        # Waveform Timeline
        # ==================================================

        st.divider()

        st.subheader(
            "Waveform Visualization"
        )

        st.image(
            "waveform_timeline.png"
        )

        # ==================================================
        # Action Items
        # ==================================================

        st.divider()

        st.subheader(
            "Action Items"
        )

        if len(action_items) == 0:

            st.warning(
                "추출된 Action Item이 없습니다."
            )

        else:
            
            trello_results = []

            for item in action_items:

                title = item.get(
                    "title",
                    ""
                )

                description = item.get(
                    "description",
                    ""
                )
                
                trello_result = create_trello_card(
                    title,
                    description
                )

                trello_results.append(
                    trello_result
                )

                st.markdown(f"""
### {title}

{description}
""")

        # ==================================================
        # 완료 메시지
        # ==================================================

        st.divider()
        
        st.subheader("Trello Result")

        st.success(
            "AI 회의 자동화 프로세스 완료"
        )