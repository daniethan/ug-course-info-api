# coursetype routers
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core import dbconfig, schemas_
from repository import course_type


router = APIRouter(prefix="/course-types", tags=["Course Types"])


@router.get("", response_model=List[schemas_.ShowCourseType])
def get_all(db: Session = Depends(dbconfig.get_session)):
    return course_type.fetch_all(db)


@router.get("/show-type/{id}", response_model=schemas_.ShowCourseType)
def show(id: int, db: Session = Depends(dbconfig.get_session)):
    return course_type.show(id, db)


@router.post("/create-course-type", response_model=schemas_.ShowCourseType)
def create_type(
    request: schemas_.CourseType, db: Session = Depends(dbconfig.get_session)
):
    return course_type.create(request, db)
