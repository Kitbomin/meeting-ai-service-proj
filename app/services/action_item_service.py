import ollama
import json

def extract_action_items(meeting_text):
    prompt = f"""
다음 회의 내용을 분석해서
업무(Action Item)를 JSON 배열 형태로 추출하세요.

반드시 JSON만 출력하세요.

회의 내용:
{meeting_text}
"""
    
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
        {
            "role": "user",
            "content": prompt
        }
        ]
    )

    result = response["message"]["content"]

    return json.loads(result)