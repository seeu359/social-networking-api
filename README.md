## Webtronics social network API

#### Linter and tests checks

[![code-check](https://github.com/seeu359/social-networking-api/actions/workflows/test_and_linter_check.yaml/badge.svg)](https://github.com/seeu359/social-networking-api/actions/workflows/test_and_linter_check.yaml)
<a href="https://codeclimate.com/github/seeu359/social-networking-api/maintainability"><img src="https://api.codeclimate.com/v1/badges/64332e6286bc594c1a69/maintainability" /></a>
<a href="https://codeclimate.com/github/seeu359/social-networking-api/test_coverage"><img src="https://api.codeclimate.com/v1/badges/64332e6286bc594c1a69/test_coverage" /></a>
---
### Description

Test task for webtronics. Simple API for social network written by FastAPI. It is possible to register and authenticate by JWT token, 
CRUD for posts, and give posts likes and dislikes

> API - https://social-networking-api-production.up.railway.app/

> SwaggerUI - https://social-networking-api-production.up.railway.app/docs

> ReDoc - https://social-networking-api-production.up.railway.app/redoc 

---
### Installation

1. Clone repo: ``$ git clone https://github.com/seeu359/social-networking-api``
2. Go to the directory with code: ``$ cd social-network-api``
3. Set the dependencies:
   1. If you're using poetry, run command: ``$ make p_install``
   2. Else: ``$ make install``

#### Environment variables

*DATABASE_URL =

*SECRET_KEY = JWT token signature. Any sequence of characters. You can generate it by command ``$ openssl rand -base64 32
``

HUNTER_API_KEY = key for hunter.io API. Is used to verify email. If HUNTER_API_KEY is None no verify will be made.

Example file with environment variables = .env.example

#### Settings file
> ./api/settings.py


#### Dependencies

| Library          | Version |
|------------------|---------|
| python           | 3.10    |
 | FastAPI          | 0.88.0  |
| pydantic[email]  | 1.10.4  |
 | request          | 3.8.3   | 
 | sqlalchemy       | 1.4.44  |
 | uvicorn          | 0.20.0  |
 | psycopg2         | 2.9.5   |
| python-dotenv    | 0.21.0  | 
| python-jose      | 3.3.0   |
| python-multipart | 0.0.5   |
| bcrypt           | 4.0.1   | 
| cryptography     | 39.0.0  |
| passlib          | 1.7.4   |
| httpx            | 0.23.3  |
| pycryptodome     | 3.16.0" |

And development dependencies:

    1.pytest
    2.isort
    3.loguru
    4.flake8
    5.pytest-cov

---

### Routes

Routes that begin from ``*`` require authorization
#### Users

``GET /users/create`` - registration route. Request body:
* ``first_name`` - must contain only letters
* ``last_name`` - must contain only letters
* ``username``
* ``email`` - You must enter valid email. If environment variables "HUNTER_API_KEY" is not None email will be checked by hunter.io service.

Response codes:
201 - Successfully created
422 - Validation Error

Response will contain JWT Token ``access_token`` which can be used for access to resources that require authorization
> {'access_token': 'token', 'token_type': 'bearer'}

``GET /users/login`` - login by username and password

Response also contains JWT TOKEN in field ``access_token``

Response codes:

``200`` - Success

``401`` - Incorrect username or password


``*GET /users/me`` - Response contains logged user

Responses codes:

``200`` - Success

``401`` - Not authenticated

#### Posts

``*GET /posts`` - Response contains all posts which field ``hidden`` is False

Responses codes:

``200`` - Success

``401`` - Not authenticated


``*GET /posts/{post_id}`` - Response contains post by entered ``post_id``

Responses codes:

``200`` - Success

``401`` - Not authenticated

``404`` - Post was not found

``*POST /posts/create`` - Route for create post. Success response contains post which was created. Request body:

* ``title`` - post title.
* ``post_body`` - body of post
* ``hidden`` - False or True. If True - post won't display in all posts.

Response codes:

``201`` - Successfully created

``401`` - Not authenticated

``422`` - Validation error

``*PUT /posts/{post_id}`` - Update post by entered ``post_id``. User can only change post his own posts. Success response contains updated post. Request body:

* ``title`` - post title
* ``post_body`` - body of post
* ``hidden`` - True or False.

Response codes:

``200`` - Success

``401`` - Not authenticated

``403`` - Attempt to delete not own post

``404`` - Post was not found

``422`` - Validation error

``*DELETE /posts/{post_id}`` - Delete post by entered ``post_id``. User can only delete post his own posts. Success response contains empty response body.

Response codes:

``204`` - Success

``401`` - Not authenticated

``403`` - Attempt to delete not own post

``404`` - Post was not found

``*GET /posts/{post_id}/like`` - Response contains all users who liked this post. 

Response codes:

``200`` - Success

``401`` - Not authenticated

``404`` - Post was not found

``*GET /posts/{post_id}/dislike`` - Response contains all users who dislike this post.

Response codes:

``200`` - Success

``401`` - Not authenticated

``404`` - Post was not found

``*PUT /posts/{post_id}/like`` - Put dislike to post by entered ``post_id``. If you liked this post before, like will be removed. If you disliked this post before - dislike will be removed, like will be added.

Response codes:

``200`` - Success

``401`` - Not authenticated

``404`` - Post was not found

``*PUT /posts/{post_id}/dislike`` - Put dislike to post by entered ``post_id``. If you dislike this post before, dislike will be removed. If you liked this post before - like will be removed, dislike will be added.

Response codes:

``200`` - Success

``401`` - Not authenticated

``404`` - Post was not found
