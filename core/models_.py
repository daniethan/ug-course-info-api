"""
New table format
"""
from itertools import chain
from .dbconfig import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship


class University(Base):
    __tablename__ = 'university'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(150), unique=True, nullable=False)
    code = Column(String(5), unique=True, nullable=False)
    district = Column(String(50), nullable=False)
    
    courses = relationship('Course', back_populates='university')


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(150), unique=True, nullable=False)
    code = Column(String(5), unique=True, nullable=False)
    is_adv = Column(Boolean, nullable=False, default=False)
    at_both_levels = Column(Boolean, nullable=False, default=True)
    # is_sci = Column(Boolean, default=False)

    essentials = relationship('EssentialSubject', back_populates='subject')
    relevants = relationship('RelevantSubject', back_populates='subject')
    desirables = relationship('DesirableSubject', back_populates='subject')
    
    def __repr__(self) -> str:
        return f"{self.name}"


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(250), unique=True, nullable=False)
    code = Column(String(5), unique=True, nullable=False)
    univ_code = Column(String, ForeignKey("university.code", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    course_type = Column(String(10), ForeignKey("course_type.code"))
    cut_off_male = Column(Float, nullable=False)
    cut_off_female = Column(Float, nullable=False)
   
    essentials = relationship('EssentialSubject', back_populates='course')
    relevants = relationship('RelevantSubject', back_populates='course')
    desirables = relationship('DesirableSubject', back_populates='course')
    university = relationship('University', back_populates='courses', foreign_keys=[univ_code])
    coursetype = relationship('CourseType', back_populates='courses', foreign_keys=[course_type])
    
    def __repr__(self) -> str:
        return f"<Course: {self.id} - {self.name} - {self.essentials}>"

    @property
    def get_essentials(self):
        return (ess.subject.name for ess in self.essentials)

    @property
    def get_relevants(self):
        return (rel.subject.name for rel in self.relevants)

    @property
    def get_desirables(self):
        return (des.subject.name for des in self.desirables)

    @property
    def get_coursetype(self):
        return self.coursetype.name

    @property
    def get_subjects(self):

        return chain(self.get_essentials,self.get_relevants,self.get_desirables)

    @property
    def make_subj_string(self):
        subjects_str = list(self.get_subjects)
        return ''.join(subjects_str)


class CourseType(Base):
    __tablename__ = 'course_type'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(250), unique=True, nullable=False)
    code = Column(String(5), unique=True, nullable=False)

    courses = relationship('Course', back_populates='coursetype')


class EssentialSubject(Base):
    __tablename__ = 'essential_subject'

    subj_id = Column(Integer,ForeignKey('subject.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    course_code = Column(String,ForeignKey('course.code', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)

    course = relationship('Course', back_populates='essentials', foreign_keys=[course_code])
    subject = relationship('Subject', back_populates='essentials', foreign_keys=[subj_id])

    def __repr__(self) -> str:
        return f"<EssentialSubject: {self.subject}-{self.course.name}>"


class RelevantSubject(Base):
    __tablename__ = 'relevant_subject'

    subj_id = Column(Integer,ForeignKey('subject.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    course_code = Column(String,ForeignKey('course.code', ondelete='CASCADE', onupdate='CASCADE'),primary_key=True, nullable=False)

    course = relationship('Course', back_populates='relevants', foreign_keys=[course_code])
    subject = relationship('Subject', back_populates='relevants', foreign_keys=[subj_id])


class DesirableSubject(Base):
    __tablename__ = 'desirable_subject'

    subj_id = Column(Integer,ForeignKey('subject.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    course_code = Column(String,ForeignKey('course.code', ondelete='CASCADE', onupdate='CASCADE'),primary_key=True, nullable=False)

    course = relationship('Course', back_populates='desirables',foreign_keys=[course_code])
    subject = relationship('Subject', back_populates='desirables', foreign_keys=[subj_id])


class Grade(Base):
    __tablename__ = 'grade'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    code = Column(String(3), unique=True, nullable=False)
    value = Column(Integer, nullable=False)
    is_advaned = Column(Boolean, nullable=False, default=False)
