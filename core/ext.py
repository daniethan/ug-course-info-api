# file contains reusable code that accomplishes some unique important logic
from passlib.context import CryptContext
from enum import Enum


class CourseSubjectType(str, Enum):
    ESSENTIAL = "Essential"
    RELEVANT = "Relevant"
    DESIRABLE = "Desirable"


class UACECombinationDependancies(set[str], Enum):
    INT_SUBJ = {
        'ECON',
        'GEOG',
        'ENT',
    }
    SCI_SUBJ = {
        'PHY',
        'CHE',
        'BIO',
        'MTC',
        'AGRI',
        'TEC'
    }
    SCIENCES = {
        "MEG",
        "PEM",
        "PCM",
        "BCM",
        "PAM",
        "BCA",
        "PTM",
        "MEE",
        "MEA",
        "MAG",
        "PCB",
    }
    HUMANITIES = {
        "REE",
        "HEE",
        "HDG",
        "HAD",
        "HED",
        "GIA",
        "HAK",
        "GAL",
        "IRE",
        "HEG",
        "FED",
        "HEI",
        "HIK",
        "GIR",
        "DEE",
        "GIF",
        "HEK",
        "GEE",
        "LEE",
        "HIF",
        "HAR",
        "HRG",
        "HFG",
        "GIL",
        "REA",
        "LEA",
        "HIL",
        "HIG",
        "HAG",
        "LED",
        "IEE",
        "AEE",
        "HLG",
        "HEL",
        "GAK",
        "RED",
        "GAF",
        "FAI",
        "HER",
        "KAI",
        "HIR",
    }


pswd_ctxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def encrypt(password: str) -> str:
        return pswd_ctxt.hash(secret=password)

    def verify_password(plain_password, hashed_password):
        return pswd_ctxt.verify(secret=plain_password, hash=hashed_password)
