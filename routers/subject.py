#subject routers
from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from core import dbconfig, schemas_,ext
from repository import subject


router = APIRouter(
    prefix='/subjects',
    tags=['Subjects']
)

@router.get('/', response_model=List[schemas_.ShowSubjectName])
def get_all(db: Session=Depends(dbconfig.get_session)):
    return subject.fetch_all(db)

@router.get('/show-subject/{id}', response_model=schemas_.ShowSubject)
def show(id: int, db: Session=Depends(dbconfig.get_session)):
    return subject.show(id, db)

@router.post('/add_subject', response_model=schemas_.ShowSubject)
def add_subject(request: schemas_.Subject, db: Session=Depends(dbconfig.get_session)):
    return subject.create(request, db)


@router.post('/add-course-subject', status_code=status.HTTP_201_CREATED)
def add_course_subject(request: schemas_.CourseSubjectIn,
                        subj_type: ext.CourseSubjectType=Query(default=ext.CourseSubjectType.ESSENTIAL), 
                        db: Session=Depends(dbconfig.get_session)
                        ):
    return subject.add_course_subject(request, db, subj_type)






