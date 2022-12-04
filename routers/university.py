#university routers
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core import dbconfig, schemas_
from repository import university


router = APIRouter(
    prefix='/universities',
    tags=['Universities']
)

@router.get('/', response_model=List[schemas_.ShowUniversity])
def get_all(db: Session=Depends(dbconfig.get_session)):
    return university.fetch_all(db)

@router.post('/create-university', response_model=schemas_.ShowUniversity)
def create_univ(request: schemas_.University, db: Session=Depends(dbconfig.get_session)):
    return university.create(request, db)
