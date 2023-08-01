from src.post.models import Post
from src.repository import BaseSQLAlchemyRepository


class PostRepository(BaseSQLAlchemyRepository):
    model = Post
