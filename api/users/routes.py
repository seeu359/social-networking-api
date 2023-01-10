from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

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
        user_data: schemes.CreateUser,
        user_services: UserServices = Depends()
) -> schemes.Token:
    """
    Create user route. Email must be valid and cannot be registered on
    temporary mail services(check by hunter.io). First name and last name must
    contain only letters. Email and username are unique fields.
    """

    return user_services.create_user(user_data)


@router.post(
    path='/login',
    response_model=schemes.Token,
    status_code=status.HTTP_200_OK,
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserServices = Depends(),
) -> schemes.Token:

    """If authenticated success, response will contain access_token which can
     be used to access routes that require authentication"""

    return user_service.authenticate_user(
        form_data.username,
        form_data.password,
    )


@router.get(
    path='/me',
    response_model=schemes.User,
    status_code=status.HTTP_200_OK
)
def get_self_user(
        user: schemes.User = Depends(get_current_user)
) -> schemes.User:
    """
    *Authenticated required

    Display data of the logged user
    """

    return user
