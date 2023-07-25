from post.models import Post
from repository import BaseSQLAlchemyRepository


class PostRepository(BaseSQLAlchemyRepository):
    model = Post
