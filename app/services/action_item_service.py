import json
import re

import ollama

LLM_MODEL = "llama3.1:latest"

PROMPT_TEMPLATE = """
다음 회의 내용을 분석하여 Action Item 을 추출해줘.
회의 내용에 없는 정보는 지어내지 마.

반드시 아래 JSON 형식으로만 응답해.

[
  {{
    "title": "업무 제목",
    "description": "업무 설명",
    "assignee": "담당자 (발화에서 이름이나 호칭으로 지목된 경우에만, 없으면 null)",
    "due": "기한 (발화에서 언급된 경우에만, 없으면 null)"
  }}
]

회의 내용:

{transcript_text}
"""


def _is_empty(value):

    return value is None or str(value).strip().lower() in ("", "null", "none", "없음")


def _parse_llm_json(content: str) -> list:
    """LLM 응답에서 JSON 배열을 꺼낸다.

    모델이 ```json 코드블록이나 앞뒤 설명 문장을 붙여 응답해도 파싱되도록
    첫 '[' 부터 마지막 ']' 까지를 잘라 다시 시도한다. 실패하면 빈 리스트.
    """

    text = re.sub(r"```(?:json)?", "", content).strip()

    candidates = [text]

    start, end = text.find("["), text.rfind("]")
    if start != -1 and end > start:
        candidates.append(text[start:end + 1])

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue

        if isinstance(parsed, dict):
            parsed = [parsed]

        if isinstance(parsed, list):
            return [item for item in parsed if isinstance(item, dict)]

    print("JSON Parsing Error. LLM raw response:\n", content)

    return []


def build_transcript_text(transcript_result) -> str:

    return "".join(
        f"[{item['speaker']}] {item['text'].strip()}\n" for item in transcript_result
    )


def extract_action_items(transcript_result) -> list:
    """전사 결과 → Action Item 리스트(dict). 각 항목은 title/description/assignee/due."""

    prompt = PROMPT_TEMPLATE.format(transcript_text=build_transcript_text(transcript_result))

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={"temperature": 0}
    )

    action_items = _parse_llm_json(response["message"]["content"])

    for item in action_items:

        notes = []

        if not _is_empty(item.get("assignee")):
            notes.append(f"담당자: {item['assignee']}")

        if not _is_empty(item.get("due")):
            notes.append(f"기한: {item['due']}")

        if notes:
            item["description"] = " / ".join(notes) + "\n" + str(item.get("description", ""))

    return action_items
