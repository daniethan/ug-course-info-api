from typing import List, Optional, Union
from pydantic import BaseModel, Field


class University(BaseModel):
    name: str
    code: str
    district: str
    
    class Config:
        orm_mode=True


class CourseTypeOut(BaseModel):
    name: str
    
    class Config:
        orm_mode=True


class Course(BaseModel):
    name: str
    code: str
    univ_code: Optional[str] = Field(default='MAK')
    cut_off_male:float
    cut_off_female:float

    class Config:
        orm_mode=True


class CourseIn(Course):
    course_type: Optional[str] = Field(default='HUM')
        
class CourseUpdate(BaseModel):
    course: str
    name: Optional[Union[str,None]] = None
    code: Optional[Union[str,None]] = None
    cut_off_male: Optional[Union[str,None]] = None
    cut_off_female: Optional[Union[str,None]] = None
    course_type: Optional[Union[str,None]] = None

class CourseOut(Course):
    coursetype: CourseTypeOut


class CourseSubjectIn(BaseModel):
    subject_name: str
    course_code: str

    class Config:
        orm_mode=True


class CourseType(CourseTypeOut):
    code: str


class ShowCourseSubject(BaseModel):
    name: str

    class Config:
        orm_mode=True   


class CourseSubject(BaseModel):
    essential: List[str] = Field(default=[])
    relevant: List[str] = Field(default=[])
    desirable: List[str] = Field(default=[])

    class Config:
        orma_mode=True


class Subject(BaseModel):
    name: str
    code: str
    is_adv: Optional[bool] = Field(default=False)
    at_both_levels: Optional[bool] = Field(default=True)

    class Config:
        orm_mode=True


class ShowCourseType(CourseType):
    courses: List[str] 


class CourseMod(Course):
    subjects: CourseSubject
    coursetype: str
    

class ShowCourse(CourseMod):
    university: University


class ShowUniversity(University):
    courses: List[Course] = Field(default=[])


class ShowSubject(Subject):
    courses: List[str]= []


class GradeOut(BaseModel):
    code: str
    value: int


class UCEResultIn(BaseModel):
    english: str
    mathematics: str
    others: List[str] = Field(..., min_items=7, max_items=8)


class UACEResult(BaseModel):
    subject: str = Field(default='Mathematics')
    grade: str = Field(default='F', min_length=1, max_length=1)

class UACEResultIn(BaseModel):
    gen_paper: str
    subsidiary: str
    main_subjects: List[UACEResult] = Field(..., min_items=3, max_items=3)


class FeaturedCourseOut(BaseModel):
    weight: float
    course: ShowCourse

    class Config:
        orm_mode=True


class ResultIn(BaseModel):
    uce: UCEResultIn
    uace: List[UACEResultIn]
    
    class Config:
        orm_mode = True


class ShowSubjectName(BaseModel):
    name: str

    class Config:
        orm_mode = True