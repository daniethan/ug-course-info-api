from sqlalchemy.orm import Session
from core import models_, schemas_


#get all universities
def fetch_all(db: Session):
    universities = db.query(models_.University).all()
    return universities

def create(request: schemas_.University, db: Session):
    new_univ = models_.University(
        name=request.name,
        code=request.code,
        district=request.district
    )

    db.add(new_univ)
    db.commit()

    db.refresh(instance=new_univ)
    return new_univ