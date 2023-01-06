from fastapi import APIRouter, Depends, status

from api.users.schemes import Token, CreateUser
from api.users.services import UserServices


router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post(
    path='/create',
    response_model=Token,
    status_code=status.HTTP_201_CREATED
)
def create_user(
        user: CreateUser,
        user_services: UserServices = Depends()
) -> Token:

    return user_services.create_user(user)
