from fastapi import FastAPI

from app.routes.meeting_route import router as meeting_router

app = FastAPI()

app.include_router(meeting_router)


@app.get("/")
def health_check():
    return {
        "message": "Meeting AI Service Running"
    }