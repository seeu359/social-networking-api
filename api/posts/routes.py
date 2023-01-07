from fastapi import APIRouter, Depends, status

from api.posts import schemes
from api.posts.services import PostService
from api.users.schemes import User
from api.users.services import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)


@router.get(
    path='/',
    response_model=list[schemes.Post],
    status_code=status.HTTP_200_OK,
)
def get_posts(
        user: User = Depends(get_current_user),
        post_services: PostService = Depends()
) -> list[schemes.Post]:

    return post_services.get_all_posts(user.id)


@router.get(
    path='/{post_id}',
    response_model=schemes.Post,
    status_code=status.HTTP_200_OK,
)
def get_post(
        post_id: int = None,
        user: User = Depends(get_current_user),
        post_services: PostService = Depends(),
) -> schemes.Post:

    return post_services.get_post(user.id, post_id)


@router.post(
    path='/create',
    response_model=schemes.Post,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
        post: schemes.CreatePost,
        user: User = Depends(get_current_user),
        post_services: PostService = Depends(),
) -> schemes.Post:

    return post_services.create_post(post, user.id)


@router.put(
    path='/{post_id}',
    response_model=schemes.Post,
    status_code=status.HTTP_200_OK,
)
def update_post(
        post_data: schemes.UpdatePost,
        post_id: int = None,
        user: User = Depends(get_current_user),
        post_services: PostService = Depends(),
) -> schemes.Post:

    return post_services.update_post(post_data, user.id, post_id)


@router.delete(
    path='/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
        post_id: int = None,
        user: User = Depends(get_current_user),
        post_service: PostService = Depends(),
) -> list:

    return post_service.delete_post(user.id, post_id)
