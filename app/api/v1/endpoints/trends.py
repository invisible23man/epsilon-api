from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_trends():
    return {"message": "Google Trends API data coming soon!"}
