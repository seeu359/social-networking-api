from fastapi import APIRouter, Depends

from api.users.schemes import User
from api.users.services import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)


@router.get(path='/')
def get_posts(user: User = Depends(get_current_user)) -> dict:

    return {'post': 'its all post, but if you\'re not authorized, you won\'t see them'}


@router.get(path='/{post_id}')
def get_posts():
    pass


@router.post(path='/create')
def create_post():
    pass


@router.put('/{post_id}')
def update_post():
    pass


@router.delete('/{post_id}')
def delete_post():
    pass
