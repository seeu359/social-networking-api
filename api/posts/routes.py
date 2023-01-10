from fastapi import APIRouter, Depends, status

from api.posts import schemes
from api.posts.services import PostService
from api.users.schemes import ConstructUser, User
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
) -> list[schemes.Post] | list[...]:

    """
    *Authenticated required

    Request must contain header "Authorization: Bearer {your JWT Token}"

    Response contains all posts which hidden fields is False
    """

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
    """
        *Authenticated required

        Request must contain header "Authorization: Bearer {your JWT Token}"

        The response contains post by passed id
    """

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

    """
    *Authenticated required

    Request must contain header "Authorization: Bearer {your JWT Token}"

    Create new post
    """

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

    """
    *Authenticated required

    Request must contain header "Authorization: Bearer {your JWT Token}"

    Response contains updated post. Post can only be updated by its creator
    """

    return post_services.update_post(post_data, user.id, post_id)


@router.delete(
    path='/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
        post_id: int = None,
        user: User = Depends(get_current_user),
        post_service: PostService = Depends(),
) -> list:
    """
        *Authenticated required

        Request must contain header "Authorization: Bearer {your JWT Token}"

        Response - empty body if deleting was successful.
        Post can only be deleted by its creator
        """

    return post_service.delete_post(user.id, post_id)


@router.put(
    path='/{post_id}/like',
    status_code=status.HTTP_200_OK,
    response_model=schemes.Post,
)
def like(
        post_id: int,
        user: User = Depends(get_current_user),
        post_service: PostService = Depends(),
) -> schemes.Post:
    """
    *Authorization required

    Request must contain header "Authorization: Bearer {your JWT Token}"

    Response contains updated post. Is not possible rate your own posts.
    If you have been liked earlier, a second request will remove like from
    post. If you have been disliked earlier, a second request will remove
    dislike and will put like.
    """

    return post_service.put_like(user.id, post_id)


@router.put(
    path='/{post_id}/dislike',
    status_code=status.HTTP_200_OK,
    response_model=schemes.Post,
)
def dislike(
        post_id: int = None,
        user: User = Depends(get_current_user),
        post_service: PostService = Depends(),
):
    """
    *Authorization required

    Request must contain header "Authorization: Bearer {your JWT Token}"

    Response contains updated post. Is not possible rate your own posts.
    If you have been dislike earlier, a second request will remove dislike
    from post.
    If you have been liked earlier, a second request will remove
    like and will put dislike.
    """
    return post_service.put_dislike(user.id, post_id)


@router.get(
    path='/{post_id}/like',
    status_code=status.HTTP_200_OK,
    response_model=list[ConstructUser],
)
def post_likes(
        post_id: int = None,
        user: User = Depends(get_current_user),
        post_service: PostService = Depends(),
) -> list[ConstructUser] | list:

    """
    *Authorization required

    Request must contain header "Authorization: Bearer {your JWT Token}"

    Response contains all users who put like on post by id from path operation
    """

    return post_service.get_post_likes(post_id)


@router.get(
    path='/{post_id}/dislike',
    status_code=status.HTTP_200_OK,
    response_model=list[ConstructUser],
)
def post_dislikes(
        post_id: int = None,
        user: User = Depends(get_current_user),
        post_service: PostService = Depends(),
) -> list[ConstructUser] | list:
    """
    *Authorization required

    Request must contain header "Authorization: Bearer {your JWT Token}"

    Response contains all users who put dislike on post by id from path
    operation
    """

    return post_service.get_post_dislikes(post_id)
