from fastapi import FastAPI

from api.posts.routes import router as posts_router
from api.users.routes import router as users_router


app = FastAPI(
    title='Webtronics-social-network',
    description='Test task for webtronics. '
                'API small social network where you can leave posts, '
                'likes/dislikes under them.'
)


@app.get('/')
def main():
    """Webtronics social network"""

    return {
        'app': 'Webtronics social network API',
        'doc_path': '/docs',
        'redoc_path': '/redoc',
    }


app.include_router(users_router)

app.include_router(posts_router)
