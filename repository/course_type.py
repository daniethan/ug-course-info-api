from core import models_, schemas_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def modify_showed_coursetype(coursetype: models_.CourseType):
    type = schemas_.ShowCourseType(
        name=coursetype.name,
        code=coursetype.code,
        courses=[course.name for course in coursetype.courses]
    )
    return type

def fetch_all(db: Session):
    db_course_types = db.query(models_.CourseType).all()
    
    return [(modify_showed_coursetype(coursetype=type)) for type in db_course_types]

def show(id: int, db: Session):
    course_type = db.query(models_.CourseType).get(id)

    if not course_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id {id} was not found"
        )
    
    return modify_showed_coursetype(coursetype=course_type)

def create(request: schemas_.CourseType, db: Session):
    new_type = models_.CourseType(
        name=request.name,
        code=request.code,
    )

    db.add(new_type)
    db.commit()

    db.refresh(instance=new_type)

    return modify_showed_coursetype(new_type)    