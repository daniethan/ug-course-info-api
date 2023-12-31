from typing import List, Optional, Union, Dict
from pydantic import BaseModel, ConfigDict, Field


class University(BaseModel):
    name: str
    code: str
    district: str

    model_config = ConfigDict(from_attributes=True)


class CourseTypeOut(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class Course(BaseModel):
    name: str
    code: str
    univ_code: Optional[str] = Field(default="MAK")
    cut_off_male: float
    cut_off_female: float

    model_config = ConfigDict(from_attributes=True)


class CourseIn(Course):
    course_type: Optional[str] = Field(default="HUM")


class CourseUpdate(BaseModel):
    course: str
    name: Optional[Union[str, None]] = None
    code: Optional[Union[str, None]] = None
    cut_off_male: Optional[Union[str, None]] = None
    cut_off_female: Optional[Union[str, None]] = None
    course_type: Optional[Union[str, None]] = None


class CourseOut(Course):
    coursetype: CourseTypeOut


class CourseSubjectIn(BaseModel):
    subject_name: str
    course_code: str

    model_config = ConfigDict(from_attributes=True)


class CourseType(CourseTypeOut):
    code: str


class ShowCourseSubject(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class CourseSubject(BaseModel):
    essential: List[str] = Field(default=[])
    relevant: List[str] = Field(default=[])
    desirable: List[str] = Field(default=[])

    class Config:
        orma_mode = True


class Subject(BaseModel):
    name: str
    code: str
    is_adv: Optional[bool] = Field(default=False)
    at_both_levels: Optional[bool] = Field(default=True)

    model_config = ConfigDict(from_attributes=True)


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
    courses: List[str] = []


class GradeOut(BaseModel):
    code: str
    value: int


class UCEResultIn(BaseModel):
    english: str
    mathematics: str
    others: List[str] = Field(..., min_items=7, max_items=8)


class CombinationResultIn(BaseModel):
    English: str = Field(...)
    Mathematics: str = Field(...)
    Physics: str = Field(...)
    Chemistry: str = Field(...)
    Biology: str = Field(...)
    Geography: str = Field(...)
    History: str = Field(...)
    others: Dict[str, str]


class CombinationOut(BaseModel):
    name: str
    subjects: list[str] = Field(..., min_items=3, max_items=4)


class UACEResult(BaseModel):
    subject: str = Field(default="Mathematics")
    grade: str = Field(default="F", min_length=1, max_length=1)


class UACEResultIn(BaseModel):
    gen_paper: str
    subsidiary: str
    main_subjects: List[UACEResult] = Field(..., min_items=3, max_items=3)


class PLEResultIn(BaseModel):
    eng: str
    mtc: str
    sci: str
    sst: str


class FeaturedCourseOut(BaseModel):
    weight: float
    course: ShowCourse

    model_config = ConfigDict(from_attributes=True)


class ResultIn(BaseModel):
    uce: UCEResultIn
    uace: List[UACEResultIn]

    model_config = ConfigDict(from_attributes=True)


class ShowSubjectName(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UACESubjectCombination(BaseModel):
    name: str = Field(
        ...,
        min_length=8,
        max_length=10,
        description="Initials of the subject combination",
    )
    main_subjects: List[ShowSubjectName] = Field(..., title="principal subjects")
    subsidiary_subjects: List[ShowSubjectName] = Field(..., title="subsidiary subjects")
    score_projection: int = Field(..., title="predicted uneb score")
