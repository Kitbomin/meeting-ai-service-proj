import requests
from dotenv import load_dotenv
import os

load_dotenv()

KEY = os.getenv("TRELLO_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
LIST_ID = os.getenv("TRELLO_LIST_ID")

def create_trello_cards(action_items):

    url = "https://api.trello.com/1/cards"

    for item in action_items:

        query = {
            "key": KEY,
            "token": TOKEN,
            "idList": LIST_ID,
            "name": item["task"],
            "desc": f"""
담당자: {item["assignee"]}
마감일: {item["deadline"]}
우선순위: {item["priority"]}
"""
        }

        requests.post(
            url,
            params=query
        )