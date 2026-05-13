import requests
from dotenv import load_dotenv
import os

load_dotenv()

KEY = os.getenv("TRELLO_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
LIST_ID = os.getenv("TRELLO_LIST_ID")

url = "https://api.trello.com/1/cards"


query = {
    "key": KEY,
    "token": TOKEN,
    "idList": LIST_ID,
    "name": "로그인 API 수정",
    "desc": """
담당자: 김철수
마감일: 내일까지
우선순위: HIGH
"""
}

response = requests.post(url, params=query)

print(response.status_code)
print(response.json)