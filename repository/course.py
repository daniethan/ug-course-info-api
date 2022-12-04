from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core import applogic, models_, schemas_
from sqlalchemy import or_
from typing import Union


def get_course_with_subjects(course):
    course_subjects = {
        'essential': [ess for ess in course.get_essentials],
        'relevant': [rel for rel in course.get_relevants],
        'desirable': [des for des in course.get_desirables],
    }
    subjects = schemas_.CourseSubject(**course_subjects)
    course_mod = schemas_.ShowCourse(
        name=course.name,
        code=course.code,
        univ_code=course.univ_code,
        cut_off_male=course.cut_off_male,
        cut_off_female=course.cut_off_female,
        subjects=subjects,
        coursetype=course.get_coursetype,
        university=course.university
    )

    return course_mod

    
def fetch_all(db: Session):  
    db_courses = db.query(models_.Course).all()
    
    courses = []
    for course in db_courses:
        course_mod = get_course_with_subjects(course)
        courses.append(course_mod)

    return courses


def find(id: int, db: Session):
    db_course = db.query(models_.Course).filter(
        models_.Course.id==id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id {id} was not found"
        )
    return get_course_with_subjects(db_course)


def create(request: schemas_.CourseIn, db: Session):
    course_data = {key:value for key,value in request.dict(exclude_none=True, exclude_unset=True).items() if (value is not None or value!='') }
    if len(course_data.values()) < 6 or len(course_data.values())>6:
        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail='All fields are required except subjects which may be added later'
                            )
                            
    new_course = models_.Course(
        name=request.name,
        code=request.code,
        univ_code=request.univ_code,
        cut_off_male=request.cut_off_male,
        cut_off_female=request.cut_off_female,
        course_type=request.course_type
    )

    db.add(new_course)
    db.commit()

    db.refresh(instance=new_course)
    return new_course


def search(db: Session,q: Union[str,None]):
    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No course like None found!')
    courses = []
    
    db_courses = db.query(models_.Course).filter(or_(
        (models_.Course.name).like(f'%{q}%'),
        (models_.Course.code).like(f'%{q}%'),
        (models_.Course.univ_code).like(f'%{q}%'),
        (models_.Course.course_type).contains(q),
    )).all()
    
    #search by subject
    for course in db.query(models_.Course).all():
        # print((course.make_subj_string).lower())
        if ((course.make_subj_string).lower()).find(q.lower())>-1:
            db_courses.append(course)       
    
    for course in db_courses:
        course_mod = get_course_with_subjects(course)
        courses.append(course_mod)

    return courses


def update(request: schemas_.CourseUpdate, db: Session):
    print("i reach here")
    course_to_edit = db.query(models_.Course).filter(models_.Course.code==request.course).first()
    if not course_to_edit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course named <{request.name}> not found!")
    
    new_course_data = { key: value 
                        for key,value in request.dict(exclude_none=True, exclude_unset=True).items()
                        if key != 'course'
                    }
    
    if len(new_course_data.values())==0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='At least one field should be field to edit'
        )

    for key,value in new_course_data.items():
        setattr(course_to_edit, key, value)

    db.add(course_to_edit)
    db.commit()
    db.refresh
    return 'Update Successful'


def get_course_fit(uce: schemas_.UCEResultIn, uace: schemas_.UACEResultIn, db: Session):
    courses = db.query(models_.Course).all()
    #TO USE APPLOGIC HERE
    sub_wgt = applogic.CourseWeight.get_uce_weight(uce_result_uneb=uce.dict())
    sub_wgt += applogic.CourseWeight.get_uace_sub_wgt(uace.dict())

    data = []
    for course in courses:
        msg: dict = applogic.CourseWeight.get_total_weight(uace.dict(), course, db=db)
        if msg:
            #get average cut-off points so act as threshold for recommending the course w.r.t calculated weight
            average_cut_off = ((msg.get('course').cut_off_male + msg.get('course').cut_off_female)/2)
            #modify the returned dat to fit the response model
            msg['course'] = get_course_with_subjects(msg['course'])
            msg['weight'] += sub_wgt
            #filter out courses with average cut-off above (weight+0.5)
            if msg.get('weight')>=(average_cut_off - 0.5):
                data.append(msg)
    return data    
