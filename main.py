from fastapi import FastAPI
from core import models_, dbconfig
from routers import course, course_type, subject, university


description = \
"""
This API provides suitable courses to university education aspirants.

Provides access to the following entities:-

##Courses

You can **see courses** included

##Subjects

You can **see subjects** included

##Course Types

You can **see course types** included

##Universities

You can **see universities** included

##Grades

You can **see grades** used

"""
tags_metadata = [
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
    title="UG-COURSE API",
    # description=description,
    version='1.0.0',
    openapi_tags=tags_metadata
)

models_.Base.metadata.create_all(bind=dbconfig.engine)


@app.get('/', tags=["Root"])
@app.get('/api', tags=['Root'])
def root():
    response = {
        "api name": "UG-COURSE API",
        "description": "Find out the feassible university courses by providing UCE and UACE results.",
        "input required": {
  "uce": {
    "english": "string",
    "mathematics": "string",
    "others": [
      "string",
      "string",
      "string",
      "string",
      "string",
      "string",
      "string"
    ]
  },
  "uace": {
    "gen_paper": "string",
    "subsidiary": "string",
    "main_subjects": [
      {
        "subject": "Mathematics",
        "grade": "F"
      },
      {
        "subject": "Mathematics",
        "grade": "F"
      },
      {
        "subject": "Mathematics",
        "grade": "F"
      }
    ]
  }
}
        
    }
    return response

app.include_router(router=university.router)
app.include_router(router=subject.router)
app.include_router(router=course_type.router)
app.include_router(router=course.router)




# app.include_router(router=user.router)