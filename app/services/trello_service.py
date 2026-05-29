import requests
import os

from dotenv import load_dotenv

load_dotenv()

TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_LIST_ID = os.getenv("TRELLO_LIST_ID")



def create_trello_card(title, description):

    url = "https://api.trello.com/1/cards"

    query = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "idList": TRELLO_LIST_ID,
        "name": title,
        "desc": description
    }

    response = requests.post(
        url,
        params=query
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code == 200:

        return {
            "success": True,
            "status": 200
        }

    else:

        return {
            "success": False,
            "status": response.status_code,
            "message": response.text
        }
        
        
        