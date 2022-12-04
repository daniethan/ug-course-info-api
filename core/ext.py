# file contains reusable code that accomplishes some unique important logic
from passlib.context import CryptContext
from enum import Enum


class CourseSubjectType(str, Enum):
    ESSENTIAL = 'Essential'
    RELEVANT = 'Relevant'
    DESIRABLE = 'Desirable'


pswd_ctxt = CryptContext(schemes=['bcrypt'], deprecated="auto")
class Hash:
    @staticmethod
    def encrypt(password: str) -> str:
        return pswd_ctxt.hash(secret=password)

    def verify_password(plain_password, hashed_password):
        return pswd_ctxt.verify(secret=plain_password, hash=hashed_password)