from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from api.users import schemes
from api.users.services import UserServices, get_current_user

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post(
    path='/create',
    response_model=schemes.Token,
    status_code=status.HTTP_201_CREATED
)
def create_user(
        user: schemes.CreateUser,
        user_services: UserServices = Depends()
) -> schemes.Token:

    return user_services.create_user(user)


@router.post(
    path='/login',
    response_model=schemes.Token,
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserServices = Depends(),
) -> schemes.Token:

    return user_service.authenticate_user(
        form_data.username,
        form_data.password,
    )


@router.get(
    path='/me',
    response_model=schemes.User
)
def get_self_user(
        user: schemes.User = Depends(get_current_user)
) -> schemes.User:
    a = user
    logger.info(a)
    return user
