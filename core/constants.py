import os
from dotenv import load_dotenv

load_dotenv()

API_DESCRIPTION: str = (
    "Find out the feasible university courses by providing UCE and UACE results."
)

API_ROUTE_PREFIX: str = "/api/v1"

API_TITLE: str = "UNIVERSITY COURSE API UG"

DATABASE_URI: str = os.environ.get("DATABASE")

PLE_RESULT_FORMAT: dict = {
    "english": "string",
    "mathematics": "string",
    "science": "string",
    "social studies": "string",
}

UCE_RESULT_FORMAT: dict = {
    "english": "string",
    "mathematics": "string",
    "others": [
        "string",
    ],
}

UACE_RESULT_FORMAT: dict = {
    "gen_paper": "string",
    "subsidiary": "string",
    "main_subjects": [
        {"subject": "subject-name", "grade": "grade-letter"},
        {"subject": "subject-name", "grade": "grade-letter"},
        {"subject": "subject-name", "grade": "grade-letter"},
    ],
}
