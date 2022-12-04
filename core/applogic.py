#file contains all classes to handle course related logic

from random import randint
from sqlalchemy.orm import Session
from . import models_
from typing import Union


class CourseWeight:
    @staticmethod
    def get_uce_weight(uce_result_uneb: dict) -> float:
        uce_wgt: float = 0.0
        user_grades: list[str] = []

        for value in uce_result_uneb.values():
            if type(value)==str:
                user_grades.append(value.upper())
            elif type(value)==list:
                user_grades += value

        for grade in user_grades:
            if str(grade) in ('1','2','D1','D2'):
                uce_wgt += 0.3
            elif str(grade) in ('3','4','5','6','C3','C4','C5','C6'):
                uce_wgt += 0.2
            elif str(grade) in ('7','8','P7','P8'):
                uce_wgt += 0.1
        
        return round(uce_wgt,1)

    @staticmethod
    def get_uace_sub_wgt(uace_result_uneb: dict) -> float:
        uace_sub_wgt: float = 0.0
        uace_subsidiary_grades = [item for item in uace_result_uneb.values()][:2]

        #get weight from the desirables <The subsidiaries (2) GP and ICT or SMTC>
        for grade in uace_subsidiary_grades:
            if str(grade).capitalize() in ('1','2','D1','D2','3','4','5','6','C3','C4','C5','C6'):
                uace_sub_wgt += 1

        return uace_sub_wgt
    
    @staticmethod
    def get_total_weight(uace_result_uneb: dict, course: models_.Course, db: Session) -> Union[tuple,None]:
        main_wgt = 0.0
        
        #Extract the combination subjects alongside their grades from the provided request json
        main_subjects = {result['subject']: result['grade'] for result in [item for item in uace_result_uneb.values()][-1]}
        
        ess, rel = [], []
        #this loop's structure implies we can't have a subject added to both ess and rel lists
        for subject in main_subjects.keys():
            if subject in list(course.get_essentials):
                ess.append((subject, main_subjects.get(subject)))
            elif subject in list(course.get_relevants):
                rel.append((subject, main_subjects.get(subject)))

        #sort tuples in either list w.r.t grades
        #be careful to dodge the IndexError in case any of the lists is empty due to refering to an empty index
        ess_sorted = sorted(ess, key=lambda x:x[-1]) if len(ess) > 0 else ess
        rel_sorted = sorted(rel, key=lambda x:x[-1]) if len(rel) > 0 else rel
        # print(f"<BEFORE>\nEss:{ess}\nRel:{rel}")
        
        #the preceding for-loop implies a possibility of all 3 main subjects ending up in the ess list
        #transfer the 3rd (but technically worst performed) subject to rel list if all 3 are part of the ess list
        if len(ess_sorted)>2:
            rel_sorted.append(ess_sorted[-1])
            ess_sorted.pop()
        if len(rel_sorted)>2:
            rel_sorted.pop()
        # print(f"<AFTER>\nEss:{ess}\nRel:{rel}")

        if (len(ess_sorted) + len(rel_sorted))==3 and len(ess_sorted)==2:
            for _,grad in ess_sorted:
                grade = db.query(models_.Grade).filter(models_.Grade.code.like(f"%{grad}%")).first()
                main_wgt += 3*grade.value
            
            for _,grad in rel_sorted:
                grade = db.query(models_.Grade).filter(models_.Grade.code.like(f"%{grad}%")).first()
                main_wgt += 2*grade.value

            return {"course": course, "weight":main_wgt}
        
        return None
