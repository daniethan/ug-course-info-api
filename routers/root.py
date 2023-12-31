from fastapi import APIRouter
from repository import root

router = APIRouter(tags=["Root"])


@router.get("/docs")
def home():
    return root.homepage()
