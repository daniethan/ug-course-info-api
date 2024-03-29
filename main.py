from core.constants import API_ROUTE_PREFIX, API_TITLE
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from fastapi import FastAPI
from core.models_ import Base
from core.dbconfig import engine
from fastapi.responses import RedirectResponse
from routers import course, course_type, subject, university, root, combinations


TAG_META_DATA = [
    {"name": "Root", "description": "Navigates to API's root"},
    {"name": "Universities", "description": "Operations on universities"},
    {
        "name": "Course Types",
        "description": "Operations on university course types e.g Engineering course",
    },
    {
        "name": "Courses",
        "description": "Operations on university courses e.g BSc. Computer Engineering",
    },
    {
        "name": "Subjects",
        "description": "Operations on subjects required by each university course",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> _AsyncGeneratorContextManager[None]:
    # Create the tables in the database
    # on app start up.
    Base.metadata.create_all(engine)
    yield
    # clean up code after shutdown goes here


app = FastAPI(
    title=API_TITLE if API_TITLE else "FastAPI",
    lifespan=lifespan,
    version="1.0.0",
    openapi_tags=TAG_META_DATA,
)


@app.get(path="/", tags=["Root"], include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


app.include_router(router=root.router, prefix=API_ROUTE_PREFIX)
app.include_router(router=university.router, prefix=API_ROUTE_PREFIX)
app.include_router(router=subject.router, prefix=API_ROUTE_PREFIX)
app.include_router(router=course_type.router, prefix=API_ROUTE_PREFIX)
app.include_router(router=course.router, prefix=API_ROUTE_PREFIX)
app.include_router(router=combinations.router, prefix=API_ROUTE_PREFIX)


# app.include_router(router=user.router)
