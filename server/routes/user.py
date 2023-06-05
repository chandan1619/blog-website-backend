from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def Users():
    return "users"