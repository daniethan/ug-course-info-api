from fastapi import APIRouter
from core.constants import (
    API_DESCRIPTION,
    API_TITLE,
    UACE_RESULT_FORMAT,
    UCE_RESULT_FORMAT,
)

router = APIRouter(tags=["Root"])


@router.get("/docs")
def homepage():
    response = {
        "api name": API_TITLE,
        "description": API_DESCRIPTION,
        "input required": {"uce": UCE_RESULT_FORMAT, "uace": UACE_RESULT_FORMAT},
    }
    return response
