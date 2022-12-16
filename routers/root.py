from fastapi import APIRouter
from repository import root

router = APIRouter(
    prefix='',
    tags=['Root']
)

@router.get('/')
def home():
    return root.homepage()

@router.get('/api')
def home():
    return root.homepage()

