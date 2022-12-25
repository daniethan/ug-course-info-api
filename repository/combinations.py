from core.applogic import UACECombinationBuilder
from sqlalchemy.orm import Session


async def generate_combinations(res: dict, db: Session):
    #clean the res dict to a form our class can work with
    for key in res:
        if key.lower()=="others":
            res.update(res.get(key))
            res.pop('others')
            break
    com_builder = UACECombinationBuilder(uce_result=res, db=db)
    combinations = await com_builder.make_combinations()
    return combinations