# Course routers
from typing import List, Union
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from core import dbconfig, schemas_
from repository import course


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("", response_model=List[schemas_.ShowCourse])
def get_courses(db: Session = Depends(dbconfig.get_session)):
    return course.fetch_all(db)


@router.get("/show-course/{id}")  # , response_model=schemas_.ShowCourse)
async def show(id: int, db: Session = Depends(dbconfig.get_session)):
    return course.find(id, db)


@router.post("/create-course")
def create_course(
    request: schemas_.CourseIn, db: Session = Depends(dbconfig.get_session)
):
    return course.create(request, db)


@router.get("/search-course", response_model=List[schemas_.ShowCourse])
def search(
    *,
    db: Session = Depends(dbconfig.get_session),
    q: Union[str, None] = Query(None, title="free query")
):
    return course.search(db, q)


@router.put("/edit-course", status_code=status.HTTP_202_ACCEPTED)
def update_course(
    request: schemas_.CourseUpdate, db: Session = Depends(dbconfig.get_session)
):
    return course.update(request, db)


@router.post("/featured-course", response_model=List[schemas_.FeaturedCourseOut])
async def get_featured_course(
    uce: schemas_.UCEResultIn,
    uace: schemas_.UACEResultIn,
    db: Session = Depends(dbconfig.get_session),
):
    return course.get_course_fit(uce, uace, db)
