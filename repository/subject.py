from typing import List
from core import models_, schemas_, ext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status



def get_subj_courses(courses: List[models_.Course], subject: str):
    for course in courses:       
        if subject in set(course.get_subjects):
            yield course.name

def fetch_all(db: Session):
    db_subjects = db.query(models_.Subject).all()
    # db_courses = db.query(models_.Course).all()
    subjects = [{"name": subject.name} for subject in db_subjects if not (str(subject).lower().find('level')) > -1]

    # for subject in db_subjects:
    #     subjects.append(schemas_.ShowSubject(
    #         name=subject.name,
    #         code=subject.code,
    #         is_adv=subject.is_adv,
    #         at_both_levels=subject.at_both_levels,
    #         courses = list(get_subj_courses(courses=db_courses, subject=subject.name))
    #     ) )
           
    return subjects

def show(id: int, db: Session):
    subject = db.query(models_.Subject).get(id)

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The subject with id {id} was not found"
        )

   
    showsubject = schemas_.ShowSubject(
        name=subject.name,
        code=subject.code,
        is_adv=subject.is_adv,
        at_both_levels=subject.at_both_levels,
        courses = list(get_subj_courses(courses=db.query(models_.Course).all(), subject=subject.name))
    )
    return showsubject

def create(request: schemas_.Subject, db: Session):
    new_subject = models_.Subject(
        name=request.name,
        code=request.code,
        is_adv=request.is_adv,
        at_both_levels=request.at_both_levels,
    )

    db.add(new_subject)
    db.commit()

    db.refresh(instance=new_subject)
    return new_subject

def add_course_subject(request: schemas_.CourseSubjectIn, db: Session,subj_type: ext.CourseSubjectType):
    subject = db.query(models_.Subject).filter(models_.Subject.name==request.subject_name).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject resource was not found"
        )
    
    if not (subject.is_adv or subject.at_both_levels):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The specified subject is not allowed")
    
    if subj_type=="Essential":
        if db.query(models_.EssentialSubject).filter(
            models_.EssentialSubject.subj_id==subject.id, 
            models_.EssentialSubject.course_code==request.course_code
            ).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The specified essential was already added")

        new_course_subj = models_.EssentialSubject(subj_id=subject.id, course_code=request.course_code)
   
    elif subj_type=="Desirable":
        if db.query(models_.DesirableSubject).filter(
            models_.DesirableSubject.subj_id==subject.id, 
            models_.DesirableSubject.course_code==request.course_code
            ).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The specified desirable was already added")
        new_course_subj = models_.DesirableSubject(subj_id=subject.id, course_code=request.course_code)
    
    else:
        if db.query(models_.RelevantSubject).filter(
            models_.RelevantSubject.subj_id==subject.id, 
            models_.RelevantSubject.course_code==request.course_code
            ).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The specified relevant was already added")
        new_course_subj = models_.RelevantSubject(subj_id=subject.id, course_code=request.course_code)

    db.add(new_course_subj)
    db.commit()

    return "Added"

