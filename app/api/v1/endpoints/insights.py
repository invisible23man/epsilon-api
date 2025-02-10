from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_insights():
    return {"message": "AI-driven mental health insights coming soon!"}
