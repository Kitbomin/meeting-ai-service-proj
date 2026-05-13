from fastapi import FastAPI

from app.api.meeting_api import router as meeting_router

app = FastAPI()

app.include_router(
    meeting_router,
    prefix="/meeting"
)

@app.get("/")
def root():
    return {"message": "돌아간다아아ㅏ아앙ㄺ"}