from src.repository import BaseSQLAlchemyRepository

from .models import Post


class PostRepository(BaseSQLAlchemyRepository):
    model = Post
