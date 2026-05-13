import ollama
# from dotenv import load_dotenv
# import os
import json


meeting_text = """
김철수:
내일까지 로그인 API 수정해주세요.

박영희:
회원가입 UI 작업 진행하겠습니다.
"""

prompt = f"""
다음 회의 내용을 분석해서
업무(Action Item)를 JSON 배열 형태로 추출하세요.

반드시 JSON만 출력하세요.

회의 내용:
{meeting_text}
"""

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

result = response["message"]["content"]

print(result)

parsed = json.loads(result)

print("\nJSON 변환 성공")
print(parsed)