# file contains all classes to handle course related logic

import itertools
from sqlalchemy.orm import Session
from .models_ import Subject, Course, Grade
from typing import Union
from .ext import UACECombinationDependancies as com_deps


class CourseWeight:
    @staticmethod
    def get_uce_weight(uce_result_uneb: dict) -> float:
        uce_wgt: float = 0.0
        user_grades: list[str] = []

        for value in uce_result_uneb.values():
            if type(value) == str:
                user_grades.append(value.upper())
            elif type(value) == list:
                user_grades += value

        for grade in user_grades:
            if str(grade) in ("1", "2", "D1", "D2"):
                uce_wgt += 0.3
            elif str(grade) in ("3", "4", "5", "6", "C3", "C4", "C5", "C6"):
                uce_wgt += 0.2
            elif str(grade) in ("7", "8", "P7", "P8"):
                uce_wgt += 0.1

        return round(uce_wgt, 1)

    @staticmethod
    def get_uace_sub_wgt(uace_result_uneb: dict) -> float:
        uace_sub_wgt: float = 0.0
        uace_subsidiary_grades = [item for item in uace_result_uneb.values()][:2]

        # get weight from the desirables <The subsidiaries (2) GP and ICT or SMTC>
        for grade in uace_subsidiary_grades:
            if str(grade).capitalize() in (
                "1",
                "2",
                "D1",
                "D2",
                "3",
                "4",
                "5",
                "6",
                "C3",
                "C4",
                "C5",
                "C6",
            ):
                uace_sub_wgt += 1

        return uace_sub_wgt

    @staticmethod
    def get_total_weight(
        uace_result_uneb: dict, course: Course, db: Session
    ) -> Union[tuple, None]:
        main_wgt = 0.0

        # Extract the combination subjects alongside their grades from the provided request json
        main_subjects = {
            result["subject"]: result["grade"]
            for result in [item for item in uace_result_uneb.values()][-1]
        }

        ess, rel = [], []
        # this loop's structure implies we can't have a subject added to both ess and rel lists
        for subject in main_subjects.keys():
            if subject in list(course.get_essentials):
                ess.append((subject, main_subjects.get(subject)))
            elif subject in list(course.get_relevants):
                rel.append((subject, main_subjects.get(subject)))

        # sort tuples in either list w.r.t grades
        # be careful to dodge the IndexError in case any of the lists is empty due to refering to an empty index
        ess_sorted = sorted(ess, key=lambda x: x[-1]) if len(ess) > 0 else ess
        rel_sorted = sorted(rel, key=lambda x: x[-1]) if len(rel) > 0 else rel
        # print(f"<BEFORE>\nEss:{ess}\nRel:{rel}")

        # the preceding for-loop implies a possibility of all 3 main subjects ending up in the ess list
        # transfer the 3rd (but technically worst performed) subject to rel list if all 3 are part of the ess list
        if len(ess_sorted) > 2:
            rel_sorted.append(ess_sorted[-1])
            ess_sorted.pop()
        if len(rel_sorted) > 2:
            rel_sorted.pop()
        # print(f"<AFTER>\nEss:{ess}\nRel:{rel}")

        if (len(ess_sorted) + len(rel_sorted)) == 3 and len(ess_sorted) == 2:
            for _, grad in ess_sorted:
                grade = (
                    db.query(Grade)
                    .filter(Grade.code.like(f"%{grad}%"))
                    .first()
                )
                main_wgt += 3 * grade.value

            for _, grad in rel_sorted:
                grade = (
                    db.query(Grade)
                    .filter(Grade.code.like(f"%{grad}%"))
                    .first()
                )
                main_wgt += 2 * grade.value

            return {"course": course, "weight": main_wgt}

        return None


class UACECombinationBuilder:
    """Builds a suggested combination basing the UCE and PLE UNEB assesments"""
    WORST_GRADE = 6

    def __init__(self, uce_result: dict, db: Session) -> None:
        self.valid_sci_combnz: set = com_deps.SCIENCES.value
        self.valid_hum: set = com_deps.HUMANITIES.value
        self.uce_res: dict = uce_result
        self.subjects: dict = {}
        self.db: Session = db
    
    #filter out all subjects whose grades are greater than 
    def _check_grade(self, grade: int) -> bool:
        return grade in range(1, UACECombinationBuilder.WORST_GRADE + 1)
    
    #fetch subject code from database
    async def _get_subject_code(self, subject_name: str) -> str|None:
        subject: Subject|None = self.db.query(Subject).filter(Subject.name==subject_name.title()).first()
        return subject.code if subject is not None else None

    #create a dictionary of subject codes against their fullnames
    async def extract_subjects(self, res_dict: dict) -> dict:
        subjects: dict = {}
        for subj in res_dict.keys():
            subj_obj: Subject = self.db.query(Subject).filter(Subject.code==subj).first()
            subjects.update({subj: subj_obj.name})
        
        return subjects 

    #Change all grades of the subjects into their equivalent integers
    async def _clean_result(self) -> dict[str, int]:
        clean_uce_res: dict = {}
        for key in self.uce_res.keys():
            grade_int = int(self.uce_res.get(key,'0')[-1])
            if self._check_grade(grade_int):
                subj_code: str|None = await self._get_subject_code(subject_name=key)
                if subj_code is not None:
                    clean_uce_res[subj_code] = self.uce_res.get(key)
        return clean_uce_res

    async def _sort_results(self) -> dict:
        """Returns best subject results with initials as keys and grades not more that C7"""  
        clean_data: dict = await self._clean_result()   
        return dict(sorted(clean_data.items(), key=lambda x: x[-1]))

    async def _match_uce_subj_to_uace_equivalent(self) -> dict:
        uace_equiv: dict = {}
        clean_data = await self._sort_results()
        
        for subj in clean_data.keys():
            obj_subj: Subject = self.db.query(Subject).filter(Subject.code==subj).first()
            if obj_subj.is_adv or obj_subj.at_both_levels:
                uace_equiv.update({subj: clean_data.get(subj)})
            elif subj=='COM':
                uace_equiv.update({'ECON': clean_data.get(subj)})
        
        return uace_equiv

    @staticmethod
    def group_subjects(subj_codes: list) -> dict:
        grouped_subjects: dict = {
            'sci': set(),
            'hum': set()
        }
        for code in subj_codes:
            if code in com_deps.SCI_SUBJ.value.union(com_deps.INT_SUBJ.value):
                grouped_subjects['sci'].add(code)
            if code in com_deps.INT_SUBJ.value or code not in com_deps.SCI_SUBJ.value:
                grouped_subjects['hum'].add(code)
        
        return grouped_subjects

    async def _build(self, subjects: set):
        available_combinations = list()
        
        def _create_arrangement(subj: list|tuple):
            return "".join((x[0] for x in subj))

        if len(subjects) >= 3:
            #form unique mathematical combinations of three of the subjects in list given
            subj_combnz = list(itertools.combinations(subjects, 3))
            
            for combn in subj_combnz:
                #form all the possible arrangements for each combination above
                arrangements = (_create_arrangement(x) for x in itertools.permutations(combn, 3))
                
                for combination in arrangements:
                    if combination in com_deps.SCIENCES.value.union(com_deps.HUMANITIES.value):
                        combn_subj = [self.subjects[code] for code in combn]
                        available_combinations.append({'name':combination, 'subjects':combn_subj})
                        break
        
        return available_combinations if len(available_combinations) > 0 else None

    async def make_combinations(self) -> set[dict]:
        combinations = list()
        clean_data_uace: dict = await self._match_uce_subj_to_uace_equivalent()
        self.subjects: dict = await self.extract_subjects(res_dict=clean_data_uace)
        subj_grps = UACECombinationBuilder.group_subjects([code for code in self.subjects.keys()])
        
        for grp in subj_grps.keys():
            built_combnz: list = await self._build(subjects=subj_grps.get(grp))
            
            if built_combnz is not None:
                combinations += built_combnz
            
        return combinations