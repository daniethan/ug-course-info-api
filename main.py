from fastapi import FastAPI
from core import models_, dbconfig
from routers import course, course_type, subject, university, root, combinations
from decouple import config


TAG_META_DATA = [
    {
        'name': 'Root',
        'description': "Navigates to API's root"
    },
    {
        'name': 'Universities',
        'description': 'Operations on universities'
    },
    {
        'name': 'Course Types',
        'description': 'Operations on university course types e.g Engineering course'
    },
    {
        'name': 'Courses',
        'description': 'Operations on university courses e.g BSc. Computer Engineering'
    },
    {
        'name': 'Subjects',
        'description': 'Operations on subjects required by each university course'
    },
    
]

app = FastAPI(
    title=config('API_NAME'),
    version='1.0.0',
    openapi_tags=TAG_META_DATA
)

models_.Base.metadata.create_all(bind=dbconfig.engine)


app.include_router(router=root.router)
app.include_router(router=university.router)
app.include_router(router=subject.router)
app.include_router(router=course_type.router)
app.include_router(router=course.router)
app.include_router(router=combinations.router)




# app.include_router(router=user.router)