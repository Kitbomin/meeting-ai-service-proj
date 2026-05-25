import ollama


def extract_action_items(transcript_result):

    transcript_text = ""

    for item in transcript_result:

        speaker = item["speaker"]
        text = item["text"]

        transcript_text += f"[{speaker}] {text}\n"

    prompt = f"""
다음 회의 내용을 분석하여 Action Item 을 추출해줘.

반드시 아래 JSON 형식으로만 응답해.

[
  {{
    "title": "업무 제목",
    "description": "업무 설명"
  }}
]

회의 내용:

{transcript_text}
"""

    response = ollama.chat(
        model="llama3.1:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]