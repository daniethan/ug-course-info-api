import os
from dotenv import load_dotenv

load_dotenv()

PLE_RESULT_FORMAT = {
    "english": "string",
    "mathematics": "string",
    "science": "string",
    "social studies": "string",
}

UCE_RESULT_FORMAT = {
    "english": "string",
    "mathematics": "string",
    "others": [
        "string",
    ],
}

UACE_RESULT_FORMAT = {
    "gen_paper": "string",
    "subsidiary": "string",
    "main_subjects": [
        {"subject": "subject-name", "grade": "grade-letter"},
        {"subject": "subject-name", "grade": "grade-letter"},
        {"subject": "subject-name", "grade": "grade-letter"},
    ],
}


def homepage():
    response = {
        "api name": os.environ.get("API_NAME"),
        "description": os.environ.get("API_DESCRIPTION"),
        "input required": {"uce": UCE_RESULT_FORMAT, "uace": UACE_RESULT_FORMAT},
    }
    return response
